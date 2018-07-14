---
title: "Pattern Matching"
document: DxxxxR0
date: 2018-05-22
audience: Evolution
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
---

\hypersetup{linkcolor=black}\tableofcontents

# Introduction

As algebraic data types gain better support in C++ with facilities such as
`tuple` and `variant`, corresponding mechanisms for interacting with them have
become increasingly more important. Pattern matching is one such mechanism that
has been widely adopted by many programming languages. These include text-based
languages such as SNOBOL back in the 1960s, functional languages such as Haskell
and OCaml, as well as "mainstream" languages such as Scala, Swift, and Rust.

Inspired by P0095 [@P0095], which proposed pattern matching and language-level
variant simulteneously, this paper explores a possible full solution for pattern
matching only, and does not address language-level variant design. This is in
correspondence with a straw poll from Kona 2015, which encouraged exploration of
a full solution for pattern matching. SF: 16, WF: 6, N: 5, WA: 1, SA: 0.

# Motivation and Scope

Virtually every program involves branching on some predicates applied to a value
and conditionally binding names to its components for use in subsequent logic.
Today, C++ provides two types of selection statements which choose between one of
several flows of control: the `switch` statement and the `if` statement.
Since `switch` statements can only operate on a _single_ integral value and
`if` statements operate on an _arbitrarily_ complex boolean expression, there is
a significant gap between the two constructs even for inspection of 
the "vocabulary types" provided by the standard library such as `tuple`,
`variant`, `string`, and `vector`.

Consider a variable `p` of type `Point` and a function `position` which
prints whether `p` is positioned at the origin, on the _x_-axis or _y_-axis,
or not on any axes.

