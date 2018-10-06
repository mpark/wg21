---
title: "Pattern Matching"
document: D1260R0
date: 2018-05-22
audience: Evolution
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
---

# Introduction

As algebraic data types gain better support in C++ with facilities such as
`tuple` and `variant`, the importance of mechanisms to interact with them have
increased. While mechanisms such as `apply` and `visit` have been added, their
usage is quite complex and limited even for simple cases. Pattern matching is
a widely adopted mechanism across many programming languages to interact with
algebraic data types that can help greatly simplify C++. Examples of programming
languages include text-based languages such as SNOBOL back in the 1960s,
functional languages such as Haskell and OCaml, and "mainstream" languages such
as Scala, Swift, and Rust.

Inspired by P0095 [@P0095] --- which proposed pattern matching and
language-level variant simulteneously --- this paper explores a possible
direction for pattern matching only, and does not address language-level
variant design. This is in correspondence with a straw poll from Kona 2015,
which encouraged exploration of a full solution for pattern matching.
SF: 16, WF: 6, N: 5, WA: 1, SA: 0.

# Motivation and Scope

Virtually every program involves branching on some predicates applied to a value
and conditionally binding names to some of its components for use in subsequent
logic. Today, C++ provides two types of selection statements: the `if` statement
and the `switch` statement.

Since `switch` statements can only operate on a _single_ integral value and
`if` statements operate on an _arbitrarily_ complex boolean expression, there is
a significant gap between the two constructs even in inspection of
the "vocabulary types" provided by the standard library.

In C++17, structured binding declarations [@P0144] introduced the ability to
concisely bind names to components of a `tuple`-like value. The proposed
direction of this paper aims to naturally extend this notion by performing
__structured inspection__ prior to forming the __structured bindings__ with
a third selection statement: the `inspect` statement. The goal of the `inspect`
statement is to bridge the gap between `switch` and `if` statements with
a __declarative__, __structured__, __cohesive__, and __composable__ mechanism.

# Before/After Comparisons

## Matching Integrals

+------------------------------------------------+-------------------------------------------------+
| __Before__                                     | __After__                                       |
+================================================+=================================================+
| ```cpp                                         | ```cpp                                          |
| switch (x) {                                   | inspect (x) {                                   |
|   case 0: std::cout << "got zero";             |   0: std::cout << "got zero";                   |
|   case 1: std::cout << "got one";              |   1: std::cout << "got one";                    |
|   default: std::cout << "don't care";          |   _: std::cout << "don't care";                 |
| }                                              | }                                               |
| ```                                            | ```                                             |
+------------------------------------------------+-------------------------------------------------+

## Matching Strings

