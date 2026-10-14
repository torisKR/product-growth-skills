"""Check multilingual README parity and keep runtime/privacy boundaries intact.

These checks validate document structure, links and shared commands, not native
speaker review, rendered GitHub appearance or runtime installation.
"""
from __future__ import annotations

from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import validate_skills as validator

ROOT = Path(__file__).resolve().parents[1]
LOCALES = {"ko": "한국어", "en": "English", "ja": "日本語", "zh": "简体中文", "fr": "Français"}
SECTIONS = ("overview", "skills", "quick-start", "workflow", "evidence", "structure", "validation", "safety", "contributing")
ANCHOR = re.compile(r'<a id="([a-z0-9-]+)"></a>')
BASH_BLOCK = re.compile(r"^```bash\n(.*?)^```$", re.MULTILINE | re.DOTALL)


class MultilingualDocumentationTests(unittest.TestCase):
    def scan(self, relative: str, content: str) -> list[str]:
        with tempfile.TemporaryDirectory(prefix="growth-docs-test-") as directory:
            root = Path(directory)
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            with patch.object(validator, "ROOT", root):
                return validator.scan_content()

    def guide(self, locale: str) -> tuple[Path, str]:
        path = ROOT / "docs" / locale / "README.md"
        self.assertTrue(path.is_file(), f"missing {locale} README")
        return path, path.read_text(encoding="utf-8")

    def test_root_readme_allows_native_language_navigation(self):
        self.assertEqual(self.scan("README.md", "# Product Growth Skills\n한국어 · 日本語 · 简体中文 · Français\n"), [])

    def test_five_human_document_locales_are_allowed(self):
        for locale, text in LOCALES.items():
            with self.subTest(locale=locale):
                self.assertEqual(self.scan(f"docs/{locale}/README.md", f"# {text}\n"), [])

    def test_unrecognized_locale_does_not_gain_exemption(self):
        errors = self.scan("docs/unknown/README.md", "# 日本語\n")
        self.assertTrue(any("runtime documentation must be English" in error for error in errors))

    def test_other_package_readmes_remain_runtime_documents(self):
        errors = self.scan("example/README.md", "# 日本語\n")
        self.assertTrue(any("runtime documentation must be English" in error for error in errors))

    def test_runtime_instruction_names_are_not_exempt_even_in_human_dirs(self):
        for relative in ("docs/ko/SKILL.md", "docs/ja/AGENTS.md", "docs/fr/CLAUDE.md", "local-knowledge/SKILL.md"):
            with self.subTest(path=relative):
                errors = self.scan(relative, "# 日本語\n")
                self.assertTrue(any("runtime documentation must be English" in error for error in errors))

    def test_localized_guides_retain_link_checks(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                errors = self.scan(f"docs/{locale}/README.md", "[Missing](missing.md)\n")
                self.assertTrue(any("broken local link" in error for error in errors))

    def test_localized_guides_retain_machine_path_checks(self):
        machine_path = "/Users/" + "fixture-user/private"
        for locale in LOCALES:
            with self.subTest(locale=locale):
                errors = self.scan(f"docs/{locale}/README.md", machine_path)
                self.assertTrue(any("machine-specific absolute path" in error for error in errors))

    def test_localized_guides_retain_credential_checks(self):
        fake_key = "-----BEGIN " + "PRIVATE KEY-----\n" + "A" * 64 + "\n-----END " + "PRIVATE KEY-----"
        for locale in LOCALES:
            with self.subTest(locale=locale):
                errors = self.scan(f"docs/{locale}/README.md", fake_key)
                self.assertTrue(any("credential-shaped content" in error for error in errors))

    def test_root_links_to_all_five_guides(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for locale in LOCALES:
            with self.subTest(locale=locale):
                self.assertIn(f"(docs/{locale}/README.md)", text)

    def test_all_guides_have_language_marker_and_cross_navigation(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                _, text = self.guide(locale)
                self.assertIn(f"<!-- docs-locale: {locale} -->", text)
                self.assertIn("(../../README.md)", text)
                for target in LOCALES:
                    self.assertIn(f"(../{target}/README.md)", text)

    def test_all_guides_cover_all_skills(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                _, text = self.guide(locale)
                skills = set(re.findall(r"\]\(../../([a-z0-9-]+)/SKILL\.md\)", text))
                self.assertEqual(skills, validator.EXPECTED)

    def test_sections_match_across_languages(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                _, text = self.guide(locale)
                self.assertEqual(tuple(ANCHOR.findall(text)), SECTIONS)
                for section in SECTIONS:
                    self.assertIn(f"](#{section})", text)

    def test_executable_examples_match_across_languages(self):
        _, english = self.guide("en")
        expected = BASH_BLOCK.findall(english)
        self.assertGreaterEqual(len(expected), 4)
        for locale in LOCALES:
            with self.subTest(locale=locale):
                _, text = self.guide(locale)
                self.assertEqual(BASH_BLOCK.findall(text), expected)
                self.assertIn("https://github.com/torisKR/product-growth-skills.git", text)
                self.assertNotIn("https://github.com/toris-dev/product-growth-skills.git", text)

    def test_guide_links_and_local_anchors_resolve(self):
        paths = [ROOT / "README.md"] + [self.guide(locale)[0] for locale in LOCALES]
        for path in paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertEqual(validator.local_link_errors(path), [])
                text = path.read_text(encoding="utf-8")
                for link in validator.MARKDOWN_LINK.findall(text):
                    if link.startswith(("http://", "https://", "mailto:")):
                        continue
                    target, separator, fragment = link.partition("#")
                    if separator and fragment:
                        destination = (path.parent / target).resolve() if target else path
                        self.assertTrue(destination.is_file())
                        self.assertIn(fragment, ANCHOR.findall(destination.read_text(encoding="utf-8")))

    def test_guides_keep_evidence_and_private_scope_links(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                _, text = self.guide(locale)
                for target in ("../../research/solo-developer-2026-10-15/README.md",
                               "../../research/solo-developer-2026-10-15/VERIFICATION.md",
                               "../../toris-solo-founder/references/agents-and-provenance.md",
                               "../../toris-flutter-play-store-release/README.md",
                               "../../CONTRIBUTING.md", "../../LICENSE"):
                    self.assertIn(f"]({target})", text)
                self.assertIn("local-knowledge/", text)
                self.assertIn("not_run", text)

    def test_code_fences_are_balanced(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                _, text = self.guide(locale)
                fences = [line for line in text.splitlines() if line.startswith("```")]
                self.assertEqual(len(fences) % 2, 0)
                for index in range(1, len(fences), 2):
                    self.assertEqual(fences[index], "```")


if __name__ == "__main__":
    unittest.main()
