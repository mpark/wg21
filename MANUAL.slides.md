---
title: Slides with MPark/WG21
subtitle: Reveal.js Presentations from Markdown
author: Michael Park
date: today
highlighting:
  keywords:
    cpp: match
---

# Getting Started

## Use Either Project Layout

Presentations work with both `flat.mk` and `paper.mk`.

Name the source `*.slides.md`:

```text
p2688r5.slides.md → p2688r5.slides.html
```

The flat layout writes the result under `generated/`; the per-paper layout
writes it alongside the source.

## Title Slide Metadata

```yaml
title: Pattern Matching
subtitle: A Design for C++
author: Michael Park
date: today
```

These elements form the title slide. This presentation's title slide is built
the same way.

## Build and Serve

```bash
make p2688r5.slides.html       # Build one presentation.
make slides                   # Build every presentation.
make serve p2688r5.slides.html
make serve slides
```

`make html` remains a separate target for papers.

## Explicit Source Mapping

`PAPER_RULE` maps a paper source and its companion slide source to the same
paper number.

```{.embed_md}
wg21-papers/
|-- wg21/ (submodule)
`-- reflection/
    |-- Makefile
    |-- reflection.md
    |-- @==reflection.slides.md==@
    |-- p2996r13.html
    `-- p2996r13.slides.html
```

```makefile
PAPER_RULE := p2996r13:reflection
include ../wg21/paper.mk
```

```bash
make p2996r13.slides.html
```

# Structuring a Presentation

## Sections and Slides

```markdown
# Design

## Syntax

The first slide in the Design section.

## Semantics

The next slide in the Design section.
```

Level-one headings start sections; level-two headings start slides within
those sections.

## Speaker Notes

```markdown
::: notes
Remind the audience why this example matters.
:::
```

Place a `notes` fenced div on a slide, then press `S` during the presentation
to open the Reveal.js speaker view.

::: notes
This slide has real speaker notes as well as showing their Markdown source.
:::

## Reveal.js Features

Standard Pandoc and Reveal.js authoring remains available. For example, an
incremental list reveals one item at a time:

::: incremental

- Pandoc parses the Markdown.
- MPark/WG21 applies its formatting.
- Reveal.js presents the result.

:::

# The WG21 Authoring Toolbox

## Paper Features Carry Over

Presentations can reuse the features that are useful when explaining a paper:

- C++ syntax highlighting and custom keywords,
- wording additions, removals, and substitutions,
- embedded Markdown inside code,
- comparison tables,
- stable-name links and paper citations, and
- wording paragraphs, examples, and notes.

## Wording Changes

::: render
`Add [new wording]{.add}.`
`Remove [old wording]{.rm}.`
`Replace [old wording](new wording){.sub}.`
:::

## Embedded Markdown in Code

The source can mix syntax highlighting with wording markup:

``````render
```cpp
template <@[typename](class){.sub}@ T>
void f(@[int i]{.add}@, $T$ value);
```
``````

There is no need to maintain a second, manually highlighted copy of the code.

## Comparison Tables

::: cmptable

### Before
```cpp
switch (x) {
  case 0: zero(); break;
  default: other();
}
```

### After
```cpp
x match {
  0 => zero();
  _ => other();
};
```

:::

## Committee Links

::: render
`Modify [basic.life] as follows.`
`See [@P2688R5] for an example.`
:::

Paper citations are linked and collected into a References slide.

# Sharing the Result

## Reproducible and Standalone

- The framework downloads a pinned, verified Reveal.js release.
- Node.js and `npm` are not required.
- Reveal.js, the theme, and other resources are embedded in the output.
- The resulting `.slides.html` file can be shared on its own.

## Learn More

- [MPark/WG21 User's Guide](https://github.com/mpark/wg21/blob/master/MANUAL.md)
- [This presentation's source](https://github.com/mpark/wg21/blob/master/MANUAL.slides.md)
- [Pandoc slide shows](https://pandoc.org/MANUAL.html#slide-shows)
- [Reveal.js documentation](https://revealjs.com/)