+--------------------------------------+---------------------------------------+
| __Before__                           | __After__                             |
+======================================+=======================================+
| ```cpp                               | ```cpp                                |
| if (s == "foo") {                    | inspect (s) {                         |
|   std::cout << "got foo";            |   "foo": std::cout << "got foo";      |
| } else if (s == "bar") {             |   "bar": std::cout << "got bar";      |
|   std::cout << "got bar";            |   _: std::cout << "don't care";       |
| } else {                             | }                                     |
|   std::cout << "don't care";         | ```                                   |
| }                                    |                                       |
| ```                                  |                                       |
+--------------------------------------+---------------------------------------+

## Matching Tuples

+--------------------------------------+---------------------------------------+
| __Before__                           | __After__                             |
+======================================+=======================================+
| ```cpp                               | ```cpp                                |
| auto&& [x, y] = p;                   | inspect (p) {                         |
| if (x == 0 && y == 0) {              |   [0, 0]: std::cout << "on origin";   |
|   std::cout << "on origin";          |   [0, y]: std::cout << "on y-axis";   |
| } else if (x == 0) {                 |   [x, 0]: std::cout << "on x-axis";   |
|   std::cout << "on y-axis";          |   [x, y]: std::cout << x << ',' << y; |
| } else if (y == 0) {                 | }                                     |
|   std::cout << "on x-axis";          | ```                                   |
| } else {                             |                                       |
|   std::cout << x << ',' << y;        |                                       |
| }                                    |                                       |
| ```                                  |                                       |
+--------------------------------------+---------------------------------------+

## Matching Variants

+------------------------------------------------+-------------------------------------------------+
| __Before__                                     | __After__                                       |
+================================================+=================================================+
| ```cpp                                         | ```cpp                                          |
| struct visitor {                               | inspect (v) {                                   |
|   void operator()(int i) const {               |   <int> i: strm << "got int: " << i;            |
|     os << "got int: " << i;                    |   <float> f: strm << "got float: " << f;        |
|   }                                            | }                                               |
|   void operator()(float f) const {             | ```                                             |
|     os << "got float: " << f;                  |                                                 |
|   }                                            |                                                 |
|   std::ostream& os;                            |                                                 |
| };                                             |                                                 |
| std::visit(visitor{strm}, v);                  |                                                 |
| ```                                            |                                                 |
+------------------------------------------------+-------------------------------------------------+

## Evaluating Expressions

Given the following definition:

```cpp
struct Expr;

struct Neg { std::shared_ptr<Expr> expr; };
struct Add { std::shared_ptr<Expr> lhs, rhs; };
struct Mul { std::shared_ptr<Expr> lhs, rhs; };

struct Expr : std::variant<int, Neg, Add, Mul> { using variant::variant; };
```

+--------------------------------------------+-------------------------------------------------+
| __Before__                                 | __After__                                       |
+============================================+=================================================+
| ```cpp                                     | ```cpp                                          |
| int eval(const Expr& expr) {               | int eval(const Expr& expr) {                    |
|   struct visitor {                         |   inspect (expr) {                              |
|     int operator()(int i) const {          |     <int> i: return i;                          |
|       return i;                            |     <Neg> [e]: return -eval(*e);                |
|     }                                      |     <Add> [l, r]: return eval(*l) + eval(*r);   |
|     int operator()(const Neg& n) const {   |     <Mul> [l, r]: return eval(*l) * eval(*r);   |
|       return -eval(*n.expr);               |   }                                             |
|     int operator()(const Add& a) const {   | }                                               |
|       return eval(*a.lhs) + eval(*a.rhs);  | ```                                             |
|     }                                      |                                                 |
|     int operator()(const Mul& m) const {   |                                                 |
|       return eval(*m.lhs) * eval(*m.rhs);  |                                                 |
|     }                                      |                                                 |
|   };                                       |                                                 |
|   return std::visit(visitor{}, expr);      |                                                 |
| }                                          |                                                 |
| ```                                        |                                                 |
+--------------------------------------------+-------------------------------------------------+

# Design Overview

## Basic Syntax

> | `inspect (` _init-statement~opt~_ _condition_ `) {`
> |     _pattern_ _guard~opt~_ `:` _statement_
> |     _pattern_ _guard~opt~_ `:` _statement_
> |     ...
> | `}`

> | _guard:_
> |     `if (` _expression_ `)`

## Basic Model

Within the parentheses, the `inspect` statement is equivalent to `switch` and
`if` statements except that no conversion nor promotion takes place in
evaluating the value of its condition.

When the `inspect` statement is executed, its condition is evaluated and matched
in order (first match semantics) against each pattern. If a pattern successfully
matches the value of the condition and the boolean expression in the guard
evalutes to `true` (or if there is no guard at all), control is passed to the
statement following the matched pattern label. If the guard expression evaluates
to `false`, control flows to the subsequent pattern. If no pattern matches, none
of the statements are executed.

## Types of Patterns

### Primary Patterns

#### Identifier Pattern

The identifier pattern has the form:

> _identifier_

and matches any value `v`. The introduced name behaves as an lvalue
referring to `v`, and is in scope from its point of declaration until
the end of the statement following the pattern label.

```cpp
int v = /* ... */;

inspect (v) {
    x: std::cout << x;
//  ^ identifier pattern
}
```

[ _Note:_ If the identifier pattern is used as a top-level pattern,
          it has the same syntax as a `goto` label. ]

#### Constant Pattern

The constant pattern has the form:

> _constant-expression_

and matches value `v` if `std::strong_equal(c, v) == std::strong_equality::equal`
is `true` where `c` is the constant expression.

```cpp
int v = /* ... */;

inspect (v) {
    0: std::cout << "got zero";
    1: std::cout << "got one";
//  ^ constant pattern
}
```

[ _Note:_ The _id-expression_ is overriden by the identifier pattern.
          `+id` or `(id)` is needed for disambiguation. ]

```cpp
static constexpr int zero = 0, one = 1;
int v = /* ... */;

inspect (v) {
    +zero: std::cout << "got zero";
    (one): std::cout << "got one";
//  ^^^^^ constant pattern
}
```

### Compound Patterns

#### Structured Binding Pattern

The structured binding pattern has `N` _pattern_ instances with the form:

> `[` _pattern_~0~`,` _pattern_~1~`,` ...`,` _pattern_~N-1~ `]`

and matches value `v` if each _pattern~i~_ matches the _i_^th^ component of `v`.
The components of `v` are determined by the structured binding declaration:
`auto&& [__e`~0~`, __e`~1~`,` ...`, __e`~N-1~`] = v;` where each `__e`_~i~_
are unique exposition-only identifiers.

```cpp
std::pair<int, int> p = /* ... */;

inspect (p) {
    [0, 0]: std::cout << "on origin";
    [0, y]: std::cout << "on y-axis";
//      ^ identifier pattern
    [x, 0]: std::cout << "on x-axis";
//      ^ constant pattern
    [x, y]: std::cout << x << ',' << y;
//  ^^^^^^ structured binding pattern
}
```

#### Alternative Pattern

The alternative pattern has the form:

> `<Alt>` _pattern_

Let `v` be the value being matched and `V` be its type. There are two cases we consider:

1. __Variant-Like__

   If `std::variant_size_v<V>` is well-formed and evaluates to an integral,
   the alternative pattern matches `v` if `Alt` is compatible with the current
   index of `v` and _pattern_ matches the active alternative of `v`.

   Let `I` be the current index of `v` given by a member `v.index()` or else
   a non-member ADL-only `index(v)`. The current alternative of `v` behaves as
   a reference of type `std::variant_alternative_t<I, V>` initialized by
   a member `v.get<I>()` or else a non-member ADL-only `get<I>(v)`.

   `Alt` is compatible with `I` if one of the following four cases is true:

     a. If `Alt` is __`auto`__
     a. If `Alt` is a __concept__ and `Alt<std::variant_alternative_t<I, V>>()`
     a. If `Alt` is a __type__ and `std::is_same_v<Alt, std::variant_alternative_t<I, V>>`
     a. If `Alt` is a __value__ and is the same value as `I`.

   ```cpp
   std::variant<int, float> v = /* ... */;

   inspect (v) {
       <int> i: std::cout << "got int: " << i;
       <float> f: std::cout << "got float: " << f;
   }
   ```
   ```cpp
   std::variant<int, int> v = /* ... */;

   inspect (v) {
       <0> x: std::cout << "got first int: " << x;
       <1> x: std::cout << "got second int: " << x;
   }
   ```

2. __Polymorphic__

// TODO

# Impact on the Standard

This is a language extension to introduce a new selection statement: `inspect`.

# Proposed Wording

## Syntax

Add to __\S8.4 [stmt.select]__ of ...

\pnum{1}Selection statements choose one of several flows of control.

> | _selection-statement:_
> |     `if constexpr`_~opt~_ `(` _init-statement~opt~_ _condition_ `)` _statement_
> |     `if constexpr`_~opt~_ `(` _init-statement~opt~_ _condition_ `)` _statement_ `else` _statement_
> |     `switch (` _init-statement~opt~_ _condition_ `)` _statement_
> |     \added `inspect (` _init-statement~opt~_ _condition_ `) {` _inspect-case-seq_ `}` \unchanged
>
> \added
> | _inspect-case-seq:_
> |     _inspect-case_
> |     _inspect-case-seq_ _inspect-case_
>
> | _inspect-case:_
> |     _attribute-specifier-seq~opt~_ _inspect-pattern_ _inspect-guard~opt~_ `:` _statement_
>
> | _inspect-pattern:_
> |     _constant-pattern_
> |     _identifier_
> |     _wildcard-pattern_
> |     _structured-binding-pattern_
> |     _alternative-pattern_
>
> | _inspect-guard:_
> |     `if (` _condition_ `)`
> \unchanged

# Design Decisions

## Conceptual Model: Extending Structured Bindings

The design intends to be consistent and naturally extend the notions introduced
by structured bindings. That is, The subobjects are __referred__ to rather than
being assigned into new variables.

## `inspect` vs `switch`

This proposal introduces a new `inspect` statement rather than trying to extend
the `switch` statement for the following reasons:

  - `switch` allows the `case` labels to appear anywhere, which hinders pattern
    matching's aim for __structured__ inspection.
  - The fall-through semantics of `switch` generally results in `break` being
    attached to every case.
  - `switch` is purposely restricted to integrals for __guaranteed__ efficiency.
    The primary goal of pattern matching in this paper is expressivity, while
    being at least as efficient as the naively hand-written code.

## First Match vs Best Match

// TODO

## Statement vs Expression

This paper diverges from P0095 [@P0095] in that it proposes to add `inspect` as
a statement only rather than trying to double as a statement and an expression.

The main reason here is that the semantic differences between the statement and
expression forms are not trivial.
  1. In the case where none of the cases match, the statement form simply skips
     over the entire statement à la `switch`, whereas the expression form throws
     an exception since it is required to yield a value.
  2. Resulting type of the statement form of `inspect` within an immediately-
     invoked-lambda is required to be explicitly specified, or is determined by
     the first `return` statement. In contrast, the expression form will
     probably need to use `std::common_type_t<Ts...>` where `Ts...` are types of
     `N` expressions to be consistent with the ternary operator.

While an expression form of `inspect` would be useful, the author believes that
it can and should be introduced later, with different syntax such as
`x inspect { /* ... */ }`. The proposed syntax in this paper is consistent with
every other statement in C++ today.

## Language vs Library

There have been three popular pattern matching libraries in existence today.

  - Mach7
  - Simple Match by jbandela
  - MPark.Patterns

The issue of introducing identifiers is burdensome enough that I believe it
justifies a language feature.

## Optimizations

Comparison elision?

...

## Ranges

...

## User-defined Patterns

...

# Examples

...

# Other Languages and Libraries

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
inspect (s) {
  email [local, domain]: ...;
  us_phone_number [area_code, _, _]: ...;
}
```

struct Email {
  using is_pattern = void () const volatile;

  std::optional<tuple<std::string_view, std::string_view>> operator()(
      std::string_view sv) const;
};

Email? [address, domain]

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

## Fixed ranges

We propose to first support matching ranges with a fixed length.
The most obvious use-case is to allow matching strings.

The fixed-range pattern is denoted by `{x, y}`. It requires that
the have functions `size()`, `operator[]`. The pattern first checks
that `size()` matches the # of elements inside `{}` then unpacks
the range via `operator[]`. For example, given:

```
inspect (s) {
  {x, y}: s0;
}
```

`s0` is executed if `s.size()` == 2, `x` is `s[0]` and `y` is `s[1]`.
If constants appear within the pattern, the matched component must
subsequently match the pattern.
-->
