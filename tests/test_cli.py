import unittest
import subprocess
import sys
from screenshot_cleaner import cli

class SmokeTests(unittest.TestCase):
    def test_help(self):
        r = subprocess.run([sys.executable, '-m', 'screenshot_cleaner', '--help'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('usage:', r.stdout)

import tempfile
from pathlib import Path
class OrganizerTests(unittest.TestCase):
    def test_move_and_collision(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); src=root/'Screenshot test.png'; src.write_bytes(b'original')
            moves=cli.plan(root,'extension'); self.assertEqual(len(moves),1)
            cli.apply_moves(moves); self.assertFalse(src.exists())
            src.write_bytes(b'new')
            with self.assertRaises(ValueError): cli.apply_moves(cli.plan(root,'extension'))
            self.assertEqual((root/'png'/src.name).read_bytes(),b'original')

