---
title: "Embedded Markdown Tests"
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

# Embedded Markdown

## Default Code Block

```
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

## Custom Delimiters

```{.default .embed_md md="%" em="!"}
%[`!custom!`]{.add}%
```

## Non-Embedded Code

```yaml {em="!"}
@[not embedded]{.add}@ and !emphasized!
```

## Embedded Markdown in C++

```cpp
@@[`namespace @_unspecified_@ { struct sender_base {}; }`]{.add}@@
@@[`using @_unspecified_@::sender_base;`]{.add}@@

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
};
```
