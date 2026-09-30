"""Recovery safety checks: no Docker daemon or real credentials required."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("staging", Path(__file__).with_name("staging.py"))
staging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(staging)


class RecoverySafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.bundle = Path(self.temporary.name) / "bundle"
        self.bundle.mkdir()
        (self.bundle / "secrets").mkdir()
        for name in ("deployment.env", "deployment.json", "compose.yml",
                     "secrets/master-key", "secrets/login-password"):
            (self.bundle / name).write_text("synthetic recovery placeholder")
        self.archive("profiles.json")

    def archive(self, name):
        with tarfile.open(self.bundle / "data.tar.gz", "w:gz") as archive:
            member = tarfile.TarInfo(name)
            member.size = 2
            archive.addfile(member, io.BytesIO(b"{}"))
        sums = {str(path.relative_to(self.bundle)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.bundle.rglob("*")
                if path.is_file() and path.name != "checksums.json"}
        (self.bundle / "checksums.json").write_text(json.dumps(sums))

    def test_complete_bundle_is_accepted(self):
        staging.verify_bundle(self.bundle)

    def test_changed_key_cannot_be_restored_silently(self):
        (self.bundle / "secrets/master-key").write_text("different key")
        with self.assertRaisesRegex(ValueError, "checksum"):
            staging.verify_bundle(self.bundle)

    def test_archive_cannot_escape_data_directory(self):
        self.archive("../outside-data")
        with self.assertRaisesRegex(ValueError, "Unsafe data"):
            staging.verify_bundle(self.bundle)

    def test_restore_cannot_reuse_existing_destination(self):
        with self.assertRaisesRegex(ValueError, "must not exist"):
            staging.restore(self.bundle, self.bundle, "wealthfolio-staging-restore-test", 18089)

    def test_restore_cannot_target_live_staging_project(self):
        with self.assertRaisesRegex(ValueError, "distinct"):
            staging.restore(self.bundle / "new", self.bundle, "wealthfolio-staging", 18089)

    def test_reinitialization_preserves_existing_configuration(self):
        before = (self.bundle / "deployment.env").read_bytes()
        with self.assertRaisesRegex(ValueError, "Already initialized"):
            staging.init(self.bundle, 18088)
        self.assertEqual(before, (self.bundle / "deployment.env").read_bytes())


if __name__ == "__main__":
    unittest.main()
