---
title: "Test document for mpark/wg21"
subtitle: "Visual inspection of various features of the framework"
document: D0000R1
date: today
audience:
  - Library Evolution
  - Library
revises: D0000R0
author:
  - name: Author 0
    email: <author0@gmail.com>
  - name: Author 1
    email: <author1@gmail.com>
toc: true
toc-depth: 2
---

# Introduction

This framework provides support for various common elements for C++ papers.
This document is intended to test various features implemented in [`mpark/wg21`].

[`mpark/wg21`]: https://github.com/mpark/wg21

# Title

The title is specified by YAML metadata block.

```yaml
---
title: Example Title
subtitle: Example Subtitle
document: DxxxxRn
date: 2019-06-13
audience:
  - Library Evolution
  - Library
author:
  - name: Author One
    email: <one@author.com>
  - name: Author Two
    email: <two@author.com>
toc: false    # default: `true`
toc-depth: 4  # default: `3`
---
```

> `date: today` will generate today's date in `YYYY-MM-DD` (ISO 8601) format.

# Markdown

[Pandoc Markdown] is the Markdown flavor used for this framework.

## Inline Formatting

Inline formatting such as __bold__, _italics_, and `verbatim` work as you would
expect. There are also useful extensions such as ~~strikeout~~,
su~b~script, su^per^script, and highlighted code: `constexpr`{.cpp}.

Various compositions in compact list:

  - ~~`A<B<T>>`{.cpp}~~
  - `compare_3way`{.cpp}
  - [`compare_3way`]{.add}
  - `3WAY`{.default}`<R>`{.cpp}
  - `operator@`{.default}
  - `operator+`{.cpp}
  - `x @ y`{.default}
  - ~~`x & y`{.cpp}~~
  - __foo `constexpr`{.cpp} bar__
  - _foo `constexpr`{.cpp} bar_
  - ~~foo `constexpr`{.cpp} bar~~
  - [`hello world`]{.add}
  - `@[hello<T>]{.add}@`
  - ~~_`hello world`_~~
  - ~~`hello world`~~
  - `namespace $unspecified$ { struct sender_base {}; }`
  - `namespace $unspecified$ { struct sender_base {}; }`{.cpp}
  - `constexpr$~opt~$`{.cpp}
  - ==highlighted==
  - `void @==foo==@();`{.cpp}
  - ==`void foo();`{.cpp}==
  - $\frac{a+b}{2}$
  - `string format(...);  // @[format.functions]{.sref}@`

---

Loose list:

  - `x$~i~$ <=> y$~i~$`{.cpp}

  - [foo `hello world` bar]{.rm}

[Pandoc Markdown]: https://pandoc.org/MANUAL.html#pandocs-markdown

## Inline Code in Headers: `int`{.cpp}, `x & y`{.cpp}

## Code Block

### No Syntax Highlighting

```
#include <iostream>
#include "foo.h"

__FILE__;

int x = 42'234'234;
const int x = 42ul;
const int x = 0B01011;

bool b = true;

struct process {
  hello @[constexpr\ ]{.rm}@detail::foo::template $foo$;

  [[using CC: opt(1), debug]] x;

  template <typename I>
  [[nodiscard]] auto operator()(I i) -> O<I> { /* ... */ };
};

@[namespace _unspecified_ { struct sender_base {}; }]{.add}@
@[`namespace $unspecified$ { struct sender_base {}; }`]{.add}@
@@[`namespace @_unspecified_@ { struct sender_base {}; }`]{.add}@@

@$\frac{a+b}{2}$@  // math
@[`$bar$`]{.add}@  // italicized code
@[``$baz$``]{.add}@  // italicized code
@[`$bar$`{.raw}]{.add}@  // raw $bar$
@==$==@text@==$==@  highlighted $

@[using _unspecified_::sender_base;]{.add}@
@[`using $unspecified$::sender_base;`]{.add}@
@@[`using @_unspecified_@::sender_base;`]{.add}@@

@[template<class, class> struct _as-receiver_; _// exposition only_]{.add}@
@[`template<class, class> struct $as-receiver$; $// exposition only$`]{.add}@
@@[`template<class, class> struct @_as-receiver_@; @_// exposition only_@`]{.add}@@

