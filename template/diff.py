#!/usr/bin/env python3

"""
A Pandoc filter to create non-code diffs. `add` and `rm` are the classes that
can be added to a `Div` or a `Span`.  `add` colors the text green, and `rm`
colors the text red. For HTML, `add` also underlines the text, and `rm` also
strikes out the text.

# Example

## `Div`

Unchanged portion

::: add
New paragraph

> Quotes

More new paragraphs
:::

## `Span`

> The return type is `decltype(`_e_(`m`)`)` [for the first form]{.add}.

"""

import panflute as pf

def action(elem, doc):
    if not isinstance(elem, pf.Div) and not isinstance(elem, pf.Span):
        return None

    color_name = None
    tag_name = None
    for cls in elem.classes:
        color_name = cls + 'color'
        if cls == 'add':
            tag_name = 'ins'
        elif cls == 'rm':
            tag_name = 'del'

    if tag_name is None:
        return None

    open_tag = pf.RawInline('<{}>'.format(tag_name), 'html')
    open_color = pf.RawInline('{{\\color{{{}}}'.format(color_name), 'tex')
    close_color = pf.RawInline('}', 'tex')
    close_tag = pf.RawInline('</{}>'.format(tag_name), 'html')

    color = doc.get_metadata(color_name)
    attributes = {} if color is None else {'style': 'color: #{}'.format(color)}

    if isinstance(elem, pf.Div):
        return pf.Div(pf.Plain(open_tag),
                      pf.Plain(open_color),
                      elem,
                      pf.Plain(close_color),
                      pf.Plain(close_tag),
                      attributes=attributes)
    elif isinstance(elem, pf.Span):
        return pf.Span(open_tag,
                       open_color,
                       elem,
                       close_color,
                       close_tag,
                       attributes=attributes)

if __name__ == '__main__':
    pf.run_filter(action)
