#!/usr/bin/env python3
"""Generate docs/CATALOG.md from skill, agent, and rule frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- Frontmatter parsing ---

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)

STOP_PATTERNS = re.compile(
    r"^\s*(Use when\b|Use before\b|Use this\b|Use proactively\b|Recognizes?:|Triggers?:|Usage:|Optional:|Cancel:|Activate when:)",
    re.IGNORECASE | re.MULTILINE,
)

YAML_KEY_RE = re.compile(r"^(\w[\w-]*)\s*:\s*(.*)")


def parse_frontmatter(filepath: Path) -> dict[str, str] | None:
    """Extract YAML frontmatter as a flat dict. Returns None if absent."""
    text = filepath.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    raw = m.group(1)
    return _parse_yaml_flat(raw)


def _parse_yaml_flat(raw: str) -> dict[str, str]:
    """Minimal parser for flat YAML with optional multiline '|' strings."""
    result: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    is_multiline = False

    for line in raw.split("\n"):
        # New key?
        key_match = YAML_KEY_RE.match(line)
        if key_match and not (is_multiline and line.startswith(" ")):
            # Flush previous key
            if current_key is not None:
                result[current_key] = _flush(current_lines)
            current_key = key_match.group(1)
            value = key_match.group(2).strip()
            if value == "|":
                is_multiline = True
                current_lines = []
            else:
                is_multiline = False
                # Strip surrounding quotes and unescape
                if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
                    value = value[1:-1]
                    # Handle double-escaped \\n before single \n
                    value = (
                        value.replace("\\\\n", "\n")
                        .replace("\\n", "\n")
                        .replace('\\\\"', '"')
                        .replace('\\"', '"')
                    )
                current_lines = [value]
        elif is_multiline and current_key is not None:
            current_lines.append(line.strip())
        # else: continuation of non-multiline or blank

    if current_key is not None:
        result[current_key] = _flush(current_lines)

    return result


def _flush(lines: list[str]) -> str:
    return "\n".join(lines).strip()


def extract_catalog_description(raw_description: str) -> str:
    """Extract the catalog-worthy portion: everything before trigger keywords."""
    m = STOP_PATTERNS.search(raw_description)
    if m:
        raw_description = raw_description[: m.start()]
    # Join lines, collapse whitespace
    desc = " ".join(raw_description.split()).strip()
    if desc and not desc.endswith("."):
        desc += "."
    return desc


# --- Discovery ---

SKILL_CATEGORY_ORDER = [
    "meta",
    "build/backend",
    "build/frontend",
    "workflow",
    "patterns",
]

SKILL_CATEGORY_DISPLAY = {
    "meta": "Meta",
    "build/backend": "Build \u2014 Backend",
    "build/frontend": "Build \u2014 Frontend",
    "workflow": "Workflow",
    "patterns": "Patterns",
}


def discover_rules() -> list[dict[str, str]]:
    rules_dir = REPO_ROOT / "rules"
    entries = []
    for f in sorted(rules_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or "name" not in fm:
            print(f"WARNING: {f} has no frontmatter, skipping", file=sys.stderr)
            continue
        entries.append({
            "name": fm["name"],
            "description": extract_catalog_description(fm.get("description", "")),
            "path": f"../rules/{f.name}",
        })
    return entries


def _skill_category(skill_path: Path) -> str:
    """Derive category key from path like skills/build/backend/foo/SKILL.md."""
    rel = skill_path.relative_to(REPO_ROOT / "skills")
    parts = rel.parts[:-2]  # drop skill-name/SKILL.md
    return "/".join(parts)


def discover_skills() -> dict[str, list[dict[str, str]]]:
    skills_dir = REPO_ROOT / "skills"
    by_category: dict[str, list[dict[str, str]]] = {}

    for f in sorted(skills_dir.rglob("SKILL.md")):
        fm = parse_frontmatter(f)
        if not fm or "name" not in fm:
            print(f"WARNING: {f} has no frontmatter, skipping", file=sys.stderr)
            continue
        cat = _skill_category(f)
        rel_path = f.relative_to(REPO_ROOT)
        by_category.setdefault(cat, []).append({
            "name": fm["name"],
            "description": extract_catalog_description(fm.get("description", "")),
            "path": f"../{rel_path}",
        })

    return by_category


def discover_agents() -> list[dict[str, str]]:
    agents_dir = REPO_ROOT / "agents"
    entries = []
    for f in sorted(agents_dir.rglob("*.md")):
        # Skip archive, reference files, READMEs
        if "_archive" in f.parts:
            continue
        if f.stem.endswith("-reference") or f.name == "README.md":
            continue
        fm = parse_frontmatter(f)
        if not fm or "name" not in fm:
            continue
        # Category from parent directory name
        category = f.parent.name.title()
        rel_path = f.relative_to(REPO_ROOT)
        entries.append({
            "name": fm["name"],
            "description": extract_catalog_description(fm.get("description", "")),
            "category": category,
            "path": f"../{rel_path}",
        })
    return entries


def discover_custom_skills() -> list[dict[str, str]]:
    custom_dir = REPO_ROOT / "custom" / "skills"
    if not custom_dir.exists():
        return []
    entries = []
    for f in sorted(custom_dir.rglob("SKILL.md")):
        fm = parse_frontmatter(f)
        if not fm or "name" not in fm:
            continue
        rel_path = f.relative_to(REPO_ROOT)
        entries.append({
            "name": fm["name"],
            "description": extract_catalog_description(fm.get("description", "")),
            "path": f"../{rel_path}",
        })
    return entries


def discover_custom_agents() -> list[dict[str, str]]:
    custom_dir = REPO_ROOT / "custom" / "agents"
    if not custom_dir.exists():
        return []
    entries = []
    for f in sorted(custom_dir.rglob("*.md")):
        if f.name == "README.md":
            continue
        fm = parse_frontmatter(f)
        if not fm or "name" not in fm:
            continue
        rel_path = f.relative_to(REPO_ROOT)
        entries.append({
            "name": fm["name"],
            "description": extract_catalog_description(fm.get("description", "")),
            "path": f"../{rel_path}",
        })
    return entries


# --- Rendering ---


def render_catalog() -> str:
    rules = discover_rules()
    skills_by_cat = discover_skills()
    agents = discover_agents()
    custom_skills = discover_custom_skills()
    custom_agents = discover_custom_agents()

    total_skills = sum(len(v) for v in skills_by_cat.values())

    lines: list[str] = []

    # Header
    lines.append("<!-- AUTO-GENERATED by scripts/generate-catalog.py \u2014 do not edit manually -->")
    lines.append("")
    lines.append("# Skill Library \u2014 Catalog")
    lines.append("")
    lines.append("> [README](../README.md) | **CATALOG** | [SKILLS-EXPLAINED](SKILLS-EXPLAINED.md) | [ARTICLE](ARTICLE.md)")
    lines.append("")
    lines.append("> [!TIP]")
    lines.append("> To install any skill or agent below, see [Quickstart](../README.md#quickstart) in the README.")
    lines.append("")

    # Rules
    lines.append(f"## Rules ({len(rules)})")
    lines.append("")
    lines.append("*Always loaded \u2014 shape every interaction.*")
    lines.append("")
    lines.append("| Name | Description |")
    lines.append("|------|------------|")
    for r in rules:
        lines.append(f"| [{r['name']}]({r['path']}) | {r['description']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Skills
    lines.append(f"## Skills ({total_skills})")
    lines.append("")
    lines.append("*Load on demand \u2014 teach Claude specialized workflows.*")
    lines.append("")

    for cat_key in SKILL_CATEGORY_ORDER:
        cat_skills = skills_by_cat.get(cat_key, [])
        if not cat_skills:
            continue
        display = SKILL_CATEGORY_DISPLAY.get(cat_key, cat_key.title())
        lines.append(f"### {display} ({len(cat_skills)})")
        lines.append("")
        lines.append("| Name | Description |")
        lines.append("|------|------------|")
        for s in cat_skills:
            lines.append(f"| [{s['name']}]({s['path']}) | {s['description']} |")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Agents
    lines.append(f"## Agents ({len(agents)})")
    lines.append("")
    lines.append("*Isolated subprocesses \u2014 zero parent context in, result out.*")
    lines.append("")
    lines.append("| Name | Category | Description |")
    lines.append("|------|----------|------------|")
    for a in agents:
        lines.append(f"| [{a['name']}]({a['path']}) | {a['category']} | {a['description']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Custom
    lines.append("## Custom")
    lines.append("")
    if custom_skills or custom_agents:
        if custom_skills:
            lines.append(f"### Custom Skills ({len(custom_skills)})")
            lines.append("")
            lines.append("| Name | Description |")
            lines.append("|------|------------|")
            for s in custom_skills:
                lines.append(f"| [{s['name']}]({s['path']}) | {s['description']} |")
            lines.append("")
        if custom_agents:
            lines.append(f"### Custom Agents ({len(custom_agents)})")
            lines.append("")
            lines.append("| Name | Description |")
            lines.append("|------|------------|")
            for a in custom_agents:
                lines.append(f"| [{a['name']}]({a['path']}) | {a['description']} |")
            lines.append("")
    else:
        lines.append("*Your project-specific skills and agents \u2014 not tracked by upstream. See [custom/README.md](../custom/README.md) to get started.*")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    check_mode = "--check" in sys.argv

    catalog = render_catalog()
    output_path = REPO_ROOT / "docs" / "CATALOG.md"

    if check_mode:
        try:
            existing = output_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print("ERROR: docs/CATALOG.md does not exist.", file=sys.stderr)
            sys.exit(1)
        if existing == catalog:
            print("CATALOG.md is up to date.")
            sys.exit(0)
        else:
            print(
                "ERROR: CATALOG.md is out of date. "
                "Run 'python3 scripts/generate-catalog.py' and commit.",
                file=sys.stderr,
            )
            sys.exit(1)

    output_path.write_text(catalog, encoding="utf-8")
    print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
