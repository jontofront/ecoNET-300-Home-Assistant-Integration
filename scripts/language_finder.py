#!/usr/bin/env python3
"""Optimized Language Finder - Discover available languages in ecoNET files.

Combines fast discovery with comprehensive extraction capabilities.
"""

import json
from pathlib import Path
import re


def safe_read_file(file_path: Path, max_size: int | None = None) -> str | None:
    """Safely read file content with optional size limit."""
    try:
        if max_size:
            return file_path.read_text(encoding="utf-8")[:max_size]
        return file_path.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return None


def find_languages_fast(js_dir: Path, max_read_size: int = 100000) -> set[str]:
    """Fast language discovery by reading only the beginning of files."""
    languages: set[str] = set()

    # Get all JS files first
    js_files = list(js_dir.glob("*.js"))

    for js_file in js_files:
        content = safe_read_file(js_file, max_read_size)
        if content is None:
            continue

        # Find all language codes in this sample
        pattern = r'trans\["([^"]+)"\]'
        matches = re.findall(pattern, content)

        for lang in matches:
            languages.add(lang)

    return languages


def find_languages_comprehensive(js_dir: Path) -> set[str]:
    """Comprehensive language discovery by reading entire files."""
    languages: set[str] = set()

    # Get all JS files first
    js_files = list(js_dir.glob("*.js"))

    for js_file in js_files:
        content = safe_read_file(js_file)
        if content is None:
            continue

        # Find all language codes
        pattern = r'trans\["([^"]+)"\]'
        matches = re.findall(pattern, content)

        for lang in matches:
            languages.add(lang)

    return languages


def analyze_language_coverage(js_dir: Path, languages: set[str]) -> dict[str, dict]:
    """Analyze coverage and quality of each language."""
    coverage: dict[str, dict] = {}

    # Initialize coverage structure
    for lang in languages:
        coverage[lang] = {
            "files_found_in": [],
            "total_translations": 0,
            "sample_translations": [],
        }

    # Get all JS files once
    js_files = list(js_dir.glob("*.js"))

    # Process each file once for all languages
    for js_file in js_files:
        content = safe_read_file(js_file)
        if content is None:
            continue

        # Check all languages in this file
        for lang in languages:
            pattern = rf'trans\["{re.escape(lang)}"\]\s*=\s*\{{([^}}]+(?:\{{[^}}]*\}}[^}}]*)*)\}}'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                coverage[lang]["files_found_in"].append(js_file.name)

                # Count translations (rough estimate)
                lang_content = match.group(1)
                translation_count = len(
                    re.findall(r'"([^"]+)"\s*:\s*"[^"]*"', lang_content)
                )
                coverage[lang]["total_translations"] += translation_count

                # Sample a few translations
                if not coverage[lang]["sample_translations"]:
                    sample_matches = re.findall(
                        r'"([^"]+)"\s*:\s*"[^"]*"', lang_content
                    )
                    coverage[lang]["sample_translations"] = sample_matches[:3]

    return coverage


def save_language_report(
    languages: set[str], coverage: dict[str, dict], output_dir: Path
) -> None:
    """Save comprehensive language report."""
    # Save simple language list
    languages_file = output_dir / "available_languages.txt"
    languages_file.write_text(
        "Available Languages in ecoNET Files:\n"
        + "=" * 40
        + "\n\n"
        + "\n".join(f"- {lang}" for lang in sorted(languages)),
        encoding="utf-8",
    )

    # Save detailed coverage report
    coverage_file = output_dir / "language_coverage_report.json"
    coverage_file.write_text(
        json.dumps(coverage, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Save markdown report
    markdown_content = [
        "# ecoNET Language Coverage Report\n\n",
        f"**Total Languages Found:** {len(languages)}\n\n",
    ]

    for lang in sorted(languages):
        lang_data = coverage[lang]
        markdown_content.extend(
            [
                f"## {lang.upper()}\n\n",
                f"- **Files Found In:** {', '.join(lang_data['files_found_in'])}\n",
                f"- **Total Translations:** {lang_data['total_translations']}\n",
            ]
        )

        if lang_data["sample_translations"]:
            markdown_content.append("- **Sample Translations:**\n")
            for key, value in lang_data["sample_translations"]:
                markdown_content.append(f'  - `{key}`: "{value}"\n')
        markdown_content.append("\n")

    markdown_file = output_dir / "language_coverage_report.md"
    markdown_file.write_text("".join(markdown_content), encoding="utf-8")


def main() -> None:
    """Execute main function with multiple discovery modes."""
    js_dir = Path("docs/cloud_translations/js_files")
    output_dir = Path("docs/cloud_translations")

    if not js_dir.exists():
        return

    # Fast discovery first
    fast_languages = find_languages_fast(js_dir)

    # Comprehensive discovery
    comprehensive_languages = find_languages_comprehensive(js_dir)

    # Combine results
    all_languages = fast_languages | comprehensive_languages

    # Analyze coverage
    coverage = analyze_language_coverage(js_dir, all_languages)

    # Save reports
    save_language_report(all_languages, coverage, output_dir)


if __name__ == "__main__":
    main()
