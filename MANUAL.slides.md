---
title: "`MPark/WG21` Slides Guide"
subtitle: Pandoc Slideshows with Reveal.js
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
---

## From Markdown to Slides

`MPark/WG21` turns Markdown into [Pandoc Slideshows] rendered with [Reveal.js].

::: {.render .slide}
``````
## Parsing Without Exceptions

```cpp
auto parse(std::string_view input)
    -> std::expected<value, parse_error> {
  if (input.empty()) {
    return std::unexpected(parse_error::empty_input);
  }
  return value{input};
}
```

Return a `value` or a *descriptive error*.

- Failure is explicit.
- Callers **must** handle both outcomes.

Added in C++23

- `std::expected` was introduced by [@P0323R12].
- The specification for `std::unexpected` can be found at [expected.unexpected].
``````
:::

# Getting Started

## Flat Project Layout

- For `<paper>.md`, create a `<paper>.slides.md` in the top-level directory.
- Outputs are written under `generated/`.

```{.embed_md}
wg21-papers/
|-- wg21/ (submodule)
|-- Makefile
|-- p2688r6.md
|-- @==p2688r6.slides.md==@
`-- generated/
    |-- p2688r6.html
    `-- @==p2688r6.slides.html==@
```

```bash
make p2688r6.slides.html        # Build one presentation.
make slides                     # Build all presentations.

make serve p2688r6.slides.html  # Live server and rebuild one presentation
make serve slides               # Live server and rebuild all presentations
```

## Per-Paper Project Layout

- For `<paper>.md`, create a `<paper>.slides.md` in the paper directory.
- Outputs are written in that paper directory.

```{.embed_md}
wg21-papers/
|-- wg21/ (submodule)
`-- p2688/
    |-- Makefile
    |-- p2688r6.md
    |-- @==p2688r6.slides.md==@
    |-- p2688r6.html
    `-- @==p2688r6.slides.html==@
```

```bash
cd p2688
make p2688r6.slides.html
make slides

make serve p2688r6.slides.html
make serve slides
```

## Explicit Source-to-Output Mapping

- In the per-paper layout, `PAPER_RULE` maps a source stem to a paper number.
- A companion `<source>.slides.md` produces `<paper>.slides.html`.

:::::: columns
::: {.column width="50%"}
```{.embed_md}
wg21-papers/
|-- wg21/ (submodule)
`-- reflection/
    |-- Makefile
    |-- reflection.md
    |-- @==reflection.slides.md==@
    |-- p2996r13.html
    `-- @==p2996r13.slides.html==@
```
:::
::: {.column width="50%"}
```makefile {.embed_md}
# Makefile
@==PAPER_RULE := p2996r13:reflection==@
include ../wg21/paper.mk
```
:::
::::::

With this setup, you can run:

```bash
cd reflection
make p2996r13.slides.html  # Builds from `reflection.slides.md`
```

# Pandoc / Reveal.js Basics

## Presentation Title

::: {.render .slide .title-slide}
```yaml
---
title: "`MPark/WG21` Slides Guide"
subtitle: Pandoc Slideshows with Reveal.js
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
---
```
:::

This is the exact same title block format as for papers.

## Section Title

::: {.render .slide .section-slide}
``````
# Design
``````
:::

A level-one heading starts a section with a title slide.

## Content Slides

::: {.render .slide}
``````
## Syntax

The first slide in the Design section.

### Details

Lower-level headings remain within the current slide.
``````
:::

- A level-two heading starts a slide within the current section.
- Lower-level headings remain within the current slide.
- A horizontal rule starts a slide without a heading.

## Incremental Content

An `incremental` fenced div reveals its list items one at a time:

::: {.render .slide}
``````
## Building a Presentation

::: incremental

- Pandoc parses the Markdown.
- `MPark/WG21` applies its formatting.
- Reveal.js presents the result.

:::
``````
:::

A paragraph containing `. . .` inserts a pause between arbitrary blocks.

## Columns

::: {.render .slide}
``````
## Choosing a Representation

:::::: columns
::: {.column width="45%"}
### Requirements

- Explicit failure
- No allocation
:::

::: {.column width="55%"}
### Interface

```cpp
std::expected<T, E> parse(input);
```
:::
::::::
``````
:::

Pandoc's `columns` and `column` fenced divs create a multi-column slide.

## Speaker Notes

```markdown
::: notes
Remind the audience why this example matters.
:::
```

- Place a `notes` fenced div on a slide
- Pressing `S` during the presentation opens the Speaker View.

::: notes
This slide has real speaker notes as well as showing their Markdown source.
:::

# `MPark/WG21` Formatting Examples

## Wording Changes

::: {.render .slide}
``````
## Proposed Wording

- Add [new wording]{.add}.
- Remove [old wording]{.rm}.
- Replace [old wording](new wording){.sub}.
``````
:::

## Embedded Markdown in Code

::: {.render .slide}
``````
## Updating a Function Template

Syntax highlighting and wording markup can be mixed in the same code block:

```cpp
template <@[typename](class){.sub}@ T>
void f(@[int i]{.add}@, $T$ value);
```
``````
:::

## Comparison Tables

The `cmptable` fenced div places alternatives side by side.

::: {.render .slide}
``````
## Filtering and Transforming

::: cmptable

### Before
```cpp
std::vector<int> result;
for (int value : values) {
  if (even(value)) {
    result.push_back(square(value));
  }
}
```

### After
```cpp
auto result = values
  | std::views::filter(even)
  | std::views::transform(square);
```

:::
``````
:::

## Stable Names and Citations

::: {.render .slide}
``````
## Committee References

- Modify [basic.life] as follows.
- See [@P2688R6] for an example.
``````
:::

Paper citations are linked and collected into a *References* slide.

[Pandoc Slideshows]: https://pandoc.org/MANUAL.html#slide-shows
[Reveal.js]: https://revealjs.com/
