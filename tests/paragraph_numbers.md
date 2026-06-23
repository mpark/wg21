---
title: "Paragraph Number Tests"
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

# Paragraph Numbers

## Manual Paragraph Numbers

[2]{.pnum} An expression is _potentially evaluated_ unless it is an unevaluated
operand (7.2) or a subexpression thereof. The set of _potential results_ of
an expression `e` is defined as follows:

  - [2.1]{.pnum} If `e` is an `$id-expression$` (7.5.4), the set contains only `e`.
  - [2.2]{.pnum} If `e` is a subscripting operation (7.6.1.1) with an array operand,
    the set contains the potential results of that operand.

::: wording
[2]{.pnum} Explicitly pins the wording-local paragraph number to `2`.

[2.1]{.pnum} `[2.1]{.pnum}` explicitly pins the nested count.

[#.#]{.pnum} `[#.#]{.pnum}`{.default} automatically continues to `(2.2)`.

[#]{.pnum} `[#]{.pnum}`{.default} automatically continues to `3`.

[#.#]{.pnum} `[#.#]{.pnum}`{.default} automatically starts the nested count at `(3.1)`.

[2.#]{.pnum} `[2.#]{.pnum}`{.default} resets the nested count to `(2.1)`.

[x]{.pnum} `x` doesn't contribute to automatic numbering.

[x.#]{.pnum} `[x.#]{.pnum}`{.default} automatically starts the nested count at `(x.1)`.

[x.#]{.pnum} `[x.#]{.pnum}`{.default} automatically continues to `(x.2)`.

[x]{.pnum} `x` resets its own nested count.

[x.#]{.pnum} `[x.#]{.pnum}`{.default} automatically restarts at `(x.1)`.

[#.#]{.pnum} `[#.#]{.pnum}`{.default} returns to the numeric path and continues to `(3.1)`.

[#.x.#]{.pnum} `[#.x.#]{.pnum}`{.default} starts a literal nested path at `(3.x.1)`.

[#.x.#]{.pnum} `[#.x.#]{.pnum}`{.default} continues the literal nested path at `(3.x.2)`.

[#.#]{.pnum} `[#.#]{.pnum}`{.default} returns to the numeric nested count at `(3.2)`.
:::

::: wording
[4.2.5]{.pnum} Explicitly pins a deeper numeric path.

[#.x.#]{.pnum} `[#.x.#]{.pnum}`{.default} starts a separate literal nested path at `(4.x.1)`.

[#.x.#]{.pnum} `[#.x.#]{.pnum}`{.default} continues the literal nested path at `(4.x.2)`.

[#.#]{.pnum} `[#.#]{.pnum}`{.default} returns to the numeric nested count at `(4.3)`.
:::

## Automatic Paragraph Numbers

::: wording
#. `#.`{.default} automatically starts at `1`.
#. Another `#.`{.default} automatically continues to `2`.
   - Nested bullet list also gets automatic numbering. `(2.1)`.

     [...]

   5. Example of skipping. Pin to `5.`{.default}, yields `(2.5)`.
   - Continues to `(2.6)`.
     - Nested nested bullet list should just work `(2.6.1)`{.default}.

       [...]

     9. `9.`{.default} here will bring us to `(2.6.9)`{.default}.
     x) `x)`{.default} here will be `(2.6.x)`{.default}.
     x) Another `x)`{.default} here will also be `(2.6.x)`{.default}.
#. `#.`{.default} automatically continues to `3`.

   Also handle code blocks within a list item:
   ```cpp
   int main();
   ```
x) Use `x)`{.default} to skip a paragraph number.
x) Another `x)`{.default} assigned `x`.
#. `#.`{.default} automatically continues to `4`.

17. Pin with `17.`{.default}.

::: add
x) `x)`{.default} is mainly to skip numbering in `add`.
   - Nested bullet within an `x)`. This will be (x.1).
   x) Nested `x)` within an `x)`. This will be (x.x).
x) Second added paragraph.
:::

::: rm
#. `#.`{.default} here will be 18 after the skips.

24. Skip and pin again, e.g. `24.`{.default}.
:::

#. Automatically continue to 25.
:::
