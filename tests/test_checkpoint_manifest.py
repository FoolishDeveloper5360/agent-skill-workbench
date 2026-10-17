"""Behavioral regression tests; run from the repository root with unittest discover."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = (Path(__file__).resolve().parents[1] / 'reference-modeling-quality'
          / 'scripts' / 'checkpoint_manifest.py')
SPEC = importlib.util.spec_from_file_location('checkpoint_manifest', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='checkpoint-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source').mkdir()
        (self.root / 'source' / '模型 sample.bin').write_bytes(b'payload')

    def run_tool(self, command, name='manifest.json'):
        with contextlib.redirect_stdout(io.StringIO()):
            MODULE.run(argparse.Namespace(root=str(self.root), command=command, manifest=name))

    def rewrite_manifest(self, transform):
        target = self.root / 'manifest.json'
        data = json.loads(target.read_text(encoding='utf-8'))
        transform(data)
        target.write_text(json.dumps(data), encoding='utf-8')

    def test_roundtrip_unicode_and_custom_name(self):
        self.run_tool('create', 'inventory.json')
        self.run_tool('verify', 'inventory.json')
        data = json.loads((self.root / 'inventory.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['files']), 1)
        self.assertEqual(data['files'][0]['path'], 'source/模型 sample.bin')

    def test_same_size_mutation_detected(self):
        self.run_tool('create')
        (self.root / 'source' / '模型 sample.bin').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'changed='):
            self.run_tool('verify')

    def test_missing_payload_detected(self):
        (self.root / 'keep.bin').write_bytes(b'keep')
        self.run_tool('create')
        (self.root / 'source' / '模型 sample.bin').unlink()
        with self.assertRaisesRegex(ValueError, 'missing='):
            self.run_tool('verify')

    def test_extra_payload_detected(self):
        self.run_tool('create')
        (self.root / 'extra.bin').write_bytes(b'extra')
        with self.assertRaisesRegex(ValueError, 'extra='):
            self.run_tool('verify')

    def test_empty_payload_rejected(self):
        (self.root / 'source' / '模型 sample.bin').unlink()
        with self.assertRaisesRegex(ValueError, 'no payload'):
            self.run_tool('create')

    def test_manifest_name_traversal_rejected(self):
        for name in ('../outside.json', 'sub/file.json', '..', r'sub\file.json'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.run_tool('create', name)

    def test_manifest_entry_traversal_rejected(self):
        self.run_tool('create')
        self.rewrite_manifest(lambda d: d['files'][0].update(path='../outside.bin'))
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            self.run_tool('verify')

    def test_duplicate_entry_rejected(self):
        self.run_tool('create')
        self.rewrite_manifest(lambda d: d['files'].append(dict(d['files'][0])))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.run_tool('verify')

    def test_invalid_hash_rejected(self):
        self.run_tool('create')
        self.rewrite_manifest(lambda d: d['files'][0].update(sha256='invalid'))
        with self.assertRaisesRegex(ValueError, 'Invalid size or hash'):
            self.run_tool('verify')

    def test_invalid_json_returns_nonzero(self):
        (self.root / 'manifest.json').write_text('{', encoding='utf-8')
        result = subprocess.run([sys.executable, str(SCRIPT), 'verify', str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('ERROR:', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_unreadable_directory_aborts(self):
        def denied_walk(*args, **kwargs):
            kwargs['onerror'](PermissionError('denied directory'))
            return iter(())

        with mock.patch.object(MODULE.os, 'walk', side_effect=denied_walk):
            with self.assertRaises(PermissionError):
                self.run_tool('create')
        self.assertFalse((self.root / 'manifest.json').exists())

    def test_reparse_detection(self):
        fake_info = mock.Mock(st_mode=0, st_file_attributes=0x400)
        with mock.patch.object(Path, 'lstat', return_value=fake_info):
            # Windows reparse bit is available as a stat constant on this runtime.
            self.assertTrue(MODULE.is_redirect(self.root))

    def test_symlink_rejected_when_available(self):
        link = self.root / 'linked.bin'
        try:
            link.symlink_to(self.root / 'source' / '模型 sample.bin')
        except OSError as error:
            self.skipTest(f'Symlink creation unavailable: {error}')
        with self.assertRaisesRegex(ValueError, 'Links/reparse'):
            self.run_tool('create')

    @unittest.skipUnless(os.name == 'nt', 'Windows junction test')
    def test_windows_junction_rejected(self):
        junction = self.root / 'junction'
        result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(junction),
                                 str(self.root / 'source')], capture_output=True)
        if result.returncode:
            self.skipTest('Junction creation unavailable')
        self.addCleanup(lambda: os.rmdir(junction) if junction.exists() else None)
        with self.assertRaisesRegex(ValueError, 'Links/reparse'):
            self.run_tool('create')


if __name__ == '__main__':
    unittest.main()
