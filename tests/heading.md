---
title: "Heading Tests"
document: D0000R1
source: https://github.com/mpark/wg21/blob/master/tests/heading.md?plain=1
date: 2026-01-01
audience:
  - Library Evolution
author:
  - name: Test Author
    email: <test@example.com>
toc: true
toc-depth: 3
---

# Revision History {- .unlisted .collapsed}

## R0 → R1 {- .unlisted}

The revision history is collapsed in HTML output.

# Numbered Collapsed Section {.collapsed}

## Nested Top-Level Section {- .unlisted}

The disclosure marker precedes a top-level section number.

# Headings

## Numbered Collapsed Subsection {.collapsed}

### Nested Subsection {- .unlisted}

The disclosure marker precedes a subsection number.

## Unlisted Collapsed Subsection {- .unlisted .collapsed}

### Nested Unlisted Subsection {- .unlisted}

An unlisted subsection uses the triangle in place of a section number.

## Third-Level Headings

### Numbered Collapsed H3 {.collapsed}

#### Nested H4 {- .unlisted}

Collapsed sections also work below the subsection level.

### Following H3 {- .unlisted}

This heading is outside the collapsed H3 section.

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
