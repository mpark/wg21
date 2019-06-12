# WG21: C++ Standards Committee Papers

## Introduction

The top-level of this repository contains the source code for various proposals
and the `generated/` directory contains the generated proposals (HTML or PDF).

This repository also includes a paper-writing framework using [Pandoc].

[Pandoc]: https://pandoc.org

## Status

- [P1371]: Pattern Matching
- [P1469]: Disallow `_` Usage in C++20 for Pattern Matching in C++23
- [P1260]: Pattern Matching - Requested to unify with [P1308]
- [P0655]: `visit<R>`: Explicit Return Type for `visit` - Accepted in C++20
- [D0080]: Tweaks to the Kona Variant - Encouraged to return with `P`-papers
- [P0080]: Variant: Discriminated Union with Value Semantics - Not presented
- [N3887]: Consistent Metafunction Aliases - Accepted in C++14

[P1371]: https://wg21.link/p1371
[P1469]: https://wg21.link/p1469
[P1308]: https://wg21.link/p1308
[P1260]: https://wg21.link/p1260
[P0655]: https://wg21.link/p0655
[D0080]: generated/D0080R1.pdf
[P0080]: https://wg21.link/p0080
[N3887]: https://wg21.link/n3887

## Generation

```bash
make <paper>.pdf  # `<paper>.md` -> `generated/<paper>.pdf`
make <paper>.html # `<paper>.md` -> `generated/<paper>.html`
```

## Integration

```bash
git submodule add https://github.com/mpark/wg21.git

echo "include wg21/Makefile" > Makefile

make <paper>.pdf  # `<paper>.md` -> `generated/<paper>.pdf`
make <paper>.html # `<paper>.md` -> `generated/<paper>.html`
```

## Formatting

This framework provides support for various common elements for C++ papers.

