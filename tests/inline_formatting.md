---
title: "Inline Formatting Tests"
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

# Inline Formatting

Inline formatting such as __bold__, _italics_, and `verbatim` work as expected.
There are also useful extensions such as ~~strikeout~~, su~b~script,
su^per^script, highlighted text ==highlighted==, and highlighted code:
`constexpr`{.cpp}.

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

Loose list:

  - `x$~i~$ <=> y$~i~$`{.cpp}

  - [foo `hello world` bar]{.rm}
