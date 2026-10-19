---
title: Slides Test
subtitle: Presentation Subtitle
author:
  - name: Slide Author
    email: <slides@example.com>
document: D1234R5
date: today
project: Programming Language C
audience: WG21
highlighting:
  keywords:
    cpp: match
---

# Overview

## Shared Formatting

Slides can use the same formatting features as papers.

::: add
This wording is added.
:::

Replace [old](new){.sub}. See [basic.scope], [basic.life]{.sref}, and
[@P2688R5]{.title}.

```{.cpp numberLines="1|2" startFrom=7}
match ($value$) {}
return;
```

```{.javascript numberLines="1-2|3"}
const one = 1;
const two = 2;
console.log(one + two);
```

```{.default .raw}
Plain code.
```

```{.default .raw .numberLines startFrom=9}
Numbered plain code.
```

```{.text numberLines="1|2" startFrom=7}
First line of text.
Second line of text.
```

::: notes
Speaker notes for the shared-formatting slide.
:::

## Animated Code {data-auto-animate= data-auto-animate-duration=0.5}

```{.cpp .numberLines data-id="code-animation"}
int one = 1;
```

## Animated Code {data-auto-animate= data-auto-animate-duration=0.5}

```{.cpp .numberLines data-id="code-animation"}
int one = 1;
int two = 2;
```

# Proposal

## Comparison Table

::: cmptable

### Before
```cpp
old();
```

### After
```cpp
new();
```

:::

## Wording

::: wording
#. First paragraph.

#. [A numbered note.]{.note}
:::
