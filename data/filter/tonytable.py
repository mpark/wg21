#!/usr/bin/env python3

"""
A Pandoc filter to create Tony Tables.

CodeBlocks are the first-class entities that get added to the table.
The last (if any) header leading upto a CodeBlock is the header that
gets attached to the table cell with the CodeBlock.

Each CodeBlock entry is pushed onto the current row. Horizontal rule
is used to move to the next row.

# Example

::: tonytable

### Before
```cpp
std::visit([&](auto&& x) {
  strm << "got auto: " << x;
}, v);
```

### After
```cpp
inspect (v) {
  <auto> x: strm << "got auto: " << x;
}
```

---

```cpp
std::visit([&](auto&& x) {
  using X = std::remove_cvref_t<decltype(x)>;
  if constexpr (C1<X>()) {
    strm << "got C1: " << x;
  } else if constexpr (C2<X>()) {
    strm << "got C2: " << x;
  }
}, v);
```

```cpp
inspect (v) {
  <C1> c1: strm << "got C1: " << c1;
  <C2> c2: strm << "got C2: " << c2;
}
```

:::

# Generates

+------------------------------------------------+-------------------------------------------------+
| __Before__                                     | __After__                                       |
+------------------------------------------------+-------------------------------------------------+
| ```cpp                                         | ```cpp                                          |
| std::visit([&](auto&& x) {                     | inspect (v) {                                   |
|   strm << "got auto: " << x;                   |   <auto> x: strm << "got auto: " << x;          |
| }, v);                                         | }                                               |
|                                                | ```                                             |
+------------------------------------------------+-------------------------------------------------+
| std::visit([&](auto&& x) {                     | ```cpp                                          |
|   using X = std::remove_cvref_t<decltype(x)>;  | inspect (v) {                                   |
|   if constexpr (C1<X>()) {                     |   <C1> c1: strm << "got C1: " << c1;            |
|     strm << "got C1: " << x;                   |   <C2> c2: strm << "got C2: " << c2;            |
|   } else if constexpr (C2<X>()) {              | }                                               |
|     strm << "got C2: " << x;                   | ```                                             |
|   }                                            |                                                 |
| }, v);                                         |                                                 |
+------------------------------------------------+-------------------------------------------------+

"""

import html
import panflute as pf

def build_header(elem):
    # We use a `pf.RawInline` here because setting the `align`
    # attribute on `pf.Div` does not work for some reason.
    header = pf.Plain(pf.RawInline('<div align="center">', 'html'),
                      pf.Strong(*elem.content),
                      pf.RawInline('</div>', 'html'))
    width = float(elem.attributes['width']) if 'width' in elem.attributes else 0
    return header, width

def build_code(elem, format):
    if (format != 'gfm'):
        return elem
    lang = ' lang="{}"'.format(elem.classes[0]) if elem.classes else ''
    code = html.escape(elem.text)
    return pf.RawBlock('\n\n<pre{lang}>\n{code}\n</pre>'.format(lang=lang, code=code))

def build_row(elems):
    return pf.TableRow(*[pf.TableCell(elem) for elem in elems])

def action(table, doc):
    if not isinstance(table, pf.Div) or 'tonytable' not in table.classes:
        return None

    rows = []

    kwargs = {}

    headers = []
    widths = []
    examples = []

    header = pf.Null()
    width = 0
    table.content.append(pf.HorizontalRule())
    for elem in table.content:
        if isinstance(elem, pf.Header):
            header, width = build_header(elem)
        elif isinstance(elem, pf.CodeBlock):
            headers.append(header)
            widths.append(width)
            header = pf.Null()
            width = 0

            examples.append(build_code(elem, doc.format))
        elif isinstance(elem, pf.HorizontalRule) and examples:
            if not all(isinstance(header, pf.Null) for header in headers):
                rows.append(build_row(headers))

            if 'width' not in kwargs:
                kwargs['width'] = widths

            rows.append(build_row(examples))

            headers = []
            widths = []
            examples = []
        else:
            pf.debug("[Warning] The following is ignored by a Tony Table:",
                     pf.stringify(elem))

    return pf.Table(*rows, **kwargs)

if __name__ == '__main__':
    pf.run_filter(action)
