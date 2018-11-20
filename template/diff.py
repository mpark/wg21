#!/usr/bin/env python3

"""
A Pandoc filter to create non-code diffs. `add` and `remove` are the classes
that can be added to a `Div` or a `Span`.  `add` colors the text green, and
`remove` colors the text red. For HTML, `add` also underlines the text, and
`remove` also strikes out the text.

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

    diff = None
    for cls in elem.classes:
        if cls == 'add' or cls == 'remove':
            diff = cls

    if diff is None:
        return None

    color_name = diff + 'color'
    color_begin = pf.RawInline('{{\\color{{{}}}'.format(color_name), 'tex')
    color_end = pf.RawInline('}', 'tex')
    color = doc.get_metadata(color_name)
    attributes = {} if color is None else {'style': 'color: #{}'.format(color)}

    def format(*args):
        if diff == 'add':
            return pf.Span(pf.RawInline('<ins>'), *args, pf.RawInline('</ins>'))
        elif diff == 'remove':
            return pf.Span(pf.RawInline('<del>'), *args, pf.RawInline('</del>'))

    if isinstance(elem, pf.Div):
        def visit(elem, doc):
            if isinstance(elem, pf.Header):
                return pf.Header(format(*elem.content))
            elif isinstance(elem, pf.Para):
                return pf.Para(format(*elem.content))
            elif isinstance(elem, pf.Plain):
                return pf.Plain(format(*elem.content))
            elif isinstance(elem, pf.LineItem):
                if elem.content:
                    head, *tail = elem.content
                    if isinstance(head, pf.Str) and head.text.isspace():
                        return pf.LineItem(head, format(*tail))
                return pf.LineItem(format(*elem.content))
        elem.walk(visit)
        return pf.Div(pf.Plain(color_begin),
                      pf.Div(*elem.content),
                      pf.Plain(color_end),
                      attributes=attributes)
    elif isinstance(elem, pf.Span):
        return pf.Span(color_begin, format(*elem.content), color_end,
                       attributes=attributes)

if __name__ == '__main__':
    pf.run_filter(action)
