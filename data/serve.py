#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2026-Present
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

import argparse
import re
import shlex
import subprocess
from html import escape
from pathlib import Path
from urllib.parse import quote

from livereload import Server
from tornado.web import RequestHandler

INDEX_HTML_TEMPLATE = '''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MPark/WG21 Live Server</title>
<style>
:root { color-scheme: light dark; }
body {
  max-width: 60rem;
  margin: 5em auto;
  padding: 0 1.5rem;
  font-family: serif;
  line-height: 1.35;
}
h1 { text-align: center; }
a { color: #4183c4; text-decoration: none; }
li { margin: .6em 0; }
li::marker { content: "—  "; }
@media (prefers-color-scheme: dark) {
  body { background: #171717; color: #e0e0e0; }
  a { color: #74bdff; }
}
</style>
</head>
<body>
<h1>MPark/WG21 Live Server</h1>
<ul>$papers$</ul>
</body>
</html>'''


def serve_targets(root, make_cmd):
    """Discover served artifacts without depending on a particular Make layout.

    Both the framework's generated rules and downstream handwritten rules
    eventually invoke Pandoc, so its output arguments are the shared contract.
    A forced dry run includes those commands even when the files are up to date.
    """
    result = subprocess.run(
        [*make_cmd, '-Bn'], check=True, stdout=subprocess.PIPE, text=True)

    root = Path(root).resolve()
    targets = set()
    for line in result.stdout.splitlines():
        if not line.startswith('pandoc ') or line.rstrip().endswith('\\'):
            continue
        tokens = shlex.split(line)
        if '-o' not in tokens:
            continue
        target = Path(tokens[tokens.index('-o') + 1]).resolve()
        if target.suffix in ('.html', '.pdf') and root in target.parents:
            # Only advertise files that the configured static root can serve.
            targets.add(target.relative_to(root).as_posix())
    return sorted(targets)


class RootHandler(RequestHandler):
    """Redirect to one artifact or list multiple artifacts."""

    def initialize(self, targets):
        self.targets = targets

    def get(self):
        if len(self.targets) == 1:
            self.redirect(f'/{quote(self.targets[0])}')
            return
        links = ''.join(
            f'<li><a href="/{quote(target)}">/{escape(target)}</a></li>'
            for target in self.targets)
        self.write(INDEX_HTML_TEMPLATE.replace('$papers$', links))


class PaperServer(Server):
    """Add a root page for the artifacts selected by Make."""

    def __init__(self, targets):
        super().__init__()
        self.targets = targets

    def get_web_handlers(self, script):
        handlers = [
            (rf'/({re.escape(quote(target))})', self.SFH, {'path': self.root})
            for target in self.targets
        ]
        if not self.targets:
            return handlers
        return [(r'/', RootHandler, {'targets': self.targets}), *handlers]


def main():
    parser = argparse.ArgumentParser(description='Build and live-reload WG21 papers')
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--root', required=True)
    parser.add_argument('--watch', nargs='*', default=[])
    parser.add_argument('make_cmd', nargs='+')
    args = parser.parse_args()

    def rebuild():
        return subprocess.run(args.make_cmd)

    # Do not start a server whose initial artifact failed to build. Later
    # rebuild failures remain recoverable while the watcher keeps running.
    rebuild().check_returncode()
    targets = serve_targets(args.root, args.make_cmd)

    server = PaperServer(targets)
    for path in args.watch:
        server.watch(path, rebuild)
    server.serve(
        host=args.host,
        port=args.port,
        root=args.root,
        live_css=False,
        default_filename=None)


if __name__ == '__main__':
    main()
