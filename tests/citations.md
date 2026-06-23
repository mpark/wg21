---
title: "Citation Tests"
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

# Citation

Automatic references are written as `[@N4762]`{.default} and render as [@N4762].
Anything in <https://wg21.link/index.yaml> is linked automatically.

  - `N` Papers (e.g., `[@N3887]`{.default} -> [@N3887])
  - `P` Papers (e.g., `[@P1371R1]`{.default} -> [@P1371R1])
  - CWG Issues (e.g., `[@CWG1234]`{.default} -> [@CWG1234])
  - LWG Issues (e.g., `[@LWG1234]`{.default} -> [@LWG1234])
  - Github Edits (e.g., `[@EDIT1234]`{.default} -> [@EDIT1234])
  - Standing Documents (e.g., `[@SD6]`{.default} -> [@SD6])

You may also write `[@P2996R8]{.title}`{.default} to include the title of the paper,
which renders as: [@P2996R8]{.title}.
