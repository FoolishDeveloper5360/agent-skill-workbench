#!/usr/bin/env python3
"""Create/verify a frozen directory's file inventory; not a backup or model validator."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def inventory(root, manifest):
    result = {}

    def fail_walk(error):
        raise error

    for current, dirs, files in os.walk(root, followlinks=False, onerror=fail_walk):
        for name in dirs + files:
            path = Path(current) / name
            if is_redirect(path):
                raise ValueError(f'Links/reparse points are unsupported: {path.relative_to(root)}')
        for name in files:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            if relative == manifest:
                continue
            if not path.is_file():
                raise ValueError(f'Not a regular file: {relative}')
            result[relative] = {'path': relative, 'bytes': path.stat().st_size,
                                'sha256': digest(path)}
    if not result:
        raise ValueError('Checkpoint has no payload files')
    return result


def is_redirect(path):
    """Reject symlinks and Windows junctions/cloud reparse points without following them."""
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, 'st_file_attributes', 0)
        & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)
    )


def run(args):
    root = Path(args.root).expanduser()
    if not root.is_dir() or is_redirect(root):
        raise ValueError('Root must be an existing non-symlink directory')
    root = root.resolve()
    name = args.manifest
    if not name or name in ('.', '..') or '/' in name or '\\' in name:
        raise ValueError('Manifest must be a single filename within the root')
    target = root / name
    if (target.exists() or target.is_symlink()) and (is_redirect(target) or not target.is_file()):
        raise ValueError('Manifest must be a regular file, not a symbolic link')
    actual = inventory(root, name)
    if args.command == 'create':
        data = {'schema': 'checkpoint-manifest-v1', 'algorithm': 'sha256',
                'files': [actual[key] for key in sorted(actual)]}
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                             dir=root, delete=False) as f:
                temporary = Path(f.name)
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write('\n')
                f.flush()
                os.fsync(f.fileno())
            os.replace(temporary, target)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
        print(f'Created {name}: {len(actual)} files')
        return
    data = json.loads(target.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('schema') != 'checkpoint-manifest-v1' or data.get('algorithm') != 'sha256':
        raise ValueError('Unsupported manifest schema or algorithm')
    entries = data.get('files')
    if not isinstance(entries, list) or not entries:
        raise ValueError('Manifest requires a nonempty file list')
    expected = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Invalid manifest entry')
        path = entry.get('path')
        if not isinstance(path, str) or not path or '\\' in path:
            raise ValueError('Invalid path')
        parts = PurePosixPath(path).parts
        if path.startswith('/') or '..' in parts or PurePosixPath(path).as_posix() != path or path == name:
            raise ValueError(f'Unsafe or noncanonical path: {path}')
        if path in expected:
            raise ValueError(f'Duplicate path: {path}')
        if type(entry.get('bytes')) is not int or entry['bytes'] < 0 or not isinstance(entry.get('sha256'), str) or not re.fullmatch('[0-9a-f]{64}', entry['sha256']):
            raise ValueError(f'Invalid size or hash: {path}')
        expected[path] = entry
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(key for key in set(actual) & set(expected)
                     if any(actual[key][field] != expected[key][field] for field in ('bytes', 'sha256')))
    if missing or extra or changed:
        raise ValueError(f'Verification failed; missing={missing}, extra={extra}, changed={changed}')
    print(f'Verified {len(actual)} files: sizes and SHA-256 match; durability not assessed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('create', 'verify'))
    parser.add_argument('root')
    parser.add_argument('--manifest', default='manifest.json')
    args = parser.parse_args()
    try:
        run(args)
    except (OSError, ValueError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
