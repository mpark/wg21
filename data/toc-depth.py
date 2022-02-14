#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2022
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

import sys
import yaml

frontmatter = next(yaml.safe_load_all(sys.stdin))
toc_depth = frontmatter.get('toc-depth')
if toc_depth is not None:
    print(toc_depth)
