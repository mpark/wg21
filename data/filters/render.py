#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2026
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

"""
Render Markdown examples as source/output tables.

Usage:

  Single example, yields a single-column table.
  "Markdown Source" on the top, "Rendered Output" on the bottom.

  ```render
  Modify section [format.functions]{.sref}
  ```

  Multiple examples, yields a two-column table.
  "Markdown Source" on the left, "Rendered Output" on the right.
  Each inline code and code block become the rows.

  ::: render
  `` `auto x = 42;`{.cpp}``

  ``````
  ```cpp
  int main() {
    return 0;
  }
  ```
  ``````
  :::

Run this as a Markdown-to-Markdown prepass. The rendered side is emitted as raw
Markdown so the normal MPark/WG21 pipeline can process framework constructs.
"""

import datetime

import panflute as pf

from wg21 import slide_title_box


def title_slide_preview(text):
    doc = pf.convert_text(text, standalone=True)
    if doc.get_metadata('date') == 'today':
        doc.metadata['date'] = datetime.date.today().isoformat()
    slide_title_box(doc)

    def inlines(name):
        return list(doc.metadata[name].content)

    blocks = [pf.Header(*inlines('title'), level=1, classes=['title'])]
    if 'subtitle' in doc.metadata:
        blocks.append(pf.Div(
            pf.Plain(*inlines('subtitle')), classes=['subtitle']))
    blocks.append(pf.Div(
        pf.Plain(*inlines('institute')), classes=['institute']))
    return pf.Div(*blocks, classes=['title-preview'])


def render(elem, doc):
    if not (isinstance(elem, (pf.CodeBlock, pf.Div)) and 'render' in elem.classes):
        return None

    def cell(text):
        return pf.TableCell(pf.Plain(pf.Str(text)), alignment='AlignCenter')

    colspec = [('AlignDefault', 'ColWidthDefault')]
    slide_preview = 'slide' in elem.classes
    title_preview = 'title-slide' in elem.classes

    def rendered(elem):
        block = (title_slide_preview(elem.text)
                 if title_preview else
                 pf.RawBlock(elem.text, 'markdown'))
        return pf.TableCell(
            pf.Div(block, classes=['slide-preview'] if slide_preview else [])
            if isinstance(elem, pf.CodeBlock) else block)

    if isinstance(elem, pf.CodeBlock):
        elem.classes.remove('render')
        elem.classes[:0] = ['raw', 'default']
        return pf.BlockQuote(
            pf.Plain(pf.Strong(pf.Str('Markdown Source'))),
            elem,
            pf.Plain(pf.Strong(pf.Str('Rendered Output'))),
            pf.Div(pf.RawBlock(elem.text, 'markdown')))

    def collect(elem, _):
        if not isinstance(elem, (pf.Code, pf.CodeBlock)):
            return None

        elem.classes[:0] = ['raw', 'default']
        rows.append(pf.TableRow(
            pf.TableCell(pf.Plain(elem) if isinstance(elem, pf.Code) else elem),
            rendered(elem)))

    rows = []
    elem.walk(collect)

    if not rows:
        return None

    table = pf.Table(
        pf.TableBody(*rows),
        head=pf.TableHead(
            pf.TableRow(cell('Markdown Source'), cell('Rendered Output'))),
        colspec=colspec*2)
    return pf.Div(table, classes=list(elem.classes))

if __name__ == '__main__':
    pf.run_filter(render)
