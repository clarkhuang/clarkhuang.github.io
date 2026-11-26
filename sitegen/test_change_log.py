"""Focused regressions for the reader-visible release notes and permanent view navigation."""
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from change_log import ROOT, VIEWS, read_releases


class ViewLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tabs = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "nav":
            self.in_tabs = attrs.get("class") == "history-tabs"
        if self.in_tabs and tag == "a":
            self.links.append((attrs["href"], attrs.get("aria-current")))

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_tabs = False


class ChangeLogTests(unittest.TestCase):
    def test_four_views_remain_in_order_on_every_entry_point(self):
        expected = [f"/change-log/{slug}/" for slug in VIEWS]
        self.assertEqual(len(expected), 4)
        for slug in ["", *VIEWS]:
            parser = ViewLinks()
            parser.feed((ROOT / "change-log" / slug / "index.html").read_text())
            self.assertEqual([url for url, _ in parser.links], expected)
            self.assertEqual([url for url, active in parser.links if active == "page"],
                             [f"/change-log/{slug or 'daily'}/"])

    def test_release_note_applies_only_when_its_content_changes_on_main(self):
        with TemporaryDirectory() as directory:
            repo = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", "-C", directory, *args], text=True)
            def commit(title):
                git("add", "-A")
                git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", title)
            git("init", "-q")
            (repo / "sitegen").mkdir()
            field = repo / "sitegen/change_log_editorial.json"
            note = {"summary": "Choose a lesson format.", "technical_summary": "Records a format preference."}
            field.write_text(json.dumps({"release_note": note}))
            commit("First")
            field.write_text(json.dumps({"release_note": note, "other": {}}))
            commit("Merge pull request #123 from fixture/unchanged")
            records = read_releases(directory, "HEAD", {}, {})
            self.assertEqual(records[0]["summary"], note["summary"])
            self.assertTrue(records[0]["editorial"])
            self.assertFalse(records[1]["editorial"])
            self.assertNotIn("123", records[1]["summary"])
            self.assertEqual(records[1]["pull_request"], 123)
