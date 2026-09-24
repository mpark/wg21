#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2026-Present
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

import argparse
import subprocess

from livereload import Server


parser = argparse.ArgumentParser(description='Build and live-reload WG21 papers')
parser.add_argument('--host', required=True)
parser.add_argument('--port', type=int, required=True)
parser.add_argument('--root', required=True)
parser.add_argument('--watch', nargs='*', default=[])
parser.add_argument('make_cmd', nargs='+')
args = parser.parse_args()


def rebuild():
    return subprocess.run(args.make_cmd)


rebuild().check_returncode()

server = Server()
for path in args.watch:
    server.watch(path, rebuild)
server.serve(host=args.host, port=args.port, root=args.root)
