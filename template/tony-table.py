#!/usr/bin/env python3

"""
A Pandoc filter to create Tony Tables.

# Example

::: TonyTable

### Before
```cpp
switch (x) {
  case 0: std::cout << "got zero"; break;
  case 1: std::cout << "got one"; break;
  default: std::cout << "don't care";
}
```

### After
```cpp
inspect (x) {
  0: std::cout << "got zero";
  1: std::cout << "got one";
  _: std::cout << "don't care";
}
```

:::

# Generates

+-------------------------------------------+---------------------------------+
| __Before__                                | __After__                       |
+-------------------------------------------+---------------------------------+
| ```cpp                                    | ```cpp                          |
| switch (x) {                              | inspect (x) {                   |
|   case 0: std::cout << "got zero"; break; |   0: std::cout << "got zero";   |
|   case 1: std::cout << "got one"; break;  |   1: std::cout << "got one";    |
|   default: std::cout << "don't care";     |   _: std::cout << "don't care"; |
| }                                         | }                               |
| ```                                       | ```                             |
+-------------------------------------------+---------------------------------+

# Notes
  - Any non-CodeBlocks are ignored.
  - CodeBlocks are grouped into pairs of before/after as they appear.
    If there are odd number of CodeBlocks, the odd one is ignored.
"""

import html
import panflute as pf

def build_header(elem, format):
    header = pf.stringify(elem)
    if format != 'gfm':
        return pf.Plain(pf.Strong(pf.Str(header)))
    # We use a `pf.RawBlock` here because setting the `align`
    # attribute on a `pf.Div` does not work for some reason.
    header = '<div align="center"><strong>{}</strong></div>'.format(header)
    return pf.RawBlock(header)

def build_code(elem, format):
    if (format != 'gfm'):
        return elem
    lang = ' lang={}'.format(elem.classes[0]) if elem.classes else ''
    code = html.escape(elem.text)
    return pf.RawBlock('<pre{lang}>{code}</pre>'.format(lang=lang, code=code))

def build_row(elems):
    return pf.TableRow(*[pf.TableCell(elem) for elem in elems])

def action(table, doc):
    if not isinstance(table, pf.Div) or 'TonyTable' not in table.classes:
        return None

    rows = []

    headers = []
    examples = []

    header = pf.Null()
    table.content.append(pf.HorizontalRule())
    for elem in table.content:
        if isinstance(elem, pf.Header):
            header = build_header(elem, doc.format)
        elif isinstance(elem, pf.CodeBlock):
            headers.append(header)
            header = pf.Null()

            examples.append(build_code(elem, doc.format))
        elif isinstance(elem, pf.HorizontalRule) and examples:
            if not all(isinstance(header, pf.Null) for header in headers):
                rows.append(build_row(headers))

            rows.append(build_row(examples))

            headers = []
            examples = []
        else:
            pf.debug("[Warning] The following is ignored by a TonyTable:",
                     pf.stringify(elem))

    return pf.Table(*rows)

if __name__ == '__main__':
    pf.run_filter(action)
