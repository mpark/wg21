#!/usr/bin/env python3

import os
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock

from tornado.testing import AsyncHTTPTestCase, ExpectLog
from tornado.web import Application
from livereload.server import LiveScriptInjector

sys.path.insert(0, str(Path(__file__).parents[1] / 'data'))

from serve import PaperServer, serve_targets


RELOAD_SCRIPT = b'<script>reload</script>'


class ReloadScriptInjector(LiveScriptInjector):
    script = RELOAD_SCRIPT


class ServeTest(unittest.TestCase):
    @mock.patch('serve.subprocess.run')
    def test_output_options(self, run):
        run.return_value.stdout = (
            'pandoc input.md -o generated/short.html\n'
            'pandoc input.md --output generated/long.html\n'
            'pandoc input.md --output=generated/equals.pdf\n')
        self.assertEqual(
            serve_targets('generated', ['make']),
            ['equals.pdf', 'long.html', 'short.html'])

    @mock.patch('serve.subprocess.run')
    def test_continued_command(self, run):
        run.return_value.stdout = (
            'pandoc input.md \\\n'
            '  --standalone \\\n'
            '  --output=generated/paper.html\n')
        self.assertEqual(
            serve_targets('generated', ['make']),
            ['paper.html'])

    def test_legacy_direct_rule_as_default_goal(self):
        directory = Path(__file__).parent / 'paper' / 'p2806'
        previous = Path.cwd()
        try:
            os.chdir(directory)
            self.assertEqual(
                serve_targets('.', ['make', 'LEGACY=1']),
                ['p2806r4.html'])
        finally:
            os.chdir(previous)


class PaperServerTest(AsyncHTTPTestCase):
    def get_app(self):
        self.directory = tempfile.TemporaryDirectory()
        html = b'<html><head>' + b' ' * (64 * 1024) + b'</head></html>'
        Path(self.directory.name, 'citations.html').write_bytes(html)

        server = PaperServer(['citations.html'])
        server.root = self.directory.name
        return Application(
            server.get_web_handlers(RELOAD_SCRIPT),
            transforms=[ReloadScriptInjector])

    def tearDown(self):
        super().tearDown()
        self.directory.cleanup()

    def test_only_selected_target_is_served(self):
        response = self.fetch('/', follow_redirects=False)
        self.assertEqual(response.code, 302)
        self.assertEqual(response.headers['Location'], '/citations.html')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            self.assertEqual(self.fetch('/citations.html').code, 200)
        with ExpectLog('tornado.access', '404 GET'):
            self.assertEqual(self.fetch('/code_blocks.html').code, 404)

    def test_livereload_is_injected_after_a_large_head(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            response = self.fetch('/citations.html')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.count(RELOAD_SCRIPT), 1)


if __name__ == '__main__':
    unittest.main()
