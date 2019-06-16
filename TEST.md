---
title: "Test document for `mpark/wg21`"
subtitle: "Visual inspection of various features of the framework"
document: D0000R0
date: today
audience:
  - Library Evolution
  - Library
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
toc: true
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

  - `x`~_`i`_~ `<=>` `y`~_`i`_~
  - `compare_3way`{.cpp}
  - `3WAY`{.default}`<R>`{.cpp}
  - `operator@`{.cpp}
  - `operator+`{.cpp}
  - `x @ y`{.cpp}
  <!-- - ~~`x & y`{.cpp}~~ <https://github.com/jgm/skylighting/issues/78> -->
  - __foo `constexpr`{.cpp} bar__
  - _foo `constexpr`{.cpp} bar_
  - ~~foo `constexpr`{.cpp} bar~~
  - [`hello world`]{.add}
  - ~~_`hello world`_~~
  - ~~`hello world`~~

---

Loose list:

  - `x`{.cpp}~_`i`{.cpp}_~ `<=>`{.cpp} `y`{.cpp}~_`i`{.cpp}_~

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
  hello @_`constexpr`_@ detail::foo::template foo;

  [[using CC: opt(1), debug]] x;

  template <typename I>
  [[nodiscard]] auto operator()(I i) -> O<I> { /* ... */ };
};
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
  hello @[`constexpr`]{.add}@ detail::foo::template foo;

  [[using CC: opt(1), debug]] x;

  template <typename I>
  [[nodiscard]] auto operator()(I i) -> O<I> { /* ... */ };

  x@~*i*~@ <=> y@~*i*~@;
  @x~*i*~@ <=> @y~*i*~@;
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
```

### `diff` Syntax Highlighting

```diff
some things just don't change.

// 20.3.4 tuple-like access to pair:
- constexpr typename tuple_element<I, std::pair<T1, T2> >::type&
+ constexpr tuple_element_t<I, pair<T1, T2> >&
-   get(std::pair<T1, T2>&) noexcept;
+   get(pair<T1, T2>&) noexcept;
```

# Tony Tables

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

# Proposed Wording

## Paragraph Numbers

[2]{.pnum} An expression is _potentially evaluated_ unless it is an unevaluated
operand (7.2) or a subexpression thereof. The set of _potential results_ of
an expression `e` is defined as follows:

  - [2.1]{.pnum} If `e` is an _id-expression_ (7.5.4), the set contains only `e`.

  - [2.2]{.pnum} If `e` is a subscripting operation (7.6.1.1) with an array operand,
the set contains the potential results of that operand.

## Wording Changes

Large changes are `::: add` for additions, `::: rm` for removals.

> Modify section 19.20.2 Formatting functions [format.functions]:
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

Small, inline changes are done with `[<new text>]{.add}` or `[<old text>]{.rm}`.

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

# Citation

Automatic references like [@N4762] use <https://wg21.link/index.yaml>.
