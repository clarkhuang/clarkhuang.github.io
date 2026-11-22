#!/usr/bin/env python3
"""Compose a GitHub Pages artifact: production at / and next-revision at /staging/.

Usage:
  python3 compose_pages.py --prod /path/to/main/checkout --staging-src /path/to/next-revision --out /path/to/_site

Copies prebuilt static files. Does not run the generator. Excludes git metadata
and workflow files from the published tree.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

EXCLUDE_DIRS = {".git", ".github", ".venv", "node_modules", "__pycache__"}
EXCLUDE_FILES = {".gitignore", ".gitattributes"}


def copy_tree(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in EXCLUDE_DIRS or item.name in EXCLUDE_FILES:
            continue
        if item.name.startswith(".git"):
            continue
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        else:
            shutil.copy2(item, target)


def ensure_robots(prod_root: Path) -> None:
    robots = prod_root / "robots.txt"
    text = robots.read_text(encoding="utf-8") if robots.exists() else "User-agent: *\nAllow: /\n"
    if "Disallow: /staging/" not in text:
        if "User-agent: *" in text:
            text = text.replace("User-agent: *\nAllow: /", "User-agent: *\nAllow: /\nDisallow: /staging/", 1)
            if "Disallow: /staging/" not in text:
                text = "User-agent: *\nAllow: /\nDisallow: /staging/\n\n" + text
        else:
            text = "User-agent: *\nAllow: /\nDisallow: /staging/\n\n" + text
    robots.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prod", required=True, type=Path)
    ap.add_argument("--staging-src", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    if not args.prod.is_dir() or not args.staging_src.is_dir():
        sys.exit("prod and staging-src must be directories")
    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)
    copy_tree(args.prod, args.out)
    # Never ship a leftover staging tree from the production branch
    leftover = args.out / "staging"
    if leftover.exists():
        shutil.rmtree(leftover)
    ensure_robots(args.out)
    staging = args.out / "staging"
    copy_tree(args.staging_src, staging)
    if (staging / "staging").exists():
        shutil.rmtree(staging / "staging")
    here = Path(__file__).resolve().parent
    subprocess.check_call([sys.executable, str(here / "stage_site.py"), str(staging)])
    print(f"composed production + staging into {args.out}")


if __name__ == "__main__":
    main()
