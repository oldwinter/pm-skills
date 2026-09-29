"""Unit tests for validate_plugins.py plus a repo-wide validation gate."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import validate_plugins as vp


class TestFrontmatterParser(unittest.TestCase):
    def test_parses_flat_keys(self):
        fm = vp.parse_yaml_frontmatter(
            '---\ndescription: Hello world\nargument-hint: "[x]"\n---\nBody'
        )
        self.assertEqual(fm["description"], "Hello world")
        self.assertEqual(fm["argument-hint"], "[x]")

    def test_none_without_frontmatter(self):
        self.assertIsNone(vp.parse_yaml_frontmatter("# Just markdown\n"))

    def test_none_when_unterminated(self):
        self.assertIsNone(vp.parse_yaml_frontmatter("---\ndescription: x\n"))

    def test_strips_quotes(self):
        fm = vp.parse_yaml_frontmatter("---\nname: 'quoted'\n---\n")
        self.assertEqual(fm["name"], "quoted")

    def test_inline_hyphens_do_not_close_frontmatter(self):
        fm = vp.parse_yaml_frontmatter(
            "---\ndescription: Use --- safely\nargument-hint: '<x>'\n---\nBody\n"
        )
        self.assertEqual(
            fm, {"description": "Use --- safely", "argument-hint": "<x>"}
        )


class TestManifestValidation(unittest.TestCase):
    def _write_manifest(self, temp_dir, data):
        plugin = Path(temp_dir) / "plugin-a"
        manifest_dir = plugin / ".claude-plugin"
        manifest_dir.mkdir(parents=True)
        (manifest_dir / "plugin.json").write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )
        return plugin

    def test_non_string_required_fields_are_errors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            plugin = self._write_manifest(
                temp_dir,
                {
                    "name": "plugin-a",
                    "version": 100,
                    "description": ["not", "text"],
                },
            )
            result = vp.validate_manifest(str(plugin))

        self.assertIn("Required field 'version' must be a string", result.errors)
        self.assertIn(
            "Required field 'description' must be a string", result.errors
        )

    def test_utf8_manifest_under_ascii_locale(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            plugin = self._write_manifest(
                temp_dir,
                {
                    "name": "plugin-a",
                    "version": "1.0.0",
                    "description": "中文插件描述足够长",
                },
            )
            code = (
                "import validate_plugins as vp; "
                f"result = vp.validate_manifest({str(plugin)!r}); "
                "raise SystemExit(0 if result.ok else 1)"
            )
            env = os.environ.copy()
            env.update(
                {
                    "LC_ALL": "C",
                    "LANG": "C",
                    "PYTHONUTF8": "0",
                    "PYTHONCOERCECLOCALE": "0",
                }
            )
            result = subprocess.run(
                [sys.executable, "-X", "utf8=0", "-c", code],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)


class TestCommandValidation(unittest.TestCase):
    def _validate(self, body):
        with tempfile.TemporaryDirectory() as temp_dir:
            command = Path(temp_dir) / "command.md"
            command.write_text(
                "---\ndescription: Valid command description\n"
                "argument-hint: '<x>'\n---\n" + body,
                encoding="utf-8",
            )
            return vp.validate_command(str(command))

    def test_missing_argument_hint_is_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            command = Path(temp_dir) / "missing-hint.md"
            command.write_text(
                "---\ndescription: Valid command description\n---\nBody\n",
                encoding="utf-8",
            )

            result = vp.validate_command(str(command))

        self.assertIn(
            "Missing required frontmatter field: argument-hint", result.errors
        )

    def test_requires_exactly_one_arguments_placeholder(self):
        missing = self._validate("Body without command input\n")
        duplicate = self._validate("$ARGUMENTS and $ARGUMENTS\n")

        self.assertIn(
            "Command must contain exactly one $ARGUMENTS placeholder; found 0",
            missing.errors,
        )
        self.assertIn(
            "Command must contain exactly one $ARGUMENTS placeholder; found 2",
            duplicate.errors,
        )


class TestSkillValidation(unittest.TestCase):
    def test_rejects_command_argument_placeholder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir) / "sample-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: sample-skill\n"
                "description: Use when testing placeholder validation\n---\n"
                "Analyze $ARGUMENTS.\n",
                encoding="utf-8",
            )
            result = vp.validate_skill(str(skill))

        self.assertIn(
            "Skills must read conversation context and cannot contain $ARGUMENTS",
            result.errors,
        )


class TestReferenceValidation(unittest.TestCase):
    def _plugin(self, temp_dir, body):
        plugin = Path(temp_dir) / "plugin-a"
        commands = plugin / "commands"
        commands.mkdir(parents=True)
        (commands / "command.md").write_text(body, encoding="utf-8")
        return plugin

    def test_dangling_skill_reference_is_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            plugin = self._plugin(
                temp_dir, "Use the **missing-skill** skill.\n"
            )
            result = vp.validate_cross_references(str(plugin), [])

        self.assertIn(
            "Command command.md references skill 'missing-skill' not found in this plugin",
            result.errors,
        )

    def test_cross_plugin_command_reference_is_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            plugin = self._plugin(
                temp_dir, "Run /plugin-a:local, then /plugin-b:other.\n"
            )
            result = vp.validate_cross_references(str(plugin), [])

        self.assertEqual(
            result.errors,
            [
                "Command command.md hard-references another plugin: /plugin-b:other"
            ],
        )


class TestReadmeValidation(unittest.TestCase):
    def test_missing_readme_is_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = vp.validate_readme(temp_dir)

        self.assertIn("Missing README.md", result.errors)


class TestCountWords(unittest.TestCase):
    def test_excludes_frontmatter(self):
        self.assertEqual(vp.count_words("---\nname: x\n---\none two three"), 3)


class TestRepoPassesValidation(unittest.TestCase):
    """Every plugin in the repo must pass the validator with zero errors."""

    def test_all_plugins_valid(self):
        plugin_dirs = sorted(
            str(p)
            for p in ROOT.iterdir()
            if p.is_dir() and (p / ".claude-plugin").is_dir()
        )
        self.assertTrue(plugin_dirs, "no plugins found in repo root")

        failures = []
        for pd in plugin_dirs:
            results = vp.validate_plugin(pd)
            for section, value in results["sections"].items():
                items = value.values() if isinstance(value, dict) else [value]
                for vr in items:
                    for err in vr.errors:
                        failures.append(f"{results['name']}/{section}: {err}")

        self.assertEqual(
            failures, [], "validator errors:\n" + "\n".join(failures)
        )


if __name__ == "__main__":
    unittest.main()
