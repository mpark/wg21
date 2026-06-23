---
title: "Modify Text Tests"
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

```
$unspecified$ @[foo](bar){.sub}@();
```

# Wording Changes

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
| `%a`      | The locale's abbreviated weekday name. If the value does not       |
|           | contain a valid weekday, [`setstate(ios::failbit)` is called]{.rm} |
|           | [`format_error` is thrown]{.add}.                                  |
+-----------+--------------------------------------------------------------------+
| `%A`      | The locale's full weekday name. If the value does not contain      |
|           | a valid weekday, [`setstate(ios::failbit)` is called]{.rm}         |
|           | [`format_error` is thrown]{.add}.                                  |
+-----------+--------------------------------------------------------------------+
