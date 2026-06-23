---
title: "Heading Tests"
document: D0000R1
date: 2026-01-01
audience:
  - Library Evolution
author:
  - name: Test Author
    email: <test@example.com>
toc: true
toc-depth: 3
---

# Headings

## Automatic Header Links {#auto-header-links}

Automatic header links are written as `[](#auto-header-links)`{.markdown},
and render as [](#auto-header-links).

## Inline Code in Headers: `int`{.cpp}, `x & y`{.cpp}

This heading checks highlighted inline code in section titles.

## Disabled Numbering {-}

This heading should not show a section number.

## Unlisted Heading {- .unlisted}

This heading should not show a section number and should be absent from the TOC.

### [intro.compliance.general]{.sref} {-}

This heading checks stable-name references in an unnumbered section heading.
