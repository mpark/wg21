# MPark/WG21 User Guide

If you have ever spent an evening fighting a word processor to get strikeouts, underlines, and margin paragraph numbers to look like the working draft, this framework is for you. MPark/WG21 lets you write a WG21 paper in plain Markdown, with a handful of extensions built for C++ proposals, and turns it into a committee-ready PDF, a single-file HTML page, or LaTeX source with one `make` command. Citations of WG21 papers, links to the working draft by stable name, section numbers, a table of contents, and a References section all appear without you writing any of them by hand. By the end of this guide you will be able to set up a paper repository, write every construct a proposal needs (wording changes, paragraph numbers, notes, examples, grammar, comparison tables), build and preview your papers, and tune the output when the defaults are not what you want.

## What it is

MPark/WG21 is a Pandoc-based framework for improving both the authoring and the reviewing experience of C++ proposals. Its two stated goals are ease of authoring papers and ease of reviewing them.

**Markdown in, PDF, HTML, or LaTeX out.** You write your paper in Pandoc's Markdown dialect: headings, lists, tables, fenced code blocks, YAML front matter, and `[@...]` citations, plus a `==highlight==` extension. The framework produces the paper as PDF (through LaTeX, using `xelatex`), as HTML, or as LaTeX source in a `.latex` file. The HTML version is a single self-contained file that works when emailed, uploaded, or opened offline.

**Extensions built for C++ proposals.** On top of ordinary Markdown, the framework adds markup for the things committee papers actually contain: added and removed wording, paragraph numbers in the margin, notes and examples in the standard's style, editorial and drafting notes, grammar productions, before and after comparison tables, and Markdown embedded inside code so you can italicize exposition-only names or mark changes inside a code block.

**Citations and stable names for free.** Cite any document in the wg21.link index, such as `[@P1240R2]` or `[@CWG1234]`, and it becomes a link plus a full References entry with author, date, and title; you write no bibliography. Write a working-draft stable name such as `[basic.life]` and it becomes a link to that section of the draft at eel.is.

**make-driven builds with a pinned toolchain.** You build with `make`. The first build downloads a pinned Pandoc (version 3.9.0.2) and sets up a private Python environment inside the framework checkout, so every co-author builds with the same Pandoc no matter what is installed on their machine. You add the framework to your repository as a git submodule and include one Makefile fragment.

## A first look

Here is a complete short paper. It has front matter, two headings, a citation, and one removed and one added phrase of proposed wording.

````markdown
---
title: "A Sample Paper"
document: P0000R0
date: 2026-01-01
audience: WG21
author:
  - name: Test Author
    email: <author@example.com>
---

# Introduction

This paper follows the direction suggested in [@P1240R2].

# Wording

Remove some [old *text*]{.rm} and add some [new **text**]{.add}.
````

Save it as `p0000r0.md` at the top of a repository whose `Makefile` is the single line `include wg21/flat.mk`, with the framework checked out as the `wg21` submodule. Then build the PDF:

````bash
make p0000r0.pdf
````

The result is `generated/p0000r0.pdf`. Page one opens with the title centered in large type and a right-aligned table of paper facts: Document #, Date, Project (always "Programming Language C++"), Audience, and Reply-to with the author's name and email. A table of contents follows, then the numbered sections "1 Introduction" and "2 Wording". The citation shows as the bracketed label `[P1240R2]` and links straight to the paper on wg21.link. The removed phrase prints in red with a strikeout and the added phrase in green with an underline. A numbered References section at the end lists the cited paper. Run `make p0000r0.html` instead and you get `generated/p0000r0.html`, with the same content, the table of contents as a navigation sidebar on wide screens, and [Latest] and [Status] links next to the document number.

Each piece is explained later in this guide:

- The front matter block: [Paper metadata](04-paper-metadata.md#the-front-matter-block)
- The one-line Makefile and the `generated/` folder: [The flat layout](02-project-layouts.md#the-flat-layout)
- The build command: [Building one paper](03-building.md#building-one-paper)
- What the first build downloads: [What the first build does](01-getting-started.md#what-the-first-build-does)
- The added and removed phrases: [Adding and removing text](07-wording.md#adding-and-removing-text)
- The citation and the References section: [Citing papers](09-stable-names-and-citations.md#citing-papers)

## How this guide is organized

Read the files in this order. Each one builds only on the files before it.

1. [Getting started](01-getting-started.md): what to install on macOS, Ubuntu, and Debian, adding the framework as a submodule, building your first paper, and what the first build sets up for you.
2. [Project layouts](02-project-layouts.md): the flat layout (all papers in one directory) and the per-paper layout (one directory per paper), mapping a source file to a paper number, and shared and machine-local settings.
3. [Building papers](03-building.md): every make target and variable, the output directory, cleaning up, refreshing data, the live preview server, and the build errors make can print.
4. [Paper metadata](04-paper-metadata.md): the front matter keys that build the title block, the table of contents settings, and the other per-paper keys.
5. [Headings and formatting](05-headings-and-formatting.md): numbered and unnumbered headings, section references, emphasis, underline, superscript and subscript, highlighting, and raw HTML.
6. [Code](06-code.md): inline code and code blocks, highlighting defaults, not-proposed code, and embedded Markdown inside code with its delimiters.
7. [Wording](07-wording.md): added and removed text, the wording block, paragraph numbers, list-based paragraphs, notes, examples, editorial and drafting notes, and grammar.
8. [Comparison tables](08-comparison-tables.md): before and after tables built from code blocks, their variants, and how they render.
9. [Stable names and citations](09-stable-names-and-citations.md): links to the working draft, explicit stable names with section numbers and titles, citing papers and issues, and the References section.
10. [Customization](10-customization.md): your own Pandoc defaults file, extra Python packages, highlighting and embedded Markdown settings, fonts, page layout, and colors.
11. [Output and troubleshooting](11-output-and-troubleshooting.md): what PDF and HTML readers get, the differences between the two, and every warning and error with its fix.
12. [Quick reference](12-quick-reference.md): tables of every syntax form, front matter key, make target, and make variable, each linked to its explanation.

## Resources

- The full User's Guide, rendered as HTML: <https://mpark.github.io/wg21/MANUAL.html>
- The full User's Guide, rendered as PDF: <https://mpark.github.io/wg21/MANUAL.pdf>
- The User's Guide source, `MANUAL.md` in the framework repository, is itself written with the framework, so comparing it with the published HTML and PDF shows how each piece of syntax renders. The repository's `README.md` is only an overview that links to the guide.
- The example paper repository, a real set of papers set up to build with the framework: <https://github.com/mpark/wg21-papers>
- The author's blog post, "How I format my C++ papers": <https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers>
- The C++Now 2019 lightning talk, "WG21 Paper in Markdown": <https://www.youtube.com/watch?v=8yReHZOw6QY>

*2026-09-25 - claude-opus-5.5*
