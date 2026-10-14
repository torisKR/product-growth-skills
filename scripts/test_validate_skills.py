"""Regression tests for the founder skill and localized human documentation.

Run with PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts
-p 'test_validate_skills.py'. Temporary fixtures stay outside the checkout.
These are structural tests, not independent agent-behavior evaluations.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_skills as validator


class DocumentationValidationTests(unittest.TestCase):
    def scan(self, relative: str, content: str) -> list[str]:
        with tempfile.TemporaryDirectory(prefix="growth-skills-test-") as directory:
            root = Path(directory)
            document = root / relative
            document.parent.mkdir(parents=True, exist_ok=True)
            document.write_text(content, encoding="utf-8")
            with patch.object(validator, "ROOT", root):
                return validator.scan_content()

    def test_founder_skill_is_registered(self) -> None:
        self.assertIn("toris-solo-founder", validator.EXPECTED)

    def test_founder_skill_satisfies_existing_contract(self) -> None:
        self.assertEqual(validator.validate_skill("toris-solo-founder"), [])

    def test_korean_human_guide_is_allowed(self) -> None:
        self.assertEqual(self.scan("docs/ko/guide.md", "# \ud55c\uad6d\uc5b4 \uc548\ub0b4\uc11c\n"), [])

    def test_korean_private_knowledge_is_allowed(self) -> None:
        self.assertEqual(self.scan("local-knowledge/torisKR/decisions.md", "# \uacb0\uc815 \uae30\ub85d\n"), [])

    def test_runtime_documentation_remains_english(self) -> None:
        errors = self.scan("example/SKILL.md", "# \ud55c\uad6d\uc5b4\n")
        self.assertTrue(any("runtime documentation must be English" in error for error in errors))

    def test_unrelated_docs_do_not_gain_language_exemption(self) -> None:
        errors = self.scan("docs/runtime.md", "# \ud55c\uad6d\uc5b4\n")
        self.assertTrue(any("runtime documentation must be English" in error for error in errors))

    def test_human_docs_still_check_links(self) -> None:
        errors = self.scan("docs/ko/guide.md", "# \uc548\ub0b4\n[Missing](missing.md)\n")
        self.assertTrue(any("broken local link" in error for error in errors))

    def test_private_docs_still_reject_machine_paths(self) -> None:
        machine_path = "/Users/" + "fixture-user/private-file"
        errors = self.scan("local-knowledge/torisKR/sources.md", machine_path)
        self.assertTrue(any("machine-specific absolute path" in error for error in errors))

    def test_private_docs_still_reject_credentials(self) -> None:
        fake_key = "-----BEGIN " + "PRIVATE KEY-----\n" + "A" * 64 + "\n-----END " + "PRIVATE KEY-----"
        errors = self.scan("local-knowledge/torisKR/sources.md", fake_key)
        self.assertTrue(any("credential-shaped content" in error for error in errors))

    def test_all_requested_tools_have_provenance_coverage(self) -> None:
        path = validator.ROOT / "toris-solo-founder/references/agents-and-provenance.md"
        self.assertTrue(path.is_file(), "Agent provenance reference is missing")
        content = path.read_text(encoding="utf-8")
        for name in ("Codex", "OpenCodex", "Hermes", "Grok", "agy", "Claude"):
            with self.subTest(tool=name):
                self.assertIn(name, content)
        self.assertIn("not inspected", content)
        self.assertIn("OpenCode", content)


if __name__ == "__main__":
    unittest.main()
