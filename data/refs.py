#!/usr/bin/env python3

import sys
import yaml
import json

index = yaml.safe_load(sys.stdin)
refs = index['references']

for item in refs:
  issued = item.get('issued', None)
  if issued is not None:
    issued['raw'] = str(issued.pop('year'))

json.dump(refs, sys.stdout, ensure_ascii=False, indent=2)
