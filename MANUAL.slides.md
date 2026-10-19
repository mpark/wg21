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

- With the [flat project layout], create a `<paper>.slides.md` alongside
  `<paper>.md` in the top-level directory.
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

make serve p2688r6.slides.html  # Launch live server for one presentation
make serve slides               # Launch live server for all presentations
```

## Per-Paper Project Layout

- With the [per-paper project layout], create a `<paper>.slides.md` alongside
  `<paper>.md` in the paper directory.
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
make p2688r6.slides.html        # Build one presentation.
make slides                     # Build all presentations.

make serve p2688r6.slides.html  # Launch live server for one presentation
make serve slides               # Launch live server for all presentations
```

## Explicit Source-to-Output Mapping

- In the [per-paper project layout], `PAPER_RULE` maps a source stem to a paper
  number.
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
make p2996r13.slides.html        # Build one presentation.
make slides                      # Build all presentations.

make serve p2996r13.slides.html  # Launch live server for one presentation
make serve slides                # Launch live server for all presentations
```

# Pandoc / Reveal.js Basics

## Presentation Title

Use the same [title metadata] as papers.

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

## Section Title

A [level-one heading][Headings] starts a section with a title slide.

::: {.render .slide .section-slide}
``````
# Design
``````
:::

## Content Slides

A level-two heading starts a slide within the current section:

::: {.render .slide}
``````
## Syntax

The first slide in the Design section.

### Details

Lower-level headings remain within the current slide.
``````
:::

- Lower-level headings remain within the current slide.
- A horizontal rule starts a slide without a heading.

## Incremental Content

An [`incremental` fenced div][Incremental Lists] reveals its list items one at
a time:

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

## Inserting Pauses

A [`. . .`][Inserting Pauses] within a slide hides the blocks that follow it
until the next advance:

::: {.render .slide}
``````
## Choosing an Approach

Start with the simplest design.

. . .

Add complexity only when evidence requires it.
``````
:::

## Columns

The [`columns` and `column` fenced divs][Columns] create a multi-column slide.

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

## Code Line Numbers

Use the same [code block] syntax as papers.

The `.numberLines`{.default} class displays line numbers. The
`startFrom`{.default} attribute sets the first displayed number.

::: {.render .slide}
``````
## Parsing Input

```{.cpp .numberLines startFrom=7}
auto parse(std::string_view input)
    -> std::expected<value, $parse_error$> {
  if (input.empty())
    return std::unexpected(parse_error::empty_input);
  return value{input};
}
```
``````
:::

See [Line Numbers & Highlights] in the Reveal.js documentation.

## Code Line Highlighting

For slides, the `numberLines`{.default} attribute highlights and steps through
lines.

It can be a single line like `2`{.default}, a range like `4-5`{.default}, or a
comma-delimited group like `2,4-5`{.default}.

These are one-based positions within the block, independent of the displayed
`startFrom`{.default} value.

::: {.render .slide}
``````
## Parsing Input

```{.cpp numberLines="2,4-5" startFrom=7}
auto parse(std::string_view input)
    -> std::expected<value, $parse_error$> {
  if (input.empty())
    return std::unexpected(parse_error::empty_input);
  return value{input};
}
```
``````
:::

See [Line Numbers & Highlights] in the Reveal.js documentation.

## Stepped Code Highlighting

Separate each step with `|`{.default} to animate the highlights.

::: {.render .slide}
``````
## Parsing Input

```{.cpp numberLines="1-2|3-4|5-6" startFrom=7}
auto parse(std::string_view input)
    -> std::expected<value, $parse_error$> {
  if (input.empty())
    return std::unexpected(parse_error::empty_input);
  return value{input};
}
```
``````
:::

See [Step-by-step Highlights] in the Reveal.js documentation.

::: {.render .slide .animation}
## Reveal.js Auto-Animation

- Place `data-auto-animate=`{.default} on adjacent headings and
  `data-id`{.default} on corresponding code blocks.
- See [Auto-Animate Settings] for the other
  `data-auto-animate-*`{.default} options.

``````
## Rectangle {data-auto-animate=}

```{.cpp .numberLines data-id="code-animation"}
struct rectangle {
  double width, height;
};
```

## Rectangle {data-auto-animate=}

```{.cpp .numberLines data-id="code-animation"}
struct rectangle {
  double width, height;

  constexpr auto area() const { return width * height; }
};
```

## Rectangle {data-auto-animate=}

```{.cpp .numberLines data-id="code-animation"}
struct rectangle {
  double width, height;

  constexpr auto area() const { return width * height; }
  constexpr auto perimeter() const { return 2 * (width + height); }
};
```
``````
:::

## Speaker Notes

Place a [`notes` fenced div][Speaker Notes] on a slide:

```markdown
::: notes
Remind the audience why this example matters.
:::
```

Press `S` during the presentation to open the Speaker View.

::: notes
This slide has real speaker notes as well as showing their Markdown source.
:::

# `MPark/WG21` Formatting Examples

## Wording Changes

The paper framework's [modifying text] syntax works unchanged in slides.

::: {.render .slide}
``````
## Proposed Wording

- Add [new wording]{.add}.
- Remove [old wording]{.rm}.
- Replace [old wording](new wording){.sub}.
``````
:::

## Embedded Markdown in Code

See [Embedded Markdown] in the user's guide for the complete syntax.

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

The [`cmptable` fenced div][Comparison Tables] places alternatives side by
side.

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

[Stable names] link to the working draft. [Citations] are linked and collected
into a *References* slide.

::: {.render .slide}
``````
## Committee References

- Modify [basic.life] as follows.
- See [@P2688R6] for an example.
``````
:::

[Pandoc Slideshows]: https://pandoc.org/MANUAL.html#slide-shows
[Reveal.js]: https://revealjs.com/
[Incremental Lists]: https://pandoc.org/MANUAL.html#incremental-lists
[Inserting Pauses]: https://pandoc.org/MANUAL.html#inserting-pauses
[Columns]: https://pandoc.org/MANUAL.html#columns
[Speaker Notes]: https://pandoc.org/MANUAL.html#speaker-notes
[flat project layout]: https://mpark.github.io/wg21/MANUAL.html#flat-project-layout
[per-paper project layout]: https://mpark.github.io/wg21/MANUAL.html#per-paper-project-layout
[title metadata]: https://mpark.github.io/wg21/MANUAL.html#title
[Headings]: https://mpark.github.io/wg21/MANUAL.html#headings
[code block]: https://mpark.github.io/wg21/MANUAL.html#code-block
[modifying text]: https://mpark.github.io/wg21/MANUAL.html#modifying-text
[Embedded Markdown]: https://mpark.github.io/wg21/MANUAL.html#embedded-markdown
[Comparison Tables]: https://mpark.github.io/wg21/MANUAL.html#comparison-tables
[Stable names]: https://mpark.github.io/wg21/MANUAL.html#stable-names
[Citations]: https://mpark.github.io/wg21/MANUAL.html#citations
[Line Numbers & Highlights]: https://revealjs.com/code/#line-numbers-highlights
[Step-by-step Highlights]: https://revealjs.com/code/#step-by-step-highlights
[Auto-Animate Settings]: https://revealjs.com/auto-animate/#animation-settings
