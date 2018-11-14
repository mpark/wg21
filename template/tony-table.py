#!/usr/bin/env python

"""
A Pandoc filter to create Tony Tables from nested divs (in a similar manner to html).

# Example

::: TonyTable

```cpp
switch (x) {
  case 0: std::cout << "got zero"; break;
  case 1: std::cout << "got one"; break;
  default: std::cout << "don't care";
}
```

```cpp
inspect (x) {
  0: std::cout << "got zero";
  1: std::cout << "got one";
  _: std::cout << "don't care";
}
```

:::

# Generates

+------------------------------------------------+-------------------------------------------------+
| __Before__                                     | __After__                                       |
+================================================+=================================================+
| ```cpp                                         | ```cpp                                          |
| switch (x) {                                   | inspect (x) {                                   |
|   case 0: std::cout << "got zero"; break;      |   0: std::cout << "got zero";                   |
|   case 1: std::cout << "got one"; break;       |   1: std::cout << "got one";                    |
|   default: std::cout << "don't care";          |   _: std::cout << "don't care";                 |
| }                                              | }                                               |
| ```                                            | ```                                             |
+------------------------------------------------+-------------------------------------------------+

# Notes
  - Any non-CodeBlocks are ignored.
  - CodeBlocks are grouped into pairs of before/after as they appear.
    If there are odd number of CodeBlocks, the odd one is ignored.
"""

import panflute as pf

def action(table, doc):
    if not isinstance(table, pf.Div) or "TonyTable" not in table.classes:
        return None

    elems = [pf.TableCell(elem) for elem in table.content if isinstance(elem, pf.CodeBlock)]
    rows = [pf.TableRow(*row) for row in zip(elems[0::2], elems[1::2])]

    header = [pf.TableCell(pf.Plain(pf.Strong(pf.Str(header)))) for header in ["Before", "After"]]
    kwargs = {"header": pf.TableRow(*header)}
    return pf.Table(*rows, **kwargs)

if __name__ == "__main__":
    pf.run_filter(action)
