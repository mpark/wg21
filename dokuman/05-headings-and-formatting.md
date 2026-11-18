# Headings and formatting

Most of a paper is ordinary prose, and the framework handles it with ordinary Markdown plus a few additions. After reading this file you will be able to structure a paper with numbered, unnumbered, and unlisted headings, link to any section with text that keeps itself up to date, and use every inline format the framework supports (emphasis, underline, strikeout, superscript and subscript, highlighting, and math), along with lists, tables, and raw HTML, knowing how each one looks in PDF and in HTML.

## Numbered and unnumbered headings

Headings can be written in Setext style, with the text underlined by `=` for level 1 or `-` for level 2, or in ATX style, with leading `#` marks:

````markdown
Header 1
========

Header 2
--------

### Header 3

#### Header 4
````

Every paper gets numbered section headings by default (1, 1.1, 1.1.1, and so on), and the table of contents shows the same numbers. A top-level `#` heading becomes an automatically numbered section with a stable anchor, a self-link, and a table of contents entry. In PDF the number prints before the heading text; level-4 and level-5 headings print on their own line rather than running into the following paragraph. In HTML the number also prints before the heading text, and the self-link shows as a faint "§" in the margin beside the heading that brightens when the reader hovers over it, giving a copyable link to that section. Every heading gets a self-link, whether numbered, unnumbered, or unlisted.

To exclude one heading from section numbering, add the `-` class or the `.unnumbered` class:

````markdown
# Miscelleneous {-}

# Miscelleneous {.unnumbered}
````

Both forms mean the same thing. The heading prints without a number in PDF and in HTML, and it still appears in the table of contents, also without a number.

