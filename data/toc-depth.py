#!/usr/bin/env python3

import sys
import yaml

frontmatter = next(yaml.safe_load_all(sys.stdin))
toc_depth = frontmatter.get('toc-depth')
if toc_depth is not None:
    print(toc_depth)
