"""Add release links after staging URL rewriting, using the built Pages content."""
import argparse
import filecmp
from html import escape
from pathlib import Path
from urllib.parse import quote

# Compare the two builds before staging gains its URL prefix, banner and robots policy.
# Build tooling and the separately deployed Reader backend are outside the Pages UI.
EXCLUDED = {".git", ".github", ".venv", "node_modules", "__pycache__", "integrations",
            "scripts", "sitegen", "staging"}
ANCHOR = '<div class="footer-fine">'


def public_files(root):
    result = set()
    for directory, dirs, files in root.walk():
        dirs[:] = [d for d in dirs if d not in EXCLUDED]
        for name in files:
            if not name.startswith(".git") and not name.endswith(".pyc"):
                result.add((directory / name).relative_to(root))
    return result


def has_preview_changes(prod, stage):
    # The first rollout adds the footer on staging before production has it.
    if (prod / "sitegen/release_footer.py").exists() != (stage / "sitegen/release_footer.py").exists():
        return True
    files = public_files(prod)
    return files != public_files(stage) or any(
        not filecmp.cmp(prod / f, stage / f, shallow=False) for f in files
    )


def page_url(relative, root, prefix):
    if not (root / relative).is_file() or relative.name == "404.html":
        return prefix
    return prefix + quote(relative.as_posix().removesuffix("index.html") if relative.name == "index.html"
                          else relative.as_posix())


def render(prod, stage, output, preview):
    changed = has_preview_changes(prod, stage)
    source = stage if preview else prod
    for relative in public_files(source):
        if relative.suffix != ".html":
            continue
        page = output / relative
        html = page.read_text()
        if ANCHOR not in html:
            continue  # Redirect stubs have no site footer.
        stable = 'Production <span class="badge">Stable</span>'
        staging = 'Staging preview'
        if changed:
            staging += ' <span class="badge soon">Upcoming</span>'
        else:
            staging += ' (matches production)'
        if preview:
            stable = f'<a href="{escape(page_url(relative, prod, "/"))}">{stable}</a>'
        else:
            staging = f'<a href="{escape(page_url(relative, stage, "/staging/"))}">{staging}</a>'
        nav = f'<nav aria-label="Site version">{stable} · {staging}</nav>'
        page.write_text(html.replace(ANCHOR, ANCHOR + "\n        " + nav, 1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("prod", "stage", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    render(args.prod, args.stage, args.output, args.preview)
