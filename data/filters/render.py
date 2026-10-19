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

import copy

import panflute as pf

from wg21 import slide_title_box


def title_slide_preview(text):
    doc = pf.convert_text(text, standalone=True)
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
        return pf.TableCell(
            pf.Plain(pf.Span(
                pf.Str(text), attributes={'data-id': text})),
            alignment='AlignCenter')

    def render_table(rows):
        return pf.Table(
            pf.TableBody(*rows),
            head=pf.TableHead(pf.TableRow(
                cell('Markdown Source'), cell('Rendered Output'))),
            colspec=[('AlignDefault', 'ColWidthDefault')]*2)

    slide_preview = 'slide' in elem.classes
    title_preview = 'title-slide' in elem.classes

    if isinstance(elem, pf.Div) and 'animation' in elem.classes:
        guide_header, *description, example = elem.content
        assert isinstance(guide_header, pf.Header)
        assert isinstance(example, pf.CodeBlock)

        slides = []
        for block in pf.convert_text(example.text):
            if isinstance(block, pf.Header) and block.level == 2:
                slides.append([block])
            else:
                assert slides
                slides[-1].append(block)
        assert len(slides) > 1

        result = []
        for i, slide in enumerate(slides):
            header = copy.deepcopy(guide_header)
            header.attributes.update(slide[0].attributes)
            if i:
                header.identifier += f'-{i}'
            source = pf.CodeBlock(
                example.text, classes=['raw', 'default'])
            slide[0].identifier += '-preview'
            slide[0].attributes.clear()
            preview = pf.Div(*slide, classes=['slide-preview'])
            row = pf.TableRow(
                pf.TableCell(source), pf.TableCell(preview))
            result.extend([
                header,
                *copy.deepcopy(description),
                pf.Div(render_table([row]), classes=['render', 'slide'])])
        return result

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

    return pf.Div(render_table(rows), classes=list(elem.classes))

if __name__ == '__main__':
    pf.run_filter(render)
