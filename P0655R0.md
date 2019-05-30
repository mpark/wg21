---
title: "`visit<R>`: Explicit Return Type for `visit`"
document: P0655R0
date: 2017-10-14
audience: Library Evolution Group
author:
  - name: Michael Park
    email: <mcypark@gmail.com>
  - name: Agustín Bergé
    email: <agustinberge@gmail.com>
toc: false
---

# Introduction

This paper proposes to allow visiting `variant`s with an explicitly specified
return type.

# Motivation and Scope

Variant visitation requires invocation of all combinations of alternatives to
result in the same type, such type is deduced as the visitation return type.
It is sometimes desirable to explicitly specify a return type to which all
the invocations are implicitly convertible to, as if by _`INVOKE`_`<R>` rather
than _`INVOKE`_:

```cpp
struct process {
  template <typename I>
  auto operator()(I i) -> O<I> { /* ... */ };
};

std::variant<I1, I2> input = /* ... */;

// mapping from a `variant` of inputs to a `variant` of results:
auto output = std::visit<std::variant<O<I1>, O<I2>>>(process{}, input);

// coercing different results to a common type:
auto result = std::visit<std::common_type_t<O<I1>, O<I2>>>(process{}, input);

// visiting a `variant` for the side-effects, discarding results:
std::visit<void>(process{}, input);
```

In all of the above cases the return type deduction would have failed, as each
invocation yields a different type for each alternative.

# Impact on the Standard

This proposal is a pure library extension.

# Proposed Wording

Modify __§23.7.2 [variant.syn]__ of [@N4687] as indicated:

```diff
  // 23.7.7, visitation
  template <class Visitor, class... Variants>
    constexpr @_see below_@ visit(Visitor&&, Variants&&...);
+  template <class R, class Visitor, class... Variants>
+    constexpr R visit(Visitor&&, Variants&&...);
```

Add new paragraphs to __§23.7.7 [variant.visit]__ of [@N4687]:

> ```diff
> + template <class R, class Visitor, class... Variants>
> +   constexpr R visit(Visitor&& vis, Variants&&... vars);
> ```
> ::: add
>> _Requires_: The expression in the _Effects_: element shall be
>> a valid expression for all combinations of alternative types
>> of all variants.  Otherwise, the program is ill-formed.
>>
>> _Effects_: Let `is...` be `vars.index()...`. Returns
>> _`INVOKE`_`<R>(forward<Visitor>(vis), get<is>(forward<Variants>(vars))...);`.
>>
>> _Throws_: `bad_variant_access` if any `variant` in `vars` is
>> `valueless_by_exception()`.
>>
>> _Complexity_: For `sizeof...(Variants) <= 1`, the invocation of the callable
>> object is implemented in constant time, i.e. it does not depend on
>> `sizeof...(Types)`. For `sizeof...(Variants) > 1`, the invocation of
>> the callable object has no complexity requirements.
> :::

# Design Decisions

There is a corner case for which the new overload could clash with the existing
overload. A call to `std::visit<Result>` actually performs overload resolution
with the following two candidates:

```cpp
template <class Visitor, class... Variants>
constexpr decltype(auto) visit(Visitor&&, Variants&&...);

template <class R, class Visitor, class... Variants>
constexpr R visit(Visitor&&, Variants&&...);
```

The template instantiation via `std::visit<Result>` replaces `Visitor` with
`Result` for the first overload, `R` with `Result` for the second, and
we end up with the following:

```cpp
template <class... Variants>
constexpr decltype(auto) visit(Result&&, Variants&&...);

template <class Visitor, class... Variants>
constexpr Result visit(Visitor&&, Variants&&...);
```

This results in an ambiguity if `Result&&` happens to be the same type as
`Visitor&&`. For example, a call to `std::visit<Vis>(Vis{});` would be
ambiguous since `Result&&` and `Visitor&&` are both `Vis&&`.

In general, we would first need a self-returning visitor, then an invocation
to `std::visit` with the same type __and__ value category specified for
the return type __and__ the visitor argument.

We claim that this problem is not worth solving considering the rarity of
such a use case and the complexity of a potential solution.

Finally, note that this is not a new problem since `bind` already uses
the same pattern to support `bind<R>`:

```cpp
  template <class F, class... BoundArgs>
    @_unspecified_@ bind(F&&, BoundArgs&&...);
  template <class R, class F, class... BoundArgs>
    @_unspecified_@ bind(F&&, BoundArgs&&...);
```

# Implementation Experience

  - [`MPark.Variant`][mpark/variant] implements `visit<R>` as proposed in
    the [`visit-r`][visit-r] branch.
  - [`Eggs.Variant`][eggs/variant] has provided an implementation of `visit<R>`
    as `apply<R>` since 2014, and also handles the corner case mentioned in
    [Design Decisions](#design-decisions).

[visit-r]: https://github.com/mpark/variant/tree/visit-r
[mpark/variant]: https://github.com/mpark/variant
[eggs/variant]: https://github.com/eggs-cpp/variant

# Future Work

There are other similar facilities that currently use _`INVOKE`_, and
do not provide an accompanying overload that uses _`INVOKE`_`<R>`.
Some examples are `std::invoke`, `std::apply`, and `std::async`.

There may be room for a paper with clear guidelines as to
if/when such facilities should have an accompanying overload.

---
references:
  - id: N4687
    citation-label: N4687
    title: "Working Draft, Standard for Programming Language C++"
    issued:
      year: 2017
    URL: http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4687.pdf
---
