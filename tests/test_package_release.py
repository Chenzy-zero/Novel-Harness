import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
import tarfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/package_release.py"
SPEC = importlib.util.spec_from_file_location("novel_package_release", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReleasePackageTests(unittest.TestCase):
    def test_archives_have_direct_project_root_and_no_development_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path, tar_path, sums_path = MODULE.build(Path(tmp))
            with zipfile.ZipFile(zip_path) as archive:
                zip_names = set(archive.namelist())
            with tarfile.open(tar_path, "r:gz") as archive:
                tar_names = set(archive.getnames())

            for names in (zip_names, tar_names):
                self.assertIn("AGENTS.md", names)
                self.assertIn("workflow.md", names)
                self.assertIn(".agents/skills/novel-init/SKILL.md", names)
                self.assertIn("chapters/README.md", names)
                self.assertIn(".github/ISSUE_TEMPLATE/arc.yml", names)
                self.assertIn("VERSION", names)
                self.assertIn("CHANGELOG.md", names)
                self.assertFalse(any(name.startswith("scaffold/") for name in names))
                self.assertFalse(any("tests/" in name for name in names))
                self.assertNotIn("scripts/install.py", names)
                self.assertNotIn("scripts/package_release.py", names)

            checksums = sums_path.read_text(encoding="ascii")
            self.assertIn(hashlib.sha256(zip_path.read_bytes()).hexdigest(), checksums)
            self.assertIn(hashlib.sha256(tar_path.read_bytes()).hexdigest(), checksums)

            with tempfile.TemporaryDirectory() as extracted:
                with zipfile.ZipFile(zip_path) as archive:
                    archive.extractall(extracted)
                skill = Path(extracted) / ".agents/skills/novel-init/SKILL.md"
                self.assertIn("name: novel-init", skill.read_text(encoding="utf-8"))
                self.assertFalse((Path(extracted) / "scripts/install.py").exists())
                result = subprocess.run(
                    [sys.executable, str(Path(extracted) / "scripts/validate_novel.py"), "--mode", "structure"],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("PASS: structure", result.stdout)

    def test_archives_are_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            a_zip, a_tar, _ = MODULE.build(first)
            b_zip, b_tar, _ = MODULE.build(second)
            self.assertEqual(a_zip.read_bytes(), b_zip.read_bytes())
            self.assertEqual(a_tar.read_bytes(), b_tar.read_bytes())

    def test_rejects_invalid_version(self):
        with self.assertRaises(ValueError):
            MODULE.read_version("latest")


if __name__ == "__main__":
    unittest.main()
