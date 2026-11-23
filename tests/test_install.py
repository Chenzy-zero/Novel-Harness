import importlib.util
import tempfile
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts/install.py"
spec = importlib.util.spec_from_file_location("novel_install", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class InstallerTests(unittest.TestCase):
    def test_install_preserves_existing_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "novel"
            first, _ = module.install(target)
            self.assertTrue(first)
            self.assertTrue((target / "workflow.md").exists())
            (target / "workflow.md").write_text("author's edits", encoding="utf-8")
            second, skipped = module.install(target)
            self.assertEqual(second, [])
            self.assertIn("workflow.md", skipped)
            self.assertEqual((target / "workflow.md").read_text(encoding="utf-8"), "author's edits")

    def test_dry_run_does_not_create(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "novel"
            module.install(target, dry_run=True)
            self.assertFalse(target.exists())

if __name__ == "__main__":
    unittest.main()