@[template<class, class> struct _as-invocable_; _// exposition only_]{.add}@
@[`template<class, class> struct $as-invocable$; $// exposition only$`]{.add}@
@@[`template<class, class> struct @_as-invocable_@; @_// exposition only_@`]{.add}@@
```

### C++ Syntax Highlighting

```cpp
#include <iostream>
#include "foo.h"

__FILE__;

int x = 42'234'234;
const int x = 42ul;
const int x = 0B01011;

bool b = true;

struct process {
  hello @[constexpr\ ]{.add}@detail::foo::template foo;

  [[using CC: opt(1), debug]] x;

  template <typename I>
  [[nodiscard]] auto operator()(I i) -> O<I> { /* ... */ };

  x$~i~$ <=> y$~i~$;
};

if (x) {
  return ""sv;
  return 5ms;
}

std::printf("%d", x);

std::variant<I1, I2> input = 'h';
std::variant<I1, I2> input = "h";
std::variant<I1, I2> input = "hello";

// mapping from a `variant` of inputs to a `variant` of results:
auto output = std::visit<std::variant<O<I1>, O<I2>>>(process{}, input);

// coercing different results to a common type:
auto result = std::visit<std::common_type_t<O<I1>, O<I2>>>(process{}, input);

// visiting a `variant` for the side-effects, discarding results:
std::visit<void>(process{}, input);

@@[`namespace @_unspecified_@ { struct sender_base {}; }`]{.add}@@
@@[`using @_unspecified_@::sender_base;`]{.add}@@

template <@[invocable](class){.sub}@ F@[, class]{.add}@>
struct $as-receiver$ {
@[private:]{.rm}@
  @[using invocable_type = std::remove_cvref_t<F>;]{.rm}@
  @[invocable_type](F){.sub}@ f_;
@[public:]{.rm}@
  @[explicit _as-receiver_(invocable_type&& f)]{.rm}@
  @[_as-receiver_(_as-receiver_&& other) = default;]{.rm}@
  void set_value() @[noexcept(is_nothrow_invocable_v<F&>)]{.add}@ {
    invoke(f_);
  }
  @[[[noreturn]]]{.add}@ void set_error(std::exception_ptr) @[noexcept]{.add}@ {
    terminate();
  }
  void set_done() noexcept {}
};

template <@[`invocable`](`class`){.sub}@ F@[`, class`]{.add}@>
struct $as-receiver$ {
@[`private:`]{.rm}@
  @[`using invocable_type = std::remove_cvref_t<F>;`]{.rm}@
  @[`invocable_type`](`F`){.sub}@ f_;
@[`public:`]{.rm}@
  @@[`explicit @_as-receiver_@(invocable_type&& f)`]{.rm}@@
  @@[`@_as-receiver_@(@_as-receiver_@&& other) = default;`]{.rm}@@
  void set_value() @[`noexcept(is_nothrow_invocable_v<F&>)`]{.add}@ {
    invoke(f_);
  }
  @[`[[noreturn]]`]{.add}@ void set_error(std::exception_ptr) @[`noexcept`]{.add}@ {
    terminate();
  }
  void set_done() noexcept {}
};

void f(@[int \*const \*_p~i~_]{.add}@);
```

### `diff` Syntax Highlighting

```diff
some things just don't change.

// 20.3.4 tuple-like access to pair:
- constexpr typename tuple_element<I, std::pair<T1, T2> >::type&
+ constexpr tuple_element_t<I, pair<T1, T2> >&
-   get(std::pair<T1, T2>&) noexcept;
+   get(pair<T1, T2>&) noexcept;

$unspecified$ detail::foo::template foo;
+ $unspecified$ detail::foo::template foo;
- $unspecified$ detail::foo::template foo;
```

### `rust` Syntax Highlighting

```rust
enum Result<T, E> {
  Ok(T),
  Err(E),
}

match parse(some_input) {
  Ok(v) => // use `v`
  Err(err) => // use `err`
}
```

## Automatic Header Links {#auto-header-links}

Automatic header links are written as `[](#auto-header-links)`{.markdown},
and renders as [](#auto-header-links).

# Comparison Tables

::: cmptable

> Put your caption here with some `code`

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

::: cmptable

### Before {width=.6}
```cpp
switch (x) {
  case 0: std::cout << "got zero"; break;
  case 1: std::cout << "got one"; break;
  default: std::cout << "don't care";
}
```

### After {width=.4}
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

# Proposed Wording

## Manual Paragraph Numbers

[2]{.pnum} An expression is _potentially evaluated_ unless it is an unevaluated
operand (7.2) or a subexpression thereof. The set of _potential results_ of
an expression `e` is defined as follows:

  - [2.1]{.pnum} If `e` is an `$id-expression$` (7.5.4), the set contains only `e`.
  - [2.2]{.pnum} If `e` is a subscripting operation (7.6.1.1) with an array operand,
    the set contains the potential results of that operand.

## Automatic Paragraph Numbers

::: wording
#. `#.`{.default} automatically starts at `1`.
#. Another `#.`{.default} automatically continues to `2`.
   - Nested bullet list also get automatic numbering. `(2.1)`.

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

[...]

17. Pin with `17.`{.default}.

::: add
x) `x)`{.default} is mainly to skip numbering in `add`.
   - Nested bullet within an `x)`. This will be (x.1).
   x) Nested `x)` within an `x)`. This will be (x.x).
x) Second added paragraph.
:::

