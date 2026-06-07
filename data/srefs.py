#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2026
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

"""Extract stable names from eel.is/c++draft."""

from bs4 import BeautifulSoup
import json
import re
import signal
import subprocess
import sys

url = 'https://eel.is/c++draft'

def rows(html):
    def normalize(text):
        text = text.replace('\N{ZERO WIDTH SPACE}', '')
        return re.sub(r'\s+', ' ', text).strip()

    soup = BeautifulSoup(html, 'html.parser')
    for heading in soup.select('h1,h2,h3,h4,h5,h6'):
        div = heading.find_parent('div', id=True)
        number = heading.select_one('.annexnum,.secnum')
        if div is None or number is None:
            continue

        number = normalize(number.get_text())
        for elem in heading.select(
                '.annexnum,.secnum,.abbr_ref,.folded_abbr_ref,.unfolded_abbr_ref'):
            elem.decompose()

        title = normalize(heading.get_text())
        yield div['id'], number, title

def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    html = subprocess.check_output(['curl', '-fsSL', url], text=True)
    json.dump({stable_name: [number, title]
               for stable_name, number, title in rows(html)},
              sys.stdout,
              separators=(',', ':'))
    print()

if __name__ == '__main__':
    main()
