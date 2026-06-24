---
title: "Stable Reference Tests"
document: D0000R1
date: 2026-01-01
audience:
  - Library Evolution
author:
  - name: Test Author
    email: <test@example.com>
toc: true
toc-depth: 2
---

# Stable Names

Stable names are written as `[basic.life]{.sref}`, and render as [basic.life]{.sref}.

- Add the `-` or `.unnumbered` class to omit the section number.
- Add the `.title` class to add the section title.

Examples:

| Markdown Source                             | Rendered Output                 |
| ------------------------------------------- | ------------------------------- |
| `[basic.life]`{.default}                    | [basic.life]                    |
| `[basic.life]/1`{.default}                  | [basic.life]/1                  |
| `[basic.life]/2.1`{.default}                | [basic.life]/2.1                |
| `[basic.life]{.sref}`{.default}             | [basic.life]{.sref}             |
| `[basic.life]{.sref}/1`{.default}           | [basic.life]{.sref}/1           |
| `[basic.life]{.sref .title}`{.default}      | [basic.life]{.sref .title}      |
| `[basic.life]{.sref .title}/1`{.default}    | [basic.life]{.sref .title}/1    |

Also supported:

| Markdown Source                             | Rendered Output                 |
| ------------------------------------------- | ------------------------------- |
| `[basic.life#1]{.sref}`{.default}           | [basic.life#1]{.sref}           |
| `[basic.life]{- .sref .title}`{.default}    | [basic.life]{- .sref .title}    |

# Override stable name links

Override [over.match] to something else.

[over.match]: https://isocpp.org