+---------------------------------+----------------------------------------+
| __Before__                      | __After__                              |
+---------------------------------+----------------------------------------+
| ```cpp                                                                   |
| struct Point { int x; int y; };                                          |
| ```                                                                      |
+---------------------------------+----------------------------------------+
| ```cpp                          | ```cpp                                 |
| void position(const Point& p) { | void position(const Point& p) {        |
|   if (p.x == 0 && p.y == 0) {   |   inspect (p) {                        |
|     cout << "at the origin";    |     [0, 0]: cout << "at the origin";   |
|   } else if (p.x == 0) {        |     [0, y]: cout << "on the x-axis";   |
|     cout << "on the x-axis";    |     [x, 0]: cout << "on the y-axis";   |
|   } else if (p.y == 0) {        |     [x, y]: cout << "not on any axes"; |
|     cout << "on the y-axis";    |   }                                    |
|   } else {                      | }                                      |
|     cout << "not on any axes";  | ```                                    |
|   }                             |                                        |
| }                               |                                        |
| ```                             |                                        |
+---------------------------------+----------------------------------------+

Structured bindings [@P0144] in C++17 introduced the ability to concisely bind
names to components of a value. Pattern matching aims to naturally extend this
notion by performing __structured inspection__ prior to forming
the __structured bindings__. The proposed direction of this paper is to
introduce an `inspect` statement as the third selection statement to fill
the gap between the `switch` statement and the `if` statement.

# Design Overview

## Basic Structure

```cpp
inspect (init-statement_opt expression) {
  pattern_0 guard_0: statement_0
  pattern_1 guard_1: statement_1
  /* ... */
}
```

## Types of Patterns

### Constant pattern

Constant patterns have the form:

> _constant-expression_

A constant pattern with _constant-expression_ `c` matches a value `v`
if `v == c` is `true`.

```cpp
int factorial(int n) {
  inspect (n) {
    0: return 1;
//  ^ constant pattern
    _: return n * factorial(n - 1);
  }
}
```

### Identifier Pattern

An identifier pattern is denoted by any valid identifier. It matches any value
and binds it to the provided identifier.

```cpp
int i = 101;
inspect (i) {
  x: cout << x; // prints 101
}
```

### Tuple Pattern

Syntax: `[`_pattern_$_0$, _pattern_$_1$, ..., _pattern_$_N$`]`

Matches values that fulfill the structured bindings protocol.

_pattern_$_i$ matches 

### Variant Pattern

```cpp
std::variant<T, U> v;
inspect (v) {
  <T> t: /* ... */
  <U> u: /* ... */
}
```

```cpp
const Base& b = /* ... */;
inspect (v) {
  <Derived1> d1: /* ... */
  <Derived2> d2: /* ... */
}
```

Match the following values:
  - Scalar
  - Product Type (i.e., Structured bindable, (e.g., `std::tuple`)
  - Closed Polymorphism (e.g., `variant`)
  - Range (e.g., `string`)
  - Open Polymorphism (e.g., `std::any`, abstract base class)

## Matching strings

```cpp
std::string s = "hello";
inspect (s) {
  "hello": std::cout << "hello";
  "world": std::cout << "world";
}
```

## Usability of `std::variant`

`variant` is hard to use. // ...

# Impact on the Standard

This is a language extension to introduce an `inspect` statement.

# Proposed Wording

```cpp
inspect (int i = 42) {
  0: std::cout << "foo";
  1: std::cout << "bar";
}
```

https://wandbox.org/permlink/okgMcTpzXqcvN700

# Design Decisions

## Conceptual Model: Extending Structured Bindings

The design intends to be consistent and naturally extend the notions introduced
by structured bindings. That is, we attempt to __refer__ to subobjects rather
than introducing new variables to extract subobjects to.

## Statement vs Expression

This paper diverges from P0095 [@P0095] in that it proposes to add `inspect` as
a statement only rather than trying to double as a statement and an expression.

The main reason here is that the differences between the statement and
expression forms are __not__ trivial.
  1. In the case where none of the cases match, the statement form simply skips
     over the entire statement à la `switch`, whereas the expression form throws
     an expression since it is required to yield a value.
  2. The resulting type of a statement-form of `inspect` within an immediately-
     invoked-lambda is required to be explicitly specified, or is determined by
     the first `return` statement. In contrast, the expression form will
     probably need to use `std::common_type_t<Ts...>` where `Ts...` are types of
     `N` expressions à la the ternary operator.

While an expression-form would be useful, the author believes that it can/should
be introduced later, with different syntax such as `x inspect { /* ... */ }`.
The proposed syntax in this paper is consistent with other statements today.

## Language vs Library

# Implementation Experience

# Other Languages

## C\#



## Rust

Constants: https://github.com/rust-lang/rfcs/blob/master/text/1445-restrict-constants-in-patterns.md

### Intersection of semantic / structural equality

## Scala

Scala Tutorial - Pattern Matching: https://www.youtube.com/watch?v=ULcpWn23waw
Matching Objects with Patterns: https://infoscience.epfl.ch/record/98468/files/MatchingObjectsWithPatterns-TR.pdf

### Extractors

## F\#

### Active Patterns

# Future Work

# Acknowledgements

Thank you to Agustín Bergé, Ori Bernstein, Alexander Chow, Louis Dionne,
Michał Dominiak, Eric Fiselier, Zach Laine, Jason Lucas, David Sankel,
Tony Van Eerd, and everyone else who contributed to the discussions, and
encouraged me to write this paper.

---
references:
  - id: N3449
    title: "Open and Efficient Type Switch for C++"
    issued:
      year: 2012
      month: 9
    author:
      family: Stroustrup
      given: Bjarne
    container-title: N3449
    URL: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3449.pdf
  - id: N3627
    title: "Relaxed switch statement"
    issued:
      year: 2013
      month: 2
    author:
      family: Yuan
      given: Zhihao
    container-title: N3627
    URL: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3627.html
  - id: P0095
    title: "Pattern Matching and Language Variants"
    issued:
      year: 2016
      month: 5
    author:
      family: Sankel
      given: David
    container-title: P0095
    URL: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0095r1.html
  - id: P0144
    title: "Structured bindings"
    issued:
      year: 2016
      month: 3
    author:
      - family: Sutter
        given: Herb 
      - family: Stroustrup
        given: Bjarne
      - family: Dos Reis
        given: Gabriel
    container-title: P0144
    URL: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0144r2.pdf
---

<!--
Consistent Comparisons: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0515r3.pdf
Class Types in Non-Type Template Parameters: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0732r0.pdf
From F# to Scala Extractors: https://theburningmonk.com/2017/01/from-f-to-scala-extractors/


```
inspect (int i = 42) {
  0: std::cout << "foo";
  1: std::cout << "bar";
}
```

```
[&] -> std::string {
  inspect (i) {
    0: return "foo";
    1: return "bar";
  }
}()
```

```
inspect (std::lock_guard lock(mutex); i) {
  0 => std::cout << "foo";
  1 => std::cout << "bar";
}
```

```
inspect (pair<int, int> p = ...; p) {
  [x, 0]: { std::cout << "foo"; x; y; }
  [0, y]: std::cout << "bar";
  _: /* ... */;
}
```

```
inspect (std::variant<int, double> v = ...; v) {
  [0]: std::cout << "foo";
  // <pair<int, int>> [x, y]: std::cout << "bar";
}
```

```
inspect (std::variant<int, pair<int, int>> v = ...; v) {
  <int> x: std::cout << "foo";
  <pair<int, int>> [x, y]: std::cout << "bar";
}
```

```
inspect (std::variant<int, int> v = ...; v) {
  <0> x: std::cout << "foo";
  <1> x: std::cout << "bar";
}
```

```
inspect (const Base& b = ...) {
  <D1> [x] => std::cout << "foo";
  <D2> [x, y] => std::cout << "bar";
}
```

inspect (f()) {
  pair [int x, int y]

```
inspect (std::variant<int, pair<int, int>> v = ..., w = ...; std::make_tuple(v, w)) {
  [<0> x, <int> y]: std::cout << "foo";
  [<int> x, <pair<int, int>> [y, 0]]: std::cout << "bar";
  [<pair<int, int>> p, <int> y]: std::cout << "bar";
  [<pair<int, int>> [x, y], <pair<int, int>> p]: std::cout << "bar";
}
```

```
inspect (s) {
  "hello": ...;
  "foobar": ...;
  "(foo)*bar"reg: ...;
  std::string_view sv:
}
```

```
inspect (s) {
  email [local, domain]: ...;
  us_phone_number [area_code, _, _]: ...;
}
```

```
  selection-statement:
  	if constexpr_opt (init-statement_opt condition) statement
    if constexpr_opt (init-statement_opt condition) statement else statement
  	switch (init-statement_opt condition) statement
+   inspect (init-statement_opt condition) { inspect-case-seq_opt }
  
+ inspect-case-seq
+   inspect-case
+   inspect-case-seq inspect-case
  
+ inspect-case
+   inspect-pattern guard_opt => statement

+ guard
+   if (condition)

+ inspect-pattern
+   identifier
+   constant-expression
+   wildcard-pattern
+   tuple-pattern
+   variant-pattern
```

- Based on structured binding protocol
  - `get<>`, `std::tuple_element`, `std::tuple_size`
  - `operator extract()`(?)
- Patterns are composed of compile-time values.
  - Optimization(?)
  - But if we keep the existing protocol, is this even possible?
  - We have to execute `operator==` which may not be `constexpr`.
  - Invocations of `get` cannot be counted, same as copy constructor
    calls cannot be counted due to optimizations.
- Syntax for matching `std::variant` and base class.
  - Given `inspect (v) { int n: stmt1; double d : stmt2;}`,
    `int n` and `double d` looks like declarations, but they are not.
- In order, determine if it's a match (e.g., dynamic type checking), then 
  transform (e.g., dynamic_cast), coupling the "is-as" pattern.
  So, given a string, why not match if it's the form of email, then transform,
  into 2 parts then continue matching?

  if (is_email(s)) {  // is
    auto [local, domain] = s;  // as
  }

```
  auto [__x, __y] = t;
  switch (__x) {
    case 0: {
      auto&& y = __y;
      // A
      break;
    }
    default: {
      switch (__y) {
        case 0: {
          auto&& x = __x;
          // B
          break;
        }
        default: {
          // C
        }
      }
    }
  }

  if (__x == 0) {
    auto&& y = __y;
    // A
  } else if (__y == 0) {
    auto&& x = __x;
    // B
  } else {
    // C
  }

  inspect (t) {
    [0, y]: /* A */
    [x, 0]: /* B */
    [_, _]: /* C */
  }
```

```
  if (holds_alternative<int>(v)) {  // is
    int x = get<int>(v);  // as
  }

  Base& b = ...;
  if (auto* d_ptr = dynamic_cast<const Derived*>(&b)) {  // almost is-as
    const Derived& d = *d_ptr;  // as
  }

  variant<int, string> v = ...;
  if (int* i = get_if<int>(&v)) {  // almost is-as
    int x = *i;  // as
  }
```

```
template <typename T>
auto variant_index(T* p) { return p != nullptr; }

template <typename T>
auto variant_index(optional<T> const& o) { return o.has_value(); }

template <typename... Ts>
auto variant_index(std::variant<Ts...> const& v) { return v.index(); };

template <typename T>
struct variant_access<optional<T>, none> { static constexpr int index = 0; };

template <typename T>
struct variant_access<optional<T>, some> {
  static constexpr int index = 1;

  auto&& get(optional<T> const& o) { return *o; }
};

template <typename... Ts, typename Alt>
struct variant_access<variant<Ts...>, Alt>
  static constexpr int index = index_of<Alt, list<Ts...>>;
  
  auto&& get(variant<Ts...> const& v) { return get<Alt>(v); }
};
  
template <typename... Ts, size_t I>
struct variant_access<variant<Ts...>, I>
  static constexpr int index = I;

  auto&& get(variant<Ts...> const& v) { return get<I>(v); }
};

inspect (v) {
  <int> x: ...
  <string>: ...
}

inspect (tuple{o, o}) {
  [<some> x, <some> y]: ...
  none: ...
}
```
-->