- [Title](#title)
- [Table of Contents](#table-of-contents)
- [Markdown](#markdown)
  - [Within Code Blocks](#within-code-blocks)
- [Tony Tables](#tony-tables)
- [Proposed Wording](#proposed-wording)
  - [Paragraph Numbers](#paragraph-numbers)
  - [Code Changes](#code-changes)
  - [Wording Changes](#wording-changes)
  - [Grammar Changes](#grammar-changes)
- [Citations](#citations)
- [References](#references)
  - [Automatic References](#automatic-references)
  - [Manual References](#manual-references)

### Title

The title is specified in a YAML metadata block.

![](img/title.png)

> `date: today` will generate today's date in `YYYY-MM-DD` (ISO 8601) format.

YAML lists can be used to specify multiple audiences and authors:

```yaml
---
title: Integration of chrono with text formatting
document: P1361R0
date: 2018-10-16
audience:
  - Library Evolution Working Group
  - Library Working Group
author:
  - name: Victor Zverovich
    email: <victor.zverovich@gmail.com>
  - name: Daniela Engert
    email: <dani@ngrt.de>
  - name: Howard E. Hinnant
    email: <howard.hinnant@gmail.com>
---
```

### Table of Contents

![](img/toc-false.png)

---

![](img/toc-true.png)

---

The default `toc-depth` is `3`, but it can be specified to go deeper:
![](img/toc-depth.png)

### Markdown

Refer to the full [Pandoc Markdown] spec for useful extensions!

[Pandoc Markdown]: https://pandoc.org/MANUAL.html#pandocs-markdown

#### Within Code Blocks

Within `` ``` ``, `` ```cpp ``, and `` ```diff `` code blocks, any text
surrounded by the `@` symbol is formatted as Markdown! This is useful for
conventions such as _`see below`_, _`unspecified`_, and _exposition-only_
variable names.

![](img/code-cpp.png)

### Tony Tables

Tony Tables are [fenced `Div` blocks][divspan] that open with `::: tonytable`
and close with `:::`. [Fenced code blocks][code] are the only elements that
actually get added to Tony Tables, except that the last header (if any) before
a [fenced code block][code] is attached to the cell above. Each code block is
pushed onto the current row.

``````md
::: tonytable

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
``````

[code]: https://pandoc.org/MANUAL.html#fenced-code-blocks
[divspan]: https://pandoc.org/MANUAL.html#divs-and-spans

![](img/tonytable-1.png)

Each [fenced code block][code] is pushed onto the current row,
and horizontal rules (`---`) are used to move to the next row.

``````md
::: tonytable

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

---

```cpp
if (s == "foo") {
  std::cout << "got foo";
} else if (s == "bar") {
  std::cout << "got bar";
} else {
  std::cout << "don't care";
}
```

```cpp
inspect (s) {
  "foo": std::cout << "got foo";
  "bar": std::cout << "got bar";
  _: std::cout << "don't care";
}
```

:::
``````

![](img/tonytable-2.png)

### Proposed Wording

#### Paragraph Numbers

Paragraph numbers are [bracketed `Span` elements][divspan] that look
like: `[2]{.pnum}` and `[2.1]{.pnum}`.

```markdown
[2]{.pnum} An expression is _potentially evaluated_ unless it is an unevaluated
operand (7.2) or a subexpression thereof. The set of _potential results_ of
an expression `e` is defined as follows:

- [2.1]{.pnum} If `e` is an _id-expression_ (7.5.4), the set contains only `e`.
- [2.2]{.pnum} If `e` is a subscripting operation (7.6.1.1) with an array operand,
the set contains the potential results of that operand.
```

![](img/pnum.png)

#### Code Changes

![](img/code-diff.png)

#### Wording Changes

Large changes are [fenced `Div` blocks][divspan] with `::: add` for additions, `::: rm` for removals.

![](img/wording-div.png)

Small, inline changes are [bracketed `Span` elements][divspan] that looks like
`[<new text>]{.add}` or `[<old text>]{.rm}`.

![](img/wording-span.png)

#### Grammar Changes

Use [line blocks][lineblock] (`|`) in order to preserve the leading spaces.

[lineblock]: https://pandoc.org/MANUAL.html#line-blocks

```markdown
> | _selection-statement:_
> |     `if constexpr`_~opt~_ `(` _init-statement~opt~_ _condition_ `)` _statement_
> |     `if constexpr`_~opt~_ `(` _init-statement~opt~_ _condition_ `)` _statement_ `else` _statement_
> |     `switch (` _init-statement~opt~_ _condition_ `)` _statement_
> |     [`inspect` `constexpr`~_opt_~ `(` _init-statement~opt~_ _condition_ `)` `{`
>            _inspect-case-seq_
>        `}`]{.add}
>
> ::: add
> | _inspect-case-seq:_
> |     _inspect-case_
> |     _inspect-case-seq_ _inspect-case_
>
> | _inspect-case:_
> |     _attribute-specifier-seq~opt~_ _inspect-pattern_ _inspect-guard~opt~_ `:` _statement_
>
> | _inspect-pattern:_
> |     _wildcard-pattern_
> |     _identifier-pattern_
> |     _constant-pattern_
> |     _structured-binding-pattern_
> |     _alternative-pattern_
> |     _binding-pattern_
> |     _extractor-pattern_
>
> | _inspect-guard:_
> |     `if (` _expression_ `)`
> :::
```

![](img/grammar.png)

### Citations

In-text citations look like this: `[@<id>]`

![](img/citation.png)

### References

#### Automatic References

The bibliography is automatically generated from <https://wg21.link/index.yaml>
for citations of the following types.

| Type              | Id                                                                            |
| ----------------- | ----------------------------------------------------------------------------- |
| Paper             | __N__*xxxx* / __P__*xxxx*__R__*n*                                             |
| Issue             | __CWG__*xxxx* / __EWG__*xxxx* / __LWG__*xxxx* / __LEWG__*xxxx* / __FS__*xxxx* |
| Editorial         | __EDIT__*xxx*                                                                 |
| Standing Document | __SD__*x*                                                                     |

The `[@N3546]` example from [Citations](#citations) generates:

![](img/automatic-reference.png)

> Use `make update` to update the local cache of [index.yaml](https://wg21.link/index.yaml).

#### Manual References

Manual references are specified in a YAML metadata block similar
to [Title](#title), typically at the bottom of the document.

```yaml
The `id` field is for in-text citations (e.g., [@PAT]),
and `citation-label` is the label for the reference.

Typically `id` and `citation-label` are kept the same.

---
references:
  - id: PAT
    citation-label: Patterns
    title: "Pattern Matching in C++"
    author:
      - family: Park
        given: Michael
    URL: https://github.com/mpark/patterns
---
```

![](img/manual-reference.png)

## Other Papers

- [P1361]: Integration of chrono with text formatting
- [P1390]: Suggested Reflection TS NB Resolutions

[P1361]: https://wg21.link/p1361
[P1390]: https://wg21.link/p1390

## Requirements

  - `pdflatex`
  - `pandoc` (>= 2.7.3)
  - `pandoc-citeproc`
  - `python3`
  - `panflute`

### OS X

```bash
brew cask install mactex
brew install pandoc pandoc-citeproc python
pip3 install panflute
```

### Ubuntu

Manually install the [latest pandoc release] following their [instructions].

```bash
sudo apt-get install texlive-latex-base
pip3 install panflute
```

[latest pandoc release]: https://github.com/jgm/pandoc/releases/latest
[instructions]: https://pandoc.org/installing.html

## Resources

  - Blog Post: [How I format my C++ papers][FMT]

[FMT]: https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers
