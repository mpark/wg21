---
title: Slides Test
subtitle: Presentation Subtitle
author:
  - name: Slide Author
    email: <slides@example.com>
document: D1234R5
date: today
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

```cpp
match ($value$) {}
```

::: notes
Speaker notes for the shared-formatting slide.
:::

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
