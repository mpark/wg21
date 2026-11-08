# Paper metadata

Every paper starts with a small block of YAML that tells the framework what the paper is: its title, number, date, audience, and authors. From those few lines the framework builds the standard WG21 header block, fills in the PDF's document title and the HTML page title, and adds [Latest] and [Status] links in HTML. After reading this file you will be able to write a complete front matter block, know exactly how each key appears in PDF and in HTML, control the table of contents, and use the less common keys for abstracts, acknowledgements, and document properties.

## The front matter block

Here is a complete front matter block with the keys most papers use:

````yaml
---
title: "`MPark/WG21` User's Guide"
subtitle: "Framework for Writing C++ Committee Proposals"
document: D0000R0
date: today
audience:
  - Library Evolution Working Group
  - Library Working Group
author:
  - name: Test Author
    email: <test@example.com>
  - name: Second Author
    email: <second@example.com>
toc-depth: 4
---
````

The block goes at the very top of the Markdown file, between two `---` lines, and ordinary Markdown headings and prose follow it. A few of these keys produce the standard WG21 header block, a table with the rows Document #, Date, Project, Audience, and Reply-to. The rows always come in this fixed order: Document #, Date, Project, Audience, an optional Revises row, then Reply-to. The Project row reads "Programming Language C++" without any key; there is no front matter key for it, so it cannot be changed per paper.

In PDF, the header opens page one: the title centered in large type, followed by a right-aligned two-column table of these facts, instead of Pandoc's stock LaTeX title. In HTML, the same facts appear as a table under the centered title.

The whole title block, the title heading plus the table, appears only when `title` is set, so a paper without a title loses the metadata table too. Always set both `title` and `document`: the framework's code reads both without a fallback, so a missing value is expected to make the build fail rather than warn.

There are no separate `abstract`, `reply-to`, or `tag` keys in the HTML header. Reply-to is built from `author`.

## Title and subtitle

`title:` sets the paper's title. It may contain inline code, and the backticks render as code:

````yaml
title: "`MPark/WG21` User's Guide"
````

The title renders as a centered top-level heading at the top of the paper. In PDF it prints centered in large type on page one; in HTML it is the centered heading above the header table, and, when the table of contents is on, it also heads the small-screen contents bar and the contents dialog.

The title does double duty as the document's name. It becomes the HTML page title shown in the browser tab and the PDF's document Title field. For those two uses it is converted back to Markdown text, so inline code in the title keeps its backticks there: the tab reads `` `MPark/WG21` User's Guide `` rather than showing code formatting.

`subtitle:` adds a subtitle under the title:

````yaml
subtitle: "Framework for Writing C++ Committee Proposals"
````

In PDF the subtitle prints on its own line directly under the title, in slightly larger type than body text. In HTML it appears centered in smaller type directly under the title. When `subtitle` is not set it is omitted entirely in both.

## Document number

`document:` records the paper number and revision:

````yaml
document: P2806R4
````

The value is printed verbatim in the Document # row, which always appears, so `document` is effectively required. The document number in the title block always comes from this field, never from the file name.

The expected format is a P or D number followed by an R revision, such as `P2806R4` or a draft `D0000R1`. When the value matches, HTML output adds [Latest] and [Status] links after the number, pointing at wg21.link. The links use the P number without the revision, so `P2806R4` links to `https://wg21.link/P2806` and `https://wg21.link/P2806/status`, and a draft `D0000R1` links to `https://wg21.link/P0000` and `https://wg21.link/P0000/status`. PDF output prints the document number in the Document # row with no [Latest] or [Status] links.

For building the links, the value is read case-insensitively, so `p1234r0` is also accepted, and trailing text after the revision is tolerated.

A value that does not fit the P or D, digits, R, digits form prints this warning and the build continues without those links:

````text
[WARNING] mpark/wg21: Document number '<document>' is an unrecognized format; expected "[PD]([0-9]+)R[0-9]+".
This just means that [Latest] and [Status] links will be missing.
````

In PDF, such a value still prints as written; the warning only matters for the HTML [Latest] and [Status] links.

## Date

`date:` sets the paper's date shown in the Date row. Write it in ISO `YYYY-MM-DD` form:

````yaml
date: 2026-01-01
````

The Date row always appears and shows the date exactly as written, in both PDF and HTML. The HTML page head also gets a machine-readable `dcterms.date` meta tag from the same value, for indexers and archivers.

To stamp the paper with the day you build it, write:

````yaml
date: today
````

`date: today` stamps the paper with today's date in `YYYY-MM-DD` (ISO 8601) format, so the Date row reads, for example, `2026-09-25` on the day of the build.

## Audience

`audience:` names the target audience, either as a single value or as a YAML list of groups:

````yaml
audience: WG21
````

````yaml
audience:
  - Library Evolution Working Group
  - Library Working Group
````

The Audience row always appears. With a list, each entry prints on its own line in the Audience row, in both PDF and HTML.

Always set `audience`. In PDF, omitting it entirely leaves the Audience row malformed, so the Reply-to row runs into it.

## Authors

`author:` lists one or more authors, each with `name:` and `email:`. The email is written in angle brackets:

````yaml
author:
  - name: Test Author
    email: <test@example.com>
  - name: Second Author
    email: <second@example.com>
