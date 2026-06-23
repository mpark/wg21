---
title: "Code Block Tests"
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

# Code Blocks

## No Syntax Highlighting

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
```

## C++ Syntax Highlighting

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
};

void f(@[int \*const \*_p~i~_]{.add}@);
```

## `diff` Syntax Highlighting

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

## `rust` Syntax Highlighting

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
