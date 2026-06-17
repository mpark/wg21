---
title: "`MPark/WG21` User's Guide"
subtitle: "Framework for Writing C++ Committee Proposals"
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
toc-depth: 4
---

# Introduction

[`MPark/WG21`](https://github.com/mpark/wg21) is a framework for writing
proposals for the C++ Standards Committee, built on top of [Pandoc](https://pandoc.org).

In short, you write **Markdown** and the framework produces the paper either in
**HTML** or **PDF** (via LaTeX).

The framework provides Markdown extensions that are specifically useful for C++ proposals.
Including, but not limited to:

  - [Modifying Wording Text][Modifying Text]
  - [Embedded Markdown in Code][Embedded Markdown]

# Goals

There are two goals for this framework, not necessarily in order:

  - Ease of **authoring** papers
  - Ease of **reviewing** papers

# Getting Started

## Requirements

The framework downloads and maintains a pinned version of Pandoc.

For HTML output, only the following dependencies are required:

  - `git`
  - `curl`
  - `make`
  - `python3`
  - `python3-venv`

For PDF output, the framework also depends on `xelatex`.

### macOS

```bash
brew install python make

# For PDF output
brew install --cask mactex
```

### Ubuntu

```bash
sudo apt-get install git curl make python3 python3-venv

# For PDF output
sudo apt-get install texlive-xetex
```

### Debian

```bash
sudo apt-get install git curl make python3 python3-venv

# For PDF output
sudo apt-get install texlive-xetex \
                     texlive-fonts-recommended \
                     texlive-latex-recommended \
                     texlive-latex-extra
```

## Integration

Add this repository to your paper repository as a git submodule:

```bash
git submodule add https://github.com/mpark/wg21.git
```

Then include the framework `Makefile` from your repository's top-level `Makefile`:

```make
include wg21/Makefile
```

Markdown files in the repository root become build targets. For example,
`P0000R0.md` can be built as `generated/P0000R0.html` or `generated/P0000R0.pdf`.

See [mpark/wg21-papers](https://github.com/mpark/wg21-papers) for an example use of this project.

## Generation

Given a `P0000R0.md` at the top-level of your repository:

```bash
make generated/P0000R0.html  # HTML Output
make generated/P0000R0.pdf   # PDF Output
```

For convenience, the `Makefile` also accepts:

```bash
make P0000R0.html  # HTML Output
make P0000R0.pdf   # PDF Output
```

In both cases, the output is written under `generated/`.

# Formatting

This framework provides support for various common elements for C++ proposals.

## Title

The title is specified in a [YAML metadata block](https://pandoc.org/MANUAL.html#extension-yaml_metadata_block).

For example, the [title](#title-block-header) of this document is generated from:

```yaml
---
title: Framework for Writing C++ Committee Proposals
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
---
```

[`date: today` generates today's date in `YYYY-MM-DD` (ISO 8601) format.]{.note}

YAML lists can be used to specify multiple audiences and authors:

```diff
  ---
  title: Framework for Writing C++ Committee Proposals
  document: D0000R0
  date: today
- audience: WG21
+ audience:
+   - Library Evolution Working Group
+   - Library Working Group
  author:
    - name: Michael Park
      email: <mcypark@gmail.com>
+   - name: Barry Revzin
+     email: <barry.revzin@gmail.com>
---
```

## Table of Contents

By default, a table of contents is generated. For an example, see the
[table of contents](#toctitle) of this document.

### Metadata: `toc`

To disable the table of contents entirely, set the `toc` metadata to `false`.

```yaml {.embed_md}
---
title: Framework for Writing C++ Committee Proposals
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
@==toc: false==@
---
```

### Metadata: `toc-depth`

The default depth of table of contents is `3`. That is, given headers like

```
# Design Overview

## Types of Patterns

### Primary Patterns

#### Wildcard Pattern
```

The table of contents will not show `#### Wildcard Pattern`{.default} since it's 4 levels deep.

To set the depth manually, set `toc-depth` to the desired number.\
For example, to make `#### Wildcard Pattern`{.default} show up:

```yaml {.embed_md}
---
title: Framework for Writing C++ Committee Proposals
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
@==toc-depth: 4==@
---
```

## Headings

Both Setext and ATX styles are available:

+-----------------+-----------------------------+
| Markdown Source | Rendered Output             |
+=================+=============================+
| ```             |                             |
| Header 1        | Header 1 {- .unlisted}      |
| ========        | ========                    |
| ```             |                             |
+-----------------+-----------------------------+
| ```             |                             |
| Header 2        | Header 2 {- .unlisted}      |
| --------        | --------                    |
| ```             |                             |
+-----------------+-----------------------------+
| ```             |                             |
| ### Header 3    | ### Header 3 {- .unlisted}  |
| ```             |                             |
+-----------------+-----------------------------+
| ```             |                             |
| #### Header 4   | #### Header 4 {- .unlisted} |
| ```             |                             |
+-----------------+-----------------------------+

### Disable from Section Numbering: `-` or `.unnumbered` {#disable-section-number}

Add the `-` or `.unnumbered` class to a header to exclude it from section numbering,
using the Pandoc extension [`header_attributes`]:

```md {.embed_md}
# Miscelleneous {@==-==@}
```

### Exclude from Table of Contents: `.unlisted` {#exclude-from-toc}

Add the `.unlisted` class **in addition to** `-` or `.unnumbered` to a header to
exclude it from the table of contents, using the Pandoc extension: [`header_attributes`]:

```md {.embed_md}
# Miscelleneous {- @==.unlisted==@}
```

### Implicit Header References

::: render
```
Given a heading like:

## Algorithm Return Type {- .unlisted}

Reference with any of the following ways:

  - [Algorithm Return Type]
  - [Algorithm Return Type][]
  - [Custom Text 1][Algorithm Return Type]
  - [Custom Text 2](#algorithm-return-type)
```
:::

The `#algorithm-return-type`{.default} identifier is automatically generated by
the Pandoc extension: [`auto_identifiers`].

Relevant Pandoc extensions: [`implicit_header_references`], [`shortcut_reference_links`]

[`shortcut_reference_links`]: https://pandoc.org/MANUAL.html#extension-shortcut_reference_links

### Header References by ID with Automatic Text

This extension interprets `[](#header-identifier)`{.default} as a reference to
a header where the heading text is automatically used.

The main usage is to first specify an explicit identifier on a header, like:

```md {.embed_md}
## Algorithm Return Type @=={#return-type}==@
```

then refer to it like `[](#return-type)`{.default}, which will be rendered as: Algorithm Return Type.

The main advantage is that when the header text changes, the reference
remains stable and the new heading text is automatically rendered.

[`header_attributes`]: https://pandoc.org/MANUAL.html#extension-header_attributes
[`implicit_header_references`]: https://pandoc.org/MANUAL.html#extension-implicit_header_references
[`auto_identifiers`]: https://pandoc.org/MANUAL.html#extension-auto_identifiers

## Inline Formatting

### Emphasis

Use asterisks (`*`) and underscores (`_`) to emphasize inline text.

::: render
`Some of these words *are emphasized*.`
`Some of these words _are emphasized also_.`
`Use two asterisks for **strong emphasis**.`
`Or, __use two underscores instead__.`
:::

For emphasizing **part** of a word, asterisks are **required**.

::: render
`feas**ible**, not feas__able__`
:::

This is the Pandoc extension: [`intraword_underscores`].

[`intraword_underscores`]: https://pandoc.org/MANUAL.html#extension-intraword_underscores

### Superscript, Subscript

Wrap caret (`^`) for superscripts and tilde (`~`) for subscripts.

::: render
`2^10^ is 1024`
`` `constexpr`~opt~ means optional``
:::

This is the Pandoc extension: [`superscript_subscript`].

[`superscript_subscript`]: https://pandoc.org/MANUAL.html#extension-superscript-subscript

### Highlighting

Wrap `==`, or use `[highlighted text]{.mark}`{.default} to highlight some text.

::: render
`This is a ==highlighted **text**==.`
`Also, [highlight *text*]{.mark}`
:::

## Wording

### Modifying Text

Small, inline changes are [bracketed `Span` elements][divspan] that look like the following:

::: render
`Let's add some [new **text**]{.add}.`
`Remove some [old *text*]{.rm} now.`
`Substitute: [old *text*](new **text**){.sub}`
:::

[Substitutions are essentially just shorthand for `[old text]{.rm}[new text]{.add}`{.default}.]{.note}

```render
The optional *attribute-specifier-seq* appertains to the [label](*general-label*){.sub}.
The only use of a [label with an *identifier*](*label*){.sub} is as the target of
a `goto`, [`break`, or `continue`]{.add}. No two [label](*label*){.sub}s in a function
shall have the same *identifier*. A [label](*general-label*){.sub} can be used
[in a `goto` statement]{.rm} before its introduction by a *labeled-statement*.
```

Large changes are [fenced `Div` blocks][divspan] with `::: add`{.default} for
additions, `::: rm`{.default} for removals, and close with `:::`{.default}.

```render
Modify section [format.functions]{.sref}

::: add
> ```
> template<class... Args>
>   string format(const locale& loc, string_view fmt, const Args&... args);
> ```
>
> *Returns*: `vformat(loc, fmt, make_format_args(args...))`.
:::
```

```render
Remove [expr.post.incr]{.sref}/2:

::: rm
> The operand of postfix `--` is decremented analogously to the postfix `++` operator.
>
> [For prefix increment and decrement, see [expr.pre.incr].]{.note} 
:::
```

[divspan]: https://pandoc.org/MANUAL.html#divs-and-spans

### Paragraph Numbers

#### Paragraph Number Element: `.pnum`

Paragraph number elements are [bracketed `Span` elements][divspan] that look
like: `[2]{.pnum}` and `[2.1]{.pnum}`.

```render
[1]{.pnum} In this subclause, "before" and "after" refer to the "happens before"
relation ([intro.multithread]).

[2]{.pnum} The *lifetime* of an object or reference is a runtime property of
the object or reference. [...]

  - [2.1]{.pnum} storage with the proper alignment and size for type `T` is obtained, and

    [...]

  - [2.4]{.pnum} if `T` is a class type, the destructor call starts, or
  - [2.5]{.pnum} the storage which the object occupies is released, or is reused by
    an object that is not nested within _o_ ([intro.object]).

[...]

::: add
[x]{.pnum} Some new paragraph here
:::

[6]{.pnum} A program may end the lifetime of an object of class type without
invoking the destructor, by reusing or releasing the storage as described above.
```

Within `::: wording`{.default}, use `#`{.default} within a paragraph number element to
automatically fill in that part. For example:

```render
::: wording
[#]{.pnum} Automatically starts at 1.

[5]{.pnum} Existing paragraph pinned at 5.

[#]{.pnum} Automatically continues to 6.

[#.#]{.pnum} Automatically starts a nested numbering at (6.1).

::: add
[x]{.pnum} Added paragraph that does not affect the next automatic number.
:::

[#]{.pnum} Automatically continues to 7.
:::
```

The automatic numbering resets for each `::: wording`{.default} div.

#### List-based Paragraphs (Experimental)

List-based paragraphs are list elements (
[`ordered_lists`](https://pandoc.org/MANUAL.html#ordered-lists) and
[`bullet_lists`](https://pandoc.org/MANUAL.html#bullet-lists)), within
a [bracketed `Div` element][divspan], `::: wording`{.default}.

At the top-level, use `#.`{.default} for automatic numbering, and `1.` for pinned numbering. For example:

```render
::: wording
#. In this subclause, "before" and "after" refer to the "happens before" relation
   ([intro.multithread]).
#. The *lifetime* of an object or reference is a runtime property of the object
   or reference. [...]

[...]

6. A program may end the lifetime of an object of class type without invoking
   the destructor, by reusing or releasing the storage as described above.
:::
```

Use nested bullet lists for sublists which are also automatically numbered, and
`1.` for partial pinning. For example, if we pin `3.` within paragraph `2`,
partial pinning will work out to `(2.3)`.

```render
::: wording
#. In this subclause, "before" and "after" refer to the "happens before" relation
   ([intro.multithread]).
#. The *lifetime* of an object or reference is a runtime property of the object
   or reference. [...]

   - storage with the proper alignment and size for type `T` is obtained, and

     [...]

   4. if `T` is a class type, the destructor call starts, or
   - the storage which the object occupies is released, or is reused by
     an object that is not nested within _o_ ([intro.object]).

[...]

6. A program may end the lifetime of an object of class type without invoking
   the destructor, by reusing or releasing the storage as described above.
:::
```

Lastly, use `x.` to mark a paragraph number `x`. This is most useful within an `::: add`
block where you want to insert new paragraphs without having to manually shift the numbers.

```render
::: wording
#. In this subclause, "before" and "after" refer to the "happens before" relation
   ([intro.multithread]).
#. The *lifetime* of an object or reference is a runtime property of the object
   or reference. [...]

   - storage with the proper alignment and size for type `T` is obtained, and

     [...]

   4. if `T` is a class type, the destructor call starts, or
   - the storage which the object occupies is released, or is reused by
     an object that is not nested within _o_ ([intro.object]).

[...]

::: add
x. Some new paragraph here
:::

6. A program may end the lifetime of an object of class type without invoking
   the destructor, by reusing or releasing the storage as described above.
:::
```

::: note
In order to nest content (code blocks, nested list, etc) properly within another list,
be sure to add a blank line and indent to line up with the first non-space character after
the list marker. See Pandoc extension: [`block_content_in_list_items`](https://pandoc.org/MANUAL.html#block-content-in-list-items).

::: example
+------------------------------------------------+-------------------------------------------------+
| Preceding blank line                           | Indent to line up                               |
+================================================+=================================================+
| ``````                                         | ```                                             |
| #. Some paragraph                              | #. @==S==@ome paragraph                         |
| @==\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ ==@ |    @==\ ==@                                     |
|    ```                                         |    @==`==@``                                    |
|    code                                        |    @==c==@ode                                   |
|    ```                                         |    @==`==@``                                    |
| ``````                                         | ```                                             |
+------------------------------------------------+-------------------------------------------------+
:::

For nested lists, the blank line may be omitted:

::: example
```
#. @==S==@ome paragraph
   @==-==@ Nested bullet list
```
:::
:::

### Code Changes

Code changes can be either shown in a `diff` code block like so:

``````render
```diff
  template <size_t I, class T1, class T2>
-   constexpr typename tuple_element<I, pair<T1, T2>>::type&
+   constexpr tuple_element_t<I, pair<T1, T2>>&
      get(pair<T1, T2>&) noexcept;
```
``````

Alternatively, [Embedded Markdown] can be used to show the changes inline:

``````render
```
template <size_t I, class T1, class T2>
  constexpr @[typename]{.rm}@ tuple_element@[_t]{.add}@<I, pair<T1, T2>>@[::type]{.rm}@&
    get(pair<T1, T2>&) noexcept;
```
``````

[For inline changes like this, prefer no-syntax-highlighting by using ` ``` `{.default} to avoid too many colors.]{.note}

### Examples

Smaller, inline examples are [bracketed `Span` elements][divspan] that looks like `[example text]{.example}`.

```render
[`T x = T(T(T()));` value-initializes `x`.]{.example}
```

Large examples are [fenced `Div` blocks][divspan] with `::: example`.

::: render
``````
::: example
A simple example of a class definition is

```cpp
struct tnode {
  char tword[20];
  int count;
  tnode* left;
  tnode* right;
};
```
:::
``````
:::

### Notes

Smaller, inline notes are [bracketed `Span` elements][divspan] that looks like `[note text]{.note}`.

```render
[Padding bits have unspecified value, but cannot cause traps.]{.note}
```

Large notes are [fenced `Div` blocks][divspan] with `::: note`.

``````render
::: note
An expression of type "*cv1* `T`" can initialize an object of type "*cv2* `T`"
independently of the cv-qualifiers *cv1* and *cv2*.

```cpp
int a;
const int b = a;
int c = b;
```
:::
``````

Use `ednote` for editorial notes:

::: render
```
[This is a drive-by fix.]{.ednote}
```
:::

```render
::: ednote
Throughout the wording, we say that a reflection (an object of type `std::meta::info`)
represents some source construct, while splicing that reflection designates that source
construct. For instance, `^^int` represents the type `int` and `[: ^^int :]` designates
the type `int`.
:::
```

Use `draftnote` for drafting notes:

```render
[An `audience` attribute addresses a specific audience]{.draftnote audience="the reader"}
```

```render
::: draftnote
We don’t think we have to change anything here, since if `E` is a *splice-specifier*
that can be interpreted as a *splice-expression*, the requirements already fall out
based on how paragraphs 1 and 3 are already worded
:::
```

To specify an audience for the [fenced `Div` block][divspan], you'll need `::: {.draftnote audience="the reader"}`.

Finally, in the relatively common situation where an example appears within a note, you can simply nest them:

``````render
::: note
The declaration of a class name takes effect immediately after the *identifier*
is seen in the class definition or *elaborated-type-specifier*.

::: example
```cpp
class A * A;
```
first specifies `A` to be the name of a class and then redefines it as the name of
a pointer to an object of that class. This means that the elaborated form `class A`
must be used to refer to the class. Such artistry with names can be confusing and
is best avoided.
:::
:::
``````

### Grammar

Use [line blocks][lineblock] (`|`) in order to preserve the leading spaces.

[lineblock]: https://pandoc.org/MANUAL.html#line-blocks

```render
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

## Code

### Inline Code

Use backticks like `` `int x = 0;` ``{.default} for inline code.

We can use the Pandoc extension [`inline_code_attributes`](https://pandoc.org/MANUAL.html#extension-inline_code_attributes)
to specify which language should be used for syntax highlighting:

::: render
`` `auto value = std::format("{}", bar);`{.cpp}``
`` `let value = format!("{bar}");`{.rust}``
`` `value = f"{bar}"`{.python}``
:::

[**Inline Code gets C++ syntax highlighting by default.**]{.note}

Since we're writing a C++ proposal, many, if not most of the inline code will be C++.
Adding the `{.cpp}`{.default} attribute everywhere can become very verbose, very fast.
Thus, inline code is implicitly interpreted as `{.cpp}`{.default}. For example,
`` `int x = 0;` ``{.default} is implicitly `` `int x = 0;`{.cpp}``{.default}.


For no-syntax-highlighting, use `{.default}`{.default} like `` `int x = 0;`{.default}``{.default}.

::: render
`` `constexpr int x = 0;` ``
`` `constexpr int x = 0;`{.default}``
:::

### Code Block

Use three or more backticks to start a code block.

::: render
``````
```
int main() {
  return 0;
}
```
``````
``````
```cpp
int main() {
  return 0;
}
```
``````
:::

[Unlike [Inline Code], code blocks are not implicitly C++.]{.note}

Add the `.numberLines` class to a code block to number the lines, and
the `startFrom=N` attribute to specify the starting number, using the Pandoc extension:
[`fenced_code_attributes`](https://pandoc.org/MANUAL.html#extension-fenced_code_attributes).

::: render
``````
```cpp {.numberLines}
int main() {
  return 0;
}
```
``````
``````
```cpp {.numberLines startFrom=8}
int main() {
  return 0;
}
```
``````
:::

### Embedded Markdown

Code in C++ proposals often needs small pieces of wording markup inside it.
With embedded Markdown enabled, text surrounded by `@`{.default} is parsed as
Markdown and then placed back into the code element. This is useful for
italicized terms, exposition-only names, [modifying text], and [stable names].

Embedded Markdown is **enabled by default** for C++ and no-syntax-highlighting code.
This is essentially:

  - Inline code such as `` `code` ``{.default}, `` `code`{.cpp}``{.default}, `` `code`{.default}``{.default}, and
  - Code blocks that start with either ` ``` `{.default}, ` ```cpp`{.default}, or ` ```default`{.default}

```render
Recall the `static_cast` syntax: `static_cast < @*type-id*@ > ( @*expression*@ )`.
```

Because italicized wording terms are so common, `@==$==@text@==$==@`{.default em=none} is provided as
a shorthand for `%==@*==%text%[*@]{.mark}%`{.default md=% em=none}.

```render
Recall the `static_cast` syntax: `static_cast < $type-id$ > ( $expression$ )`.
```

A more elaborate example with [modifying text]:

``````render
```cpp
template <@[invocable](class){.sub}@ F@[, class]{.add}@>
struct $as-receiver$ {
@[private:]{.rm}@
  @[using invocable_type = std::remove_cvref_t<F>;]{.rm}@
  @[invocable_type](F){.sub}@ f_;
@[public:]{.rm}@
  @[explicit *as-receiver*(invocable_type&& f)]{.rm}@
  @[*as-receiver*(*as-receiver*&& other) = default;]{.rm}@
  void set_value() @[noexcept(is_nothrow_invocable_v<F&>)]{.add}@ {
    invoke(f_);
  }
  @[[[noreturn]]]{.add}@ void set_error(std::exception_ptr) @[noexcept]{.add}@ {
    terminate();
  }
  void set_done() noexcept {}
};
```
``````

#### Code within Embedded Markdown

Suppose we want to **add** a parameter `int i` to a function `f`:

::: render
``````
```cpp
void f(@[int i]{.add}@);
```
``````
:::

This is perfectly fine, and quite intuitive. However, consider if the parameter
is something more complicated, like `$foo$ *const *ptr`:

::: render
``````
```cpp
void f(@[*foo* *const *ptr]{.add}@);
```
``````
:::

Now, the pointers have disappeared and `const` is italicized. This is because
the **full text** within `@`{.default} is treated as Markdown, which is exactly
what we want for `*foo*` for example. It's just not want we want for
the `*const *` part of it.

There are a couple of ways to resolve this issue:

1. Introduce an **inline code within the embedded Markdown**:

   ``````render
   ```cpp
   void f(@[`$foo$ *const *ptr`]{.add}@);
   ```
   ``````

   Given that `` `$foo$ *const *ptr` ``{.default .raw} is exactly how it would be written if
   we were writing inline code, this is a decent solution.

   However, this approach can't really handle markup more complicated than italicizing
   because the parsing of `@`{.default} is extremely naive in its current implementation.

2. **Escape the special Markdown characters** that you want interpreted literally.
   Any symbol can be escaped with a backslash like `\*`, and is interpreted literally
   by the Pandoc extension: [`all_symbols_escapable`](https://pandoc.org/MANUAL.html#extension-all_symbols_escapable).

   ``````render
   ```cpp
   void f(@[*foo* \*const \*ptr]{.add}@);
   ```
   ``````

   This approach can handle more complicated markup requirements.
   For example, if `foo` needed to be bolded instead, we can just do:

   ``````render
   ```cpp
   void f(@[**foo** \*const \*ptr]{.add}@);
   ```
   ``````

#### Opt-out for Default Languages: `.raw`

Add the `.raw` class to opt-out of embedded Markdown, using Pandoc extensions
[`inline_code_attributes`] or [`fenced_code_attributes`].

One example of a problem involving emails:

::: render
``````
```cpp {.raw}
auto emails = { "a@mail.com", "b@mail.com" };
```
``````
``````
```cpp
auto emails = { "a@mail.com", "b@mail.com" };
```
``````
:::

The `@`{.default} characters "disappear" without the `.raw` class because the
text between the two `@`{.default}, `domain.com", "bar` is parsed as Markdown,
and placed back into the full range of `@domain.com", "bar@`{.default .raw}.

#### Opt-in for Other Languages: `.embed_md` {#embed_md}

Add the `.embed_md` class to opt-in for embedded Markdown, using Pandoc extensions
[`inline_code_attributes`] or [`fenced_code_attributes`].

::: render
``````
```rust
fn main() {
    @**println**@!("hello!");
}
```
``````
``````
```rust {.embed_md}
fn main() {
    @**println**@!("hello!");
}
```
``````
`` `s.trim_@[left](start){.sub}@()`{.rust}``
`` `s.trim_@[left](start){.sub}@()`{.rust .embed_md}``
:::

[`inline_code_attributes`]: https://pandoc.org/MANUAL.html#extension-inline_code_attributes
[`fenced_code_attributes`]: https://pandoc.org/MANUAL.html#extension-fenced_code_attributes

#### Overriding the Delimiters: `md`, `em`

The final escape hatch, is to change the default Markdown and italics delimiters
from `@`{.default} and `$`{.default} respectively, to something else.

Add the attribute `md=<symbol>|none` to set the Markdown delimiter or disable,
and `em=<symbol>|none` to set the italics delimiter or disable.

Consider this `bash` example:

``````render
```bash
rsync -av "$@" "deploy@$target:/srv/app/"
```
``````

If we want to bold the `"$@"` for example, we need to enable embedded Markdown.
However, the two occurences each of `@`{.default} and `$`{.default}
make the default delimiters (`@`{.default} and `$`{.default}) unusable.
In this example, we set the Markdown delimiter to be `%`{.default} instead,
and disable the italics delimiter entirely.

``````render
```bash {md=% em=none}
rsync -av %**"$@"**% "deploy@$target:/srv/app/"
```
``````

[Effectively, `.embed_md` is `md=@ em=$`{.default} and `.raw` is `md=none em=none`.]{.note}

## Comparison Tables

Comparison Tables are [fenced `Div` blocks][divspan] that open with `::: cmptable`
and close with `:::`. [Fenced code blocks][code] are the only elements that
actually get added to Comparison Tables, except that the last header (if any)
before a [fenced code block][code] is attached to the cell above.

[code]: https://pandoc.org/MANUAL.html#fenced-code-blocks

**Markdown Source**

``````markdown
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
``````

**Rendered Output**

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

Each [fenced code block][code] is pushed onto the current row, and
horizontal rules (`---`) are used to move to the next row.

**Markdown Source**

``````md
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
s match {
  "foo" => do { std::cout << "got foo" };
  "bar" => do { std::cout << "got bar" };
  _ => do { std::cout << "don't care" };
};
```

:::
``````

**Rendered Output**

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
s match {
  "foo" => do { std::cout << "got foo" };
  "bar" => do { std::cout << "got bar" };
  _ => do { std::cout << "don't care" };
};
```

:::


The last block quote `> caption` (if any) is used as the caption.

**Markdown Source**

``````md
::: cmptable

> Put your caption here

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
``````

**Rendered Output**

::: cmptable

> Put your caption here

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

## Stable Names

Stable names come in two flavors: *explicit* and *implicit* .

[Run `make update` to re-fetch and update the local databases, including stable names.]{.note}

### Implicit Stable Names

*Implicit* stable names are [`shortcut_reference_links`] such as `[basic.life]`,
and automatically links to <https://eel.is/c++draft/basic.life>.
This is typically used in quoting standard paragraphs like this:

```render
> [...] whose lifetime has begun and has not ended ([basic.life]).
```

[Under the hood, `[basic.life]` expands to `[basic.life]{- .sref}` (See [Explicit Stable Names]).]{.note}

### Explicit Stable Names

*Explicit* stable names are [bracketed `Span` elements][divspan] that look like:
`[stable.name]@=={.sref}==@`{.default}. A leading section number is rendered
automatically. This is typically used to describe the section to be modified:

::: render
```
Modify section [basic.life]{.sref}:
```
:::

Add the `.title` class in addition to `.sref`, to also render the section title
of the stable name, like: `[stable.name]{.sref @==.title==@}`{.default}.
This is typically used as a header in wording:

::: render
```
## [basic.life]{.sref .title} {- .unlisted}
```
:::

[The `{- .unlisted}`{.default} is applied to the header itself, to
[disable the section numbering](#disable-section-number) and to
[exclude it from the table of contents](#exclude-from-toc)]{.note}

Lastly, you may also add the class `-` or `.unnumbered` to `.sref` to omit
the section number. This is mostly for completeness, as something like
`[basic.life]{- .sref}` can be written simply as `[basic.life]`. You can also
use this to render *only* the section title without the section number like:

::: render
```
[basic.life]{- .sref .title}
```
:::

### Paragraph Link

A suffix `/pnum`{.default} can be added to link to a specific paragraph number,
where `pnum` is a dot-separated integers like `1` or `2.1`.

::: render
```
Refer to a specific paragraph [basic.life]/1:
```
```
Change [basic.life]{.sref}/2.1 as follows:
```
:::

## Citations

In-text citations look like this: `[@paper]`{.default}

```render
This is a proposal for a reduced initial set of features to support static
reflection in C++. Specifically we are mostly proposing a subset of features
suggested in [@P1240R2].
```

You may also include the title of the paper by adding the `.title` class,
like `[@paper]%=={.title}==%`{.default md=%} which generates:

```render
This is a proposal for a reduced initial set of features to support static
reflection in C++. Specifically we are mostly proposing a subset of features
suggested in [@P1240R2]{.title}.
```

## References

### Automatic References

The bibliography is automatically generated from <https://wg21.link/index.yaml>
for citations of the following types.

| Type              | Identifier                                                                    |
| ----------------- | ----------------------------------------------------------------------------- |
| Paper             | __N__*xxxx* / __P__*xxxx***R***n*                                             |
| Issue             | __CWG__*xxxx* / __EWG__*xxxx* / __LWG__*xxxx* / __LEWG__*xxxx* / __FS__*xxxx* |
| Editorial         | __EDIT__*xxx*                                                                 |
| Standing Document | __SD__*x*                                                                     |

The `[@P1240R2]`{.default} example from [Citations](#citations) produces
a bibliography entry: `[P1240R2]` in [References](#bibliography).

[Run `make update` to re-fetch and update the local databases, including the automatic references.]{.note}

### Manual References

Manual references are specified in a YAML metadata block similar
to [Title], typically at the bottom of the document.

```render
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

This produces a bibliography entry `[Patterns]` in [References](#bibliography).

# Configurations

## Default Language for Code Elements

As mentioned in sections [Inline Code] and [Code Block], inline code elements
are C++ syntax highlighted by default, while code blocks are not.

The default configuration is:

```yaml
---
highlighting: 
  inline-code: cpp
  code-block: default
---
```

You could change this for your document by adding both or either entries to
the YAML metadata block. For example, if you also want code blocks to be C++
by default:

```yaml {.embed_md}
---
title: Framework for Writing C++ Committee Proposals
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
@==highlighting:==@
  @==code-block: cpp==@
---
```

or if you want inline-code to be treated normally, not as C++:

```yaml {.embed_md}
---
title: Framework for Writing C++ Committee Proposals
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
@==highlighting:==@
  @==inline-code: default==@
---
```

## Embedded Markdown by Default Code Classes

[Embedded Markdown] is enabled by default for `cpp` and `default`{.default} code elements.

While the [`.embed_md`](#embed_md) class should be suffcient for most use cases
to enable embedded Markdown as needed, if you want to change the default, you
can set the `embedded-md-code-classes` YAML metadata. For example:

```yaml {.embed_md}
---
title: Framework for Writing C++ Committee Proposals
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
@==embedded-md-code-classes:==@
  @==- cpp==@
  @==- default==@
  @==- diff==@
  @==- nasm==@
  @==- rust==@
---
```

This is an **override** for the existing list of `cpp` and `default`{.default},
so if it's desired to keep `cpp` and `default`{.default} to have embedded Markdown
enabled by default, they must be listed again.

## Unicode Fonts

If building for PDF (via LaTeX) output with Unicode characters, you may want to
select specific [Fonts] for rendering. For example, `monofont` can be specified
in the YAML metadata block to select a font for code elements.

```yaml {.embed_md}
---
title: Framework for Writing C++ Committee Proposals
document: D0000R0
date: today
audience: WG21
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
@==monofont: "DejaVu Sans Mono"==@
---
```

"DejaVu Sans Mono" provides glyphs for a large amount of the Unicode characters.
If you want the list of available fonts on your system, most supported systems
will produce a list via the command-line tool `fc-list`.

[Fonts]: https://pandoc.org/MANUAL.html#fonts

# License

Distributed under the [Boost Software License, Version 1.0](https://github.com/mpark/wg21/blob/master/LICENSE.md).

# Resources

  - Blog Post: [How I format my C++ papers](https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers)
  - Lightning Talk @ C++Now 2019: [WG21 Paper in Markdown](https://www.youtube.com/watch?v=8yReHZOw6QY)

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
