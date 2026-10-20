"""Bounded, data-only inputs shared by the two advisory tools."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import unicodedata

from audit import text_findings

MAX_BYTES = 1024 * 1024
MAX_FILES = 100

class InputError(ValueError):
    pass

def read_packet(path):
    path = Path(path)
    if path.suffix.lower() != '.json' or path.name.casefold() in {'auth.json','credentials.json','secrets.json'} or path.name.startswith('.env'):
        raise InputError('EXCLUDED_INPUT_FILE')
    for item in (path, *path.parents):
        if item.is_symlink() or (hasattr(item, 'is_junction') and item.is_junction()):
            raise InputError('REDIRECTED_INPUT')
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise InputError('MISSING_OR_OVERSIZED_INPUT')
    try:
        raw = path.read_bytes()
        if len(raw) > MAX_BYTES:
            raise InputError('OVERSIZED_INPUT')
        return json.loads(raw.decode('utf-8'), object_pairs_hook=unique_keys)
    except (UnicodeError, json.JSONDecodeError, OSError, RecursionError):
        raise InputError('INVALID_INPUT') from None

def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result

def logical_path(value):
    if not isinstance(value, str) or not value or len(value) > 240:
        raise InputError('INVALID_LOGICAL_PATH')
    try:
        value.encode('utf-8')
    except UnicodeError:
        raise InputError('INVALID_UNICODE') from None
    value = unicodedata.normalize('NFC', value)
    if (PurePosixPath(value).is_absolute() or '\\' in value or
            re.search(r'[\x00-\x1f\x7f<>:"|?*]', value) or text_findings(value)):
        raise InputError('UNSAFE_LOGICAL_PATH')
    for part in value.split('/'):
        if (part in ('', '.', '..', '.git') or part.endswith((' ', '.')) or
                re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part)):
            raise InputError('NONPORTABLE_LOGICAL_PATH')
    return value

def validate_packet(packet, top_fields, file_fields):
    if not isinstance(packet, dict) or set(packet) != set(top_fields):
        raise InputError('INVALID_PACKET_FIELDS')
    if packet['schema_version'] != 1 or type(packet['schema_version']) is not int or packet['synthetic'] is not True:
        raise InputError('SYNTHETIC_SCHEMA_V1_REQUIRED')
    revision = packet['revision']
    if not isinstance(revision, str) or not re.fullmatch(r'[A-Za-z0-9._-]{1,80}', revision) or text_findings(revision):
        raise InputError('INVALID_REVISION')
    files = packet['files']
    if not isinstance(files, list) or not 1 <= len(files) <= MAX_FILES:
        raise InputError('INVALID_FILE_COUNT')
    seen = set()
    validated = []
    for record in files:
        if not isinstance(record, dict) or set(record) != set(file_fields):
            raise InputError('INVALID_FILE_FIELDS')
        path = logical_path(record['path'])
        if path.casefold() in seen:
            raise InputError('DUPLICATE_OR_CASE_COLLIDING_PATH')
        seen.add(path.casefold())
        item = dict(record, path=path)
        for key in set(file_fields) - {'path'}:
            content = item[key]
            if content is not None and not isinstance(content, str):
                raise InputError('INVALID_FILE_CONTENT')
            try:
                size = len(content.encode('utf-8')) if content is not None else 0
            except UnicodeError:
                raise InputError('INVALID_UNICODE') from None
            if content is not None and (size > MAX_BYTES or '\x00' in content):
                raise InputError('OVERSIZED_OR_BINARY_CONTENT')
            if content and text_findings(content):
                raise InputError('SENSITIVE_INPUT_REFUSED')
        validated.append(item)
    return validated

def digest_files(files):
    data = json.dumps(sorted(files, key=lambda x:x['path']), ensure_ascii=True, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
