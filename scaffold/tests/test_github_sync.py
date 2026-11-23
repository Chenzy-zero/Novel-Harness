import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "scripts/github_sync.py"
spec = importlib.util.spec_from_file_location("github_sync", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class GithubSyncTests(unittest.TestCase):
    def test_stable_id_matching(self):
        with patch.object(mod, "pages", return_value=[
            {"number": 4, "body": "<!-- novel-id: ARC-001 -->", "title": "Arc"},
            {"number": 5, "body": "", "title": "PR", "pull_request": {}}
        ]):
            index = mod.issue_index("owner/repo", "token")
        self.assertEqual(list(index), ["ARC-001"])

    def test_duplicate_remote_ids_fail(self):
        with patch.object(mod, "pages", return_value=[
            {"number": 1, "body": "<!-- novel-id: CHAR-1 -->"},
            {"number": 2, "body": "<!-- novel-id: CHAR-1 -->"}
        ]):
            with self.assertRaises(RuntimeError):
                mod.issue_index("owner/repo", "token")

    def test_bootstrap_idempotent(self):
        with patch.object(mod, "pages", return_value=[
            {"name": "novel:" + k.lower()} for k in mod.KINDS
        ]), patch.object(mod, "api") as api:
            mod.labels("owner/repo", "token")
            api.assert_not_called()

    def test_sync_no_duplicate_create(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "manifest.json"
            path.write_text('[{"id":"ARC-001","title":"First","path":"workflow.md"}]', encoding="utf-8")
            body = mod.MARKER.format("ARC-001") + "\n\nCanonical document: `workflow.md`\n\n"
            with patch.object(mod, "issue_index", return_value={
                "ARC-001": {"number": 2, "title": "First", "body": body}
            }), patch.object(mod, "api") as api:
                mod.sync("owner/repo", "token", path)
                api.assert_not_called()

if __name__ == "__main__":
    unittest.main()
