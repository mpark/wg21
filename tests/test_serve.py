#!/usr/bin/env python3

import os
import sys
import unittest
import warnings
from pathlib import Path
from unittest import mock

from tornado.testing import AsyncHTTPTestCase, ExpectLog
from tornado.web import Application

sys.path.insert(0, str(Path(__file__).parents[1] / 'data'))

from serve import PaperServer, serve_targets


class ServeTest(unittest.TestCase):
    @mock.patch('serve.subprocess.run')
    def test_ignores_continued_commands(self, run):
        run.return_value.stdout = (
            'pandoc input.md \\\n'
            '  -o ignored.html; \\\n'
            'pandoc input.md -o generated/paper.html\n'
            'pandoc input.md -o generated/paper.pdf\n')
        self.assertEqual(
            serve_targets('generated', ['make']),
            ['paper.html', 'paper.pdf'])

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
        server = PaperServer(['citations.html'])
        server.root = str(Path(__file__).parent / 'expected')
        return Application(server.get_web_handlers(b''))

    def test_only_selected_target_is_served(self):
        response = self.fetch('/', follow_redirects=False)
        self.assertEqual(response.code, 302)
        self.assertEqual(response.headers['Location'], '/citations.html')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            self.assertEqual(self.fetch('/citations.html').code, 200)
        with ExpectLog('tornado.access', '404 GET'):
            self.assertEqual(self.fetch('/code_blocks.html').code, 404)


if __name__ == '__main__':
    unittest.main()
