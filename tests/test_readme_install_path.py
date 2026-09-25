"""README install CTA must send people to this Chinese fork first."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")


def _section(heading: str) -> str:
    marker = f"## {heading}"
    start = README.index(marker)
    rest = README[start + len(marker) :]
    nxt = re.search(r"\n## ", rest)
    return rest if nxt is None else rest[: nxt.start()]


class TestReadmeInstallPath(unittest.TestCase):
    def test_start_here_requires_this_fork(self):
        start = _section("Start Here")
        self.assertIn("oldwinter/pm-skills", start)
        self.assertIn("Installation", start)

    def test_installation_primary_commands_use_fork(self):
        install = _section("Installation")
        primary = install.split("### English upstream", 1)[0]
        self.assertIn("claude plugin marketplace add oldwinter/pm-skills", primary)
        self.assertIn("codex plugin marketplace add oldwinter/pm-skills", primary)
        self.assertIn("Enter: `oldwinter/pm-skills`", primary)
        self.assertNotIn("marketplace add phuryn/pm-skills", primary)
        self.assertNotIn("Enter: `phuryn/pm-skills`", primary)

    def test_upstream_is_secondary_option(self):
        install = _section("Installation")
        self.assertIn("### English upstream", install)
        fork = install.index("marketplace add oldwinter/pm-skills")
        upstream = install.index("marketplace add phuryn/pm-skills")
        self.assertLess(fork, upstream)


if __name__ == "__main__":
    unittest.main()