::: rm
#. `#.`{.default} here will be 18 after the skips.

[...]

24. Skip and pin again, e.g. `24.`{.default}.
:::

#. Automatically continue to 25.
:::

---

::: wording

### General [intro.compliance.general]{.sref} {-}

1. The set of _diagnosable rules_ consists of all syntactic and semantic rules
   in this document except for those rules containing an explicit notation that
   "no diagnostic is required" or which are described as resulting in "undefined behavior".

#. Although this document states only requirements on C++ implementations, those
   requirements are often easier to understand if they are phrased as requirements
   on programs, parts of programs, or execution of programs. Such requirements have
   the following meaning:

   - If a program contains no violations of the rules in [lex]{- .sref} through
     [exec]{- .sref} as well as those specified in [depr]{- .sref}, a conforming
     implementation shall accept and correctly execute that program, except when
     the implementation's limitations (see below) are exceeded.
   - If a program contains a violation of a rule for which no diagnostic is required,
     this document places no requirement on implementations with respect to that program.
   - Otherwise, if a program contains
     - a violation of any diagnosable rule,
     - a preprocessing translation unit with a `#warning` preprocessing directive
       ([cpp.error]{- .sref}),
     - an occurrence of a construct described in this document as “conditionally-supported”
       when the implementation does not support that construct, or
     - a contract assertion ([basic.contract.eval]{- .sref}) evaluated with
       a checking semantic in a manifestly constant-evaluated context
       ([expr.const.defns]{- .sref}) resulting in a contract violation,

     a conforming implementation shall issue at least one diagnostic message.

   [During template argument deduction and substitution, certain constructs that
   in other contexts require a diagnostic are treated differently;
   see [temp.deduct]{- .sref}.]{.note}

   Furthermore, a conforming implementation shall not accept
     - a preprocessing translation unit containing a `#error` preprocessing
       directive ([cpp.error]{- .sref}),
     - a translation unit with a `$static_assert-declaration$` that
       fails ([dcl.pre]{- .sref}), or
     - a contract assertion evaluated with a terminating semantic
       ([basic.contract.eval]{- .sref}) in a manifestly constant-evaluated context
       ([expr.const.defns]{- .sref}) resulting in a contract violation.

#. For classes and class templates, the library Clauses specify partial definitions.
   Private members are not specified, but each implementation shall supply them to complete
   the definitions according to the description in the library Clauses.

### Diagnostic directives [cpp.error]{.sref} {-}