To turn section numbering off for a whole paper, set `number-sections: false` in your own Pandoc defaults file; [Your own defaults file](10-customization.md#your-own-defaults-file) explains how to create one. When numbering is off, every heading is unnumbered.

In PDF only, `secnumdepth:` in the front matter controls how many heading levels get numbers. It defaults to 5 when numbering is on:

````yaml
secnumdepth: 3
````

## Headings left out of the table of contents

Adding `.unlisted` together with `-` or `.unnumbered` also hides the heading from the table of contents:

````markdown
# Miscelleneous {- .unlisted}
````

The heading prints without a number and has no table of contents entry, in both PDF and HTML. `.unlisted` works only in combination with `-` or `.unnumbered`, so always write it alongside one of them. An unlisted heading keeps its self-link.

The two formats differ for headings nested under an unlisted heading. In HTML, those nested headings are also missing from the table of contents. PDF still lists them.

## Referring to sections

Every heading gets an id generated automatically from its text. "Algorithm Return Type" becomes `#algorithm-return-type`, `## C++ Syntax Highlighting` becomes `c-syntax-highlighting`, and a heading with inline code, ``## Inline Code in Headers: `int`{.cpp}, `x & y`{.cpp}``, becomes `inline-code-in-headers-int-x-y`.

### Linking by heading text

You can link to a heading by writing its text in brackets, without defining the anchor yourself. Given a heading `## Algorithm Return Type`, all four of these forms link to it:

````markdown
[Algorithm Return Type]

[Algorithm Return Type][]

[Custom Text 1][Algorithm Return Type]

[Custom Text 2](#algorithm-return-type)
````

The first two display the heading text; the last two display your own text. In PDF and HTML alike, each becomes a working internal link to the section.

### Custom ids

`{#id}` after a heading gives it a custom id so you can link to it directly, and the id does not change when you reword the heading:

````markdown
## Numbering of Explicit Stable Names {#numbering-stable-names}
````

The heading looks the same as without the id; only its anchor changes.

### Links that fill in the heading text

A link with empty text, `[](#id)`, displays the target heading's current text automatically. This is a framework extension, not stock Pandoc:

````markdown
## Algorithm Return Type {#return-type}

See [](#return-type) for details.
````

The link renders as "Algorithm Return Type" in both PDF and HTML. When you reword the heading, the reference stays valid and picks up the new text. If an empty link points at something other than a heading, the build prints this warning and the link is left with no text:

````text
[WARNING] mpark/wg21: cannot find automatic text for link to: #<anchor>
````

### Fixed anchors

The title block and the table of contents have fixed anchors you can link to from anywhere in the paper, `#title-block-header` and `#toctitle`. The same anchors work in PDF and HTML:

````markdown
Go back to the [title](#title-block-header) or the [table of contents](#toctitle).
````

### Other kinds of links

A link target can be defined once as a reference definition and reused anywhere by writing the label in brackets:

````markdown
[shortcut_reference_links]: https://pandoc.org/MANUAL.html#extension-shortcut_reference_links

Pandoc calls this [shortcut_reference_links].
````

A bare URL in angle brackets becomes a clickable link that shows the URL itself:

````markdown
<https://wg21.link/index.yaml>
````

Both work the same way in PDF and HTML. Links to C++ working-draft sections by stable name, such as `[basic.life]`, are a separate feature covered in [Stable names](09-stable-names-and-citations.md#stable-names).

## Emphasis and underline

Single asterisks or underscores emphasize text, and doubled ones strongly emphasize it:

````markdown
Some of these words *are emphasized*.
Some of these words _are emphasized also_.
Use two asterisks for **strong emphasis**.
Or, __use two underscores instead__.
````

Emphasis renders in italics and strong emphasis in bold, in both PDF and HTML.

To emphasize part of a word you must use asterisks. Underscores inside a word stay literal text:

````markdown
feas**ible**, not feas__able__
````

The first renders "feas" plain and "ible" in bold; the second prints the underscores as typed.

`[text]{.underline}` underlines text:

````markdown
This is [underlined text]{.underline}.
````

The text is underlined in both PDF and HTML.

## Strikeout

`~~text~~` strikes text out, and it renders in PDF with no extra setup:

````markdown
This is ~~struck out~~ text.
````

The text is drawn with a line through it in both PDF and HTML. Strikeout for proposed wording changes has its own markup with its own colors, covered in [Adding and removing text](07-wording.md#adding-and-removing-text); plain `~~text~~` is for when you just want a strikeout.

One PDF restriction applies to strikeout, underline, and highlighting alike: avoid nesting them inside one another, because in PDF those constructs do not nest and the result is broken.

## Superscript and subscript

Wrapping text in carets makes a superscript, and wrapping text in tildes makes a subscript:

````markdown
2^10^ is 1024

`constexpr`~opt~ means optional
````

In both PDF and HTML, `10` is raised and `opt` is lowered in smaller type. The subscript form is how you mark an optional grammar element, as the standard does; [Grammar](07-wording.md#grammar) shows it in context.

## Highlighting

Wrapping text in `==` highlights it, and other inline formatting may appear inside:

````markdown
This is a ==highlighted **text**==.
````

Highlights render with a yellow background, in both PDF and HTML, with the inner formatting (here, bold) intact.

`[highlighted text]{.mark}` is an alternative way to write the same thing:

````markdown
Also, [highlight *text*]{.mark}
````

It renders exactly like `==` highlighting, a yellow background behind the text.

## Math

Inline math is TeX between single dollar signs in ordinary text:

````markdown
The average is $\frac{a+b}{2}$.
````

In PDF, the math is typeset by LaTeX. amsmath and amssymb are always available, and `\cancel` works because the package that provides it is loaded automatically when the math uses it. In HTML, the math is rendered as native MathML by default, with no MathJax script to load.

## Line breaks and quotes

Ending a line with a backslash forces a line break inside a paragraph:

````markdown
To set the depth manually, set `toc-depth` to the desired number.\
For example, to make the heading show up:
````

The second sentence starts on a new line in both PDF and HTML, without starting a new paragraph.

Straight quotes and apostrophes you type become typographic curly quotes in both PDF and HTML, so `"no diagnostic is required"` and `the implementation's limitations` print with curly quotation marks and a curly apostrophe.

## Raw HTML

Raw HTML in the paper body passes through to HTML output, so you can hand-build something like a `<table>` for the HTML version of a paper. The sources behind this guide record only the HTML behavior, so check the PDF yourself if you rely on raw HTML there.

Because raw HTML is recognized, C++ with angle brackets in running prose can be mistaken for an HTML tag. Write C++ such as `generator<T>` inside backticks:

````markdown
The coroutine returns a `generator<T>`.
````

In backticks, `generator<T>` renders as code in both PDF and HTML. Without the backticks, `<T>` could be read as an HTML tag.

## Lists and tables

### Lists

A bulleted list with no blank lines between items is a compact list, tightly spaced in both outputs. A bulleted list with blank lines between items is a loose list, spaced more widely:

````markdown
- compact item one
- compact item two

- loose item one

- loose item two
````

Bulleted lists render with long-dash bullets rather than round bullets, matching the C++ working draft; in PDF the long dashes are used at every nesting level.

Code blocks, extra paragraphs, and notes can go inside a bulleted list item when indented two spaces under the `-` bullet.

### Pipe tables

Pipe tables work as usual:

````markdown
| Markdown Source                             | Rendered Output                 |
| ------------------------------------------- | ------------------------------- |
| `[basic.life]`                              | a link to the working draft     |
````

Header cells come out bold and centered, and column widths follow the relative lengths of the dashes in the separator row, in both PDF and HTML. Here the first column gets the larger share because its dash run is longer.

### Grid tables

Grid tables work too, with `+---+` border lines, a `+===+` rule under the header row, and dash widths that set relative column widths:

````markdown
+-----------+--------------------------------------------------------------------+
| Specifier | Replacement                                                        |
+===========+====================================================================+
| `%d`      | The day of the month as a decimal number.                          |
+-----------+--------------------------------------------------------------------+
````

Header cells are bold and centered in both outputs, and the PDF table has no caption number. Grid-table cells can hold wording-change markup, which [Adding and removing text](07-wording.md#adding-and-removing-text) covers.

In HTML, every table is wrapped in a container with the class `table-wrapper`, which a stylesheet can target.

Previous: [Paper metadata](04-paper-metadata.md) | Next: [Code](06-code.md)

*2026-09-25 - claude-opus-5.5*
