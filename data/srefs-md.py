#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2026
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

"""Generate Markdown link definitions from srefs.json."""

import json
import sys

for stable_name in json.load(sys.stdin):
    print(f'[{stable_name}]: {{.sref}}')