1. A preprocessing directive of the form

   > ```cpp
   > # error $pp-tokens~opt~$ $new-line$
   > ```

   renders the program ill-formed. A preprocessing directive of the form

   > ```cpp
   > # warning $pp-tokens~opt~$ $new-line$
   > ```

   requires the implementation to produce at least one diagnostic message for
   the preprocessing translation unit ([intro.compliance.general]{- .sref}).

#. _Recommended practice_: Any diagnostic message caused by either of these directives should include the specified sequence of preprocessing tokens.
:::

## Wording Changes

Large changes are `::: add` for additions, `::: rm` for removals.

> Modify section [format.functions]{.sref}:
>
> ::: add
>
> ```
> template<class... Args>
>   string format(const locale& loc, string_view fmt, const Args&... args);
> ```
>
> _Returns:_ `vformat(loc, fmt, make_format_args(args...))`.
>
> :::

Small, inline changes are done with `[new text]{.add}`{.default} or
`[old text]{.rm}`{.default}.

Substitutions can be written as `[old text](new text){.sub}`{.default}.
This is essentially just a short-form for `[old text]{.rm}[new text]{.add}`{.default}.

The optional _attribute-specifier-seq_ appertains to the [label](_general-label_){.sub}.
The only use of a [label with an _identifier_](_label_){.sub} is as the target of a `goto`,
[`break`, or `continue`]{.add}. No two [label](_label_){.sub}s in a function shall have
the same _identifier_. A [label](_general-label_){.sub} can be used [in a `goto` statement]{.rm}
before its introduction by a _labeled-statement_.

+-----------+--------------------------------------------------------------------+
| Specifier | Replacement                                                        |
+===========+====================================================================+
| `%a`      | The locale’s abbreviated weekday name. If the value does not       |
|           | contain a valid weekday, [`setstate(ios::failbit)` is called]{.rm} |
|           | [`format_error` is thrown]{.add}.                                  |
+-----------+--------------------------------------------------------------------+
| `%A`      | The locale’s full weekday name. If the value does not contain      |
|           | a valid weekday, [`setstate(ios::failbit)` is called]{.rm}         |
|           | [`format_error` is thrown]{.add}.                                  |
+-----------+--------------------------------------------------------------------+

## Grammar Changes

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

# Stable Names

Stable names are written as `[basic.life]{.sref}`, and renders as [basic.life]{.sref}.

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

# Notes

There are three supported styles of note:

- Use the `note` class for notes that are expected to appear in the specification wording
  ```
  [Notes will look like this]{.note}
  ```
  [Notes will look like this]{.note}

- Use the `ednote` for editorial notes, these will be formatted as
  ```
  [Editorial notes are important]{.ednote}
  ```
  [Editorial notes are important]{.ednote}

- Use `draftnote` to include text that is intended as questions or information for reviews and
  working groups.
  ```
  [Drafting notes can be used to provide comments for reviewers that are explicitly not to be
   included in the specification.]{.draftnote}

   [It is also possible to indicate the a note is for
   a specific `audience` via this optional attribute.]{.draftnote audience="the reader"}
  ```
  [Drafting notes can be used to provide comments for reviewers that are explicitly not to be
   included in the specification.]{.draftnote}

  [It is also possible to indicate the a note is for
   a specific `audience` via this optional attribute.]{.draftnote audience="the reader"}

# Citation

Automatic references are written as `[@N4762]`{.default} and renders as [@N4762].
Anything in <https://wg21.link/index.yaml> are linked automatically.

  - `N` Papers (e.g., `[@N3887]`{.default} → [@N3887])
  - `P` Papers (e.g., `[@P1371R1]`{.default} → [@P1371R1])
  - CWG Issues (e.g., `[@CWG1234]`{.default} → [@CWG1234])
  - LWG Issues (e.g., `[@LWG1234]`{.default} → [@LWG1234])
  - Github Edits (e.g, `[@EDIT1234]`{.default} → [@EDIT1234])
  - Standing Documents (e.g., `[@SD6]`{.default} → [@SD6])

You may also write `[@P2996R8]{.title}`{.default} to include the title of the paper,
and renders as: [@P2996R8]{.title}.