````

`author` is a YAML list of mappings, each entry starting with `- name:`, not a plain string. Each author appears in the Reply-to row with the name on one line and the email, in angle brackets, on the next, and the email is a clickable mail link. In PDF, each name prints on its own row under Reply-to with each email on the next row in angle brackets, and one author may list several emails.

Two mistakes produce odd output:

- An author with only a `name:` shows an empty `<>` line under Reply-to in HTML, and just the name in PDF. Supply an `email:` for every author.
- An author written as a plain string instead of a `name:` entry prints nothing in the PDF Reply-to row.

## Abstract and thanks

Two keys add content to the PDF title area and are silently dropped from HTML output.

`abstract:` adds an abstract right after the title block and before the table of contents:

````yaml
abstract: "This paper proposes a new library facility."
````

`thanks:` attaches a footnote to the title, for acknowledgements or funding notes:

````yaml
thanks: "Thanks to the reviewers of earlier revisions."
````

In PDF, the abstract appears between the header table and the table of contents, and the thanks text appears as a footnote marked on the title. In HTML neither appears. If you want a summary in the HTML page for search engines and link previews, use `description:`, covered under [Other front matter keys](#other-front-matter-keys); it is distinct from `abstract`.

## Table of contents

A table of contents is generated by default, with no setup. It is placed after the title block and before the paper body; in PDF it also comes after the abstract and any include-before content.

### Turning it off

`toc: false` in the front matter turns the table of contents off for that paper:

````yaml
toc: false
````

In PDF the table of contents simply disappears. In HTML, `toc: false` removes every table-of-contents feature of the page: the wide-screen sidebar, the small-screen top bar, the contents dialog, and the contents script. The reader's view controls and theme switcher remain.

### Choosing the depth

`toc-depth` controls how many heading levels appear in the table of contents, and defaults to `3`. Given these headings:

````markdown
# Design Overview
## Types of Patterns
### Primary Patterns
#### Wildcard Pattern
````

the default depth leaves `#### Wildcard Pattern` out, because it is four levels deep. To include it:

````yaml
toc-depth: 4
````

Both PDF and HTML honor `toc-depth` from the paper's front matter. A few rules keep it working:

- A missing `toc-depth` key falls back to the default depth in both formats. For HTML, an empty or null value (`toc-depth:` or `toc-depth: ~`) also falls back to the default; for PDF this guide cannot confirm what a null value does, so leave the key out instead.
- Give it a whole number. The value is passed through without being checked, so a non-number such as `true` breaks it.
- For HTML output, put `toc-depth` in the metadata block at the very top of the first Markdown file. A `toc-depth` in a later file of a multi-file paper, or in a metadata block placed lower in the file, is ignored for HTML. If the first file does not open with a metadata block, the HTML build may also print a Python error in the terminal, but the build keeps going at the default depth.

### PDF-only table of contents keys

Four more keys affect only the PDF:

- `toc-title:` renames the table of contents heading, which is "Contents" by default. The HTML heading always reads "Contents", whatever you set.
- `toccolor:` sets the link color of table of contents entries. The framework default is black, while links in the body stay blue.
- `lof: true` adds a list of figures right after the table of contents.
- `lot: true` adds a list of tables right after the table of contents.

````yaml
toc-title: "Table of Contents"
lof: true
lot: true
````

## Other front matter keys

These keys are less common, and several affect only one output format.

`revises:` records which earlier revision this paper supersedes. It adds a Revises row between Audience and Reply-to only when the key is present, and the value is printed as written, with no links generated:

````yaml
revises: P2806R3
````

`keywords:` takes a list. It becomes a single comma-separated keywords meta tag in the HTML head. It is unrelated to `highlighting: keywords:`, which adds syntax-highlighting keywords (see [Extra C++ keywords](10-customization.md#extra-c-keywords)):

````yaml
keywords:
  - pattern matching
  - reflection
````

`description:` adds a page summary for search engines and link previews to the HTML head. It affects HTML only and is distinct from `abstract`, which appears only in PDF.

`subject:`, `author-meta:`, and `keywords:` are also standard Pandoc template variables for PDF document properties. The framework's LaTeX template does not use them itself; any effect comes from Pandoc's built-in LaTeX partials, which are not part of the framework, so this guide cannot confirm how they appear in the PDF. See the [Pandoc manual](https://pandoc.org/MANUAL.html#metadata-variables), and check a built PDF if those properties matter to you.

In HTML, an author meta tag appears only when plain-text author metadata can be derived; with the usual structured `name:` and `email:` authors, the output contains no author meta tag.

The framework's changelog mentions markup for local metadata overrides within part of a paper, but its syntax is not documented, so this guide cannot show it.

Several other keys live in front matter but belong with the features they control, and later files cover them: `secnumdepth` with [headings](05-headings-and-formatting.md#numbered-and-unnumbered-headings), `references` and `reference-section-title` with [the References section](09-stable-names-and-citations.md#the-references-section), and the highlighting, language, page layout, font, and color keys in [Customization](10-customization.md).

Previous: [Building papers](03-building.md) | Next: [Headings and formatting](05-headings-and-formatting.md)

*2026-09-25 - claude-opus-5.5*
