---
title: "Note Tests"
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

# Notes

There are three supported styles of note:

- Use the `note` class for notes that are expected to appear in the specification wording.
  ```
  [Notes will look like this]{.note}
  ```
  [Notes will look like this]{.note}

- Use `ednote` for editorial notes.
  ```
  [Editorial notes are important]{.ednote}
  ```
  [Editorial notes are important]{.ednote}

- Use `draftnote` to include text that is intended as questions or information for reviews and
  working groups.
  ```
  [Drafting notes can be used to provide comments for reviewers that are explicitly not to be
   included in the specification.]{.draftnote}

  [It is also possible to indicate that a note is for
   a specific `audience` via this optional attribute.]{.draftnote audience="the reader"}
  ```
  [Drafting notes can be used to provide comments for reviewers that are explicitly not to be
   included in the specification.]{.draftnote}

  [It is also possible to indicate that a note is for
   a specific `audience` via this optional attribute.]{.draftnote audience="the reader"}
