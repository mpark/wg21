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

import panflute as pf

def render(elem, doc):
    if not (isinstance(elem, (pf.CodeBlock, pf.Div)) and 'render' in elem.classes):
        return None

    def cell(text):
        return pf.TableCell(pf.Plain(pf.Str(text)), alignment='AlignCenter')

    colspec = [('AlignDefault', 'ColWidthDefault')]

    def rendered(elem):
        block = pf.RawBlock(elem.text, 'markdown')
        return pf.TableCell(pf.Div(block) if isinstance(elem, pf.CodeBlock) else block)

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

    return pf.Table(
        pf.TableBody(*rows),
        head=pf.TableHead(
            pf.TableRow(cell('Markdown Source'), cell('Rendered Output'))),
        colspec=colspec*2)

if __name__ == '__main__':
    pf.run_filter(render)
