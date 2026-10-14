# Comparison tables

A before and after table is often the fastest way to sell a proposal: today's code on the left, the proposed code on the right. The framework builds these tables, formerly called Tony Tables, straight from fenced code blocks, so the code in each cell gets full syntax highlighting and everything else code blocks can do. After reading this file you will be able to build a comparison table with any number of rows and columns, label and size its columns, give it a caption, and know how it looks in PDF and in HTML and what the build warns about.

## A before and after table

A side-by-side comparison table is built by wrapping fenced code blocks in a `::: cmptable` fenced div closed with `:::`:

````markdown
::: cmptable
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
x match {
  0 => do { std::cout << "got zero" };
  1 => do { std::cout << "got one" };
  _ => do { std::cout << "don't care" };
};
```
:::
````

The result is a two-column table with "Before" and "After" as bold, centered column headings and the two code blocks side by side beneath them, each with normal C++ highlighting, in both PDF and HTML.

Three rules make this work. Each fenced code block inside the div is pushed onto the current row, so consecutive code blocks sit side by side as the cells of one row. In the first row, a heading placed right before a code block becomes that column's label. And the headings are column labels only: they do not become document sections, get no section number, do not appear in the table of contents, get no self-link, and cannot be the target of an automatic empty-link title `[](#id)`.

`::: tonytable` is accepted as an alias for `::: cmptable`, so older papers keep working. The HTML stylesheet's full-width rule targets only the `cmptable` class, though, so write `cmptable` in new papers.

## Table variants

### More rows

A horizontal rule `---` on its own line starts a new row of the comparison table; it does not draw a rule. Cells in later rows need no headings: header-less code blocks become plain cells under the columns set by the first row, and they keep the first row's widths.

````markdown
::: cmptable
### Before
```cpp
switch (x) {
  case 0: std::cout << "got zero"; break;
}
```

### After
```cpp
x match {
  0 => do { std::cout << "got zero" };
};
```

---

```cpp
if (s == "foo") {
  std::cout << "got foo";
}
```

```cpp
s match {
  "foo" => do { std::cout << "got foo" };
};
```
:::
````

The table has two rows under one Before and After header.

### More columns

Because every code block in a row becomes a cell, three code blocks in a row give three columns:

````markdown
::: cmptable
### C++17
```cpp
template <class T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
void f(T);
```

### C++20
```cpp
template <std::integral T>
void f(T);
```

### Abbreviated
```cpp
void f(std::integral auto);
```
:::
````

The table has three labeled columns of equal width.

### Unlabeled columns

A column is left unlabeled by omitting its heading. If no first-row code block has a heading at all, the table has no header row:

````markdown
::: cmptable
```cpp
int x = 0;
```

```cpp
auto x = 0;
```
:::
````

This gives two side-by-side cells with no header row.

### A caption

A block quote inside the `::: cmptable` div becomes the table's caption. If there are several block quotes, only the last one is used. The framework's own guide puts the caption first, before the headings:

````markdown
::: cmptable
> Put your caption here with some `code`

### Before
```cpp
int x = 0;
```

### After
```cpp
auto x = 0;
```
:::
````

The caption appears as the table's caption in both PDF and HTML. Inline code in a comparison table caption is highlighted as C++ by default, like inline code anywhere else, and in PDF it does not break the build. Leaving out the block quote gives a table with no caption, which is the default.

### Column widths

A numeric `width` attribute on each first-row heading sets relative column widths. The numbers are normalized against their sum:

````markdown
::: cmptable
### Before {width=2}
```cpp
int x = 0;
```

### After {width=1}
```cpp
auto x = 0;
```
:::
````

Here 2 and 1 give columns of 2/3 and 1/3 of the table width. Writing `{width=.6}` and `{width=.4}` gives 60% and 40%. The `width` attribute text does not appear in the rendered heading, which still reads just "Before" or "After". When no heading has a `width` attribute, every column gets an equal share of the table width.

Specify `width` on every column or on none. A partial set prints a warning (quoted below) and the table falls back to equal widths. Because the width lives on the heading, a table with explicit widths needs a heading on every column. The value must be a plain number: something like `{width=50%}` is not a number, and the build stops with a Python error.

### Extra classes

The generated table keeps every class written on the div (`cmptable` or `tonytable` plus any extra classes you add), so a custom HTML stylesheet can target it. Its columns use default alignment.

````markdown
::: {.cmptable .wide}
### Before
```cpp
int x = 0;
```

### After
```cpp
auto x = 0;
```
:::
````

This renders like any other comparison table, but the table has the extra `wide` class for your own styling to use.

### Code features inside cells

Syntax highlighting, embedded Markdown, `diff` coloring, and `.not_proposed` all work inside comparison table cells, exactly as they do for code anywhere else in the paper:

````markdown
::: cmptable
### Rejected
```cpp {.not_proposed}
auto $result$ = f();
```

### Proposed
```diff
- auto r = f();
+ auto r = g();
```
:::
````

The left cell shows the not-proposed styling with `result` in italics, and the right cell shows red and green diff lines.

### What else can go in the div

Only fenced code blocks become comparison table cells. Headings (as column labels), block quotes (as the caption), and `---` (as the row break) are the only other elements with a role inside `::: cmptable`. Keep everything else out: other content is dropped with a warning.

## How comparison tables render

In both formats, every table, ordinary Markdown tables and comparison tables alike, gets bold, centered header cells.

In PDF, the table is a real table with the code blocks as cells, and each cell is top-aligned. Long comparison tables break across pages, with the column headers such as Before and After repeated at the top of each page. A table without a caption has no caption number.

In HTML, comparison tables span the full page width, and explicit column widths are preserved. Like every HTML table, the comparison table is wrapped in a container with the class `table-wrapper`. On screens narrower than 90em, a table wider than the page scrolls sideways inside that container instead of widening the page.

### Warnings from comparison tables

The build warns, and keeps going, when a table does not follow the rules above:

- Comparison table headings belong in the first row only. A heading placed after the first `---` is dropped with the warning `[WARNING] mpark/wg21: <element type> <heading text> in a comparison table is ignored`.
- Put at most one heading before each first-row code block. When two headings precede the same block, only the later one is used and the earlier one is dropped with the same "in a comparison table is ignored" warning.
- Use at most one block quote. With several, only the last becomes the caption and each earlier one is dropped with the same warning.
- Any content other than headings, code blocks, block quotes, and `---` (paragraphs, lists, nested divs, and so on) is dropped with the warning `[WARNING] mpark/wg21: <element type> <element text> in a comparison table is ignored`, where the element type is printed as a Python class name and the text is flattened onto one line. A `---` that does not follow at least one code block, such as one at the very start or end of the div or two in a row, is dropped with the same warning.
- A partial set of `width` attributes prints the following warning, and the table falls back to equal widths:

````text
[WARNING] mpark/wg21: cmptable widths must be specified for all columns or none.
Ignoring the specified widths and defaulting to even column widths.
````

In that message, the dump of the table appears between the two lines shown.

Previous: [Wording](07-wording.md) | Next: [Stable names and citations](09-stable-names-and-citations.md)

*2026-09-25 - claude-opus-5.5*
