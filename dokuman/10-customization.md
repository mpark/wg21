# Customization

The framework's defaults match the C++ working draft closely, so most papers need no configuration at all. When you do want something different, there are two places to change it: front matter keys in the paper itself, for per-paper metadata, layout, and colors, and your own Pandoc defaults file, for Pandoc-level settings such as section numbering, the template, and the citation style. After reading this file you will know which lever to reach for, how settings are layered, and every documented knob: highlighting and embedded Markdown defaults, extra C++ keywords, stable-name numbering, fonts, page layout, link and change colors, language, extra head and body content, and a few PDF-only options.

## How settings are layered

Every paper inherits framework-wide settings without writing them: A4 paper, 10pt font, margins copied from the C++ working draft, blue links, a "References" section title, linked citations, English as the language, and the colors used for changed wording in PDF. Any inherited setting can be overridden for one paper by setting the same key in that paper's front matter:

````yaml
---
title: "A Letter-Sized Paper"
document: P0000R0
date: 2026-01-01
audience: WG21
author:
  - name: Test Author
    email: <test@example.com>
papersize: letter
---
````

This paper prints on US letter paper; everything else stays at the framework's defaults.

One rule matters more than any other here. A list-valued setting in the front matter, such as `geometry`, `classoption`, `header-includes`, or `embedded-md-code-classes`, replaces the framework's list as a whole; it is not merged. So when you set one of these, write out the complete list you want, including any default entries you mean to keep. Each section below points out where this bites.

## Your own defaults file

For settings that live at the Pandoc level rather than in paper metadata, add your own Pandoc defaults file. Name it with the `DEFAULTS` make variable, or drop in a top-level `defaults.yaml`, which the flat layout picks up automatically; [Your own defaults and packages](03-building.md#your-own-defaults-and-packages) covers the make side. The file is applied after the framework's own defaults, which makes source, output, bibliography, and highlighting behavior configurable:

````yaml
# defaults.yaml
number-sections: false
````

With this file in place, every paper built from the repository has unnumbered headings, in both PDF and HTML.

Single-value keys you set in your own defaults file take precedence over the framework's. The keys the sources name for this file are:

- `number-sections`, which turns section numbering on or off (on by default).
- `table-of-contents`, the Pandoc-level switch for the table of contents (per paper, `toc: false` in front matter does the same).
- `template`, which chooses the template. The WG21 paper layout, including the title block built from `title`, `document`, `date`, `audience`, and `author`, comes from the framework's `wg21` template, chosen automatically for HTML or for PDF and LaTeX; set `template:` to use a different one.
- `csl`, which chooses the citation style. Citations and the References section use the framework's own WG21 citation style (`csl: wg21`) instead of a generic academic one, and an ACM style ships alongside the WG21 one.
- `bibliography` and `pdf-engine`.
- `css` and `filters`, covered in [Stylesheets and filters](#stylesheets-and-filters).
- `resource-path`. Framework resources such as the bibliography, stylesheets, and favicon resolve by short names no matter which folder your paper lives in, because Pandoc's resource search path is set to the framework's data directory. Images referenced relative to your paper's own folder may need `.` added to `resource-path`; no test covers this.
- `id-prefix`, covered in [Prefixing HTML ids](#prefixing-html-ids).
- `html-math-method`, which changes how HTML renders math (MathML by default).

Whether list keys such as `css`, `filters`, `metadata-files`, and `resource-path` add to or replace the framework's lists is Pandoc behavior the framework does not state, so test the output when you set one.

Two limits apply. First, your own defaults file takes effect for the main build, but code and embedded-Markdown fragments are formatted with the framework's own formatting defaults only, so overriding `syntax-definition` or `syntax-highlighting` in your file does not reach most code. Math inside embedded code fragments, such as `@$\frac{a+b}{2}$@`, always stays MathML even if you change `html-math-method`. Second, build papers through make: the framework's defaults point at its own data directory, which make hands to Pandoc on every build, so running Pandoc by hand without that same data directory breaks those paths.

Every build runs three filters in a fixed order: the framework's citation-title filter, Pandoc's built-in `citeproc`, and then the framework's main WG21 filter. Whether adding `filters:` in your own defaults file appends to or replaces this chain is not stated.

### Prefixing HTML ids

Every element id in an HTML paper can be namespaced under a prefix, so the paper can be embedded in a larger page without id collisions. Add Pandoc's `id-prefix:` key to your own defaults file; there is no make variable for it:

````yaml
# defaults.yaml
id-prefix: paper-
````

With this prefix, `# Heading` gets the id `paper-heading`, contents links become `#paper-heading`, and the contents navigation and dialog ids and their controls are renamed to match (`paper-TOC`, `paper-toc-dialog`). This affects HTML only.

## Extra Python packages

If your own Pandoc filters or Makefile rules need Python packages the framework does not install, name a pip requirements file with the `REQUIREMENTS` make variable, or drop a top-level `requirements.txt` into a flat-layout repository. The packages are installed into the build's private Python environment alongside the framework's own. The file uses the usual pip requirements format, one package per line, either pinned (`name==version`) or bare:

````text
# requirements.txt
package-name==1.0.0
another-package
````

Nothing about the paper's output changes by itself; the packages become available to your filters and recipes. Extra Python requirements are tracked as build dependencies, so:

- The Python environment is rebuilt from scratch whenever your `REQUIREMENTS` file, the framework's own requirements, or its environment installer changes. That rebuild also re-runs the citation and stable-name downloads and then rebuilds your papers.
- To remove a Python package, delete it from your requirements file and rebuild. The old environment is wiped before every install, so nothing stale lingers.
- Command-line tools installed by your requirements files can be used directly in your Makefile recipes, because the environment's `bin` directory is on the PATH for every recipe.

## Default language for code

The built-in highlighting defaults are:

````yaml
highlighting:
  inline-code: cpp
  code-block: default
````

That is, inline code is C++ highlighted and code blocks are plain. To make fenced code blocks C++ highlighted by default for the whole paper, set this in the paper's metadata block:

````yaml
highlighting:
  code-block: cpp
````

Unlabeled code blocks then render with C++ colors in both PDF and HTML, as if each had ```` ```cpp ````; blocks with their own language keep it.

To stop inline code from being C++ highlighted by default for the whole paper:

````yaml
highlighting:
  inline-code: default
````

Unlabeled inline code then prints as plain monospace. You can set both entries at once, and per-element classes such as `{.cpp}` or `{.default}` still override the paper default for one piece of code.

## Extra C++ keywords

Proposals often introduce new keywords that the highlighter does not know. List them under `highlighting.keywords.cpp` in the paper's YAML metadata block:

````yaml
highlighting:
  keywords:
    cpp:
      - match
````

After that, `match` is highlighted as a keyword in C++ code:

````markdown
```cpp
f() match {
  case 0 => 0;
  case auto y => y - x;
};
```
````

`match` now gets the keyword color in both PDF and HTML. A single extra keyword can use the scalar shorthand instead of a one-item list:

````yaml
highlighting:
  keywords:
    cpp: match
````

Every C++ code element is re-highlighted with the extra keywords, even when it contains no embedded Markdown. That includes ```` ```cpp ```` blocks marked `{.raw}` and unlabeled inline code, which is C++ by default. The same line in an unhighlighted block stays plain. In PDF, custom keywords are not applied to inline code inside section headings.

Only the `cpp` language is supported for extra keywords. Keywords listed under `highlighting.keywords` for any other language are silently ignored.

`highlighting.keywords` is unrelated to the top-level `keywords:` front matter key, which fills document metadata; see [Other front matter keys](04-paper-metadata.md#other-front-matter-keys).

## Which code gets embedded Markdown

The `embedded-md-code-classes` metadata list sets which code classes get embedded Markdown by default, paper-wide. Its built-in value is `cpp`, `default`, and `diff`. Any code whose class is listed gets embedded Markdown automatically, with no `.embed_md`. To add NASM and Rust:

````yaml
embedded-md-code-classes:
  - cpp
  - default
  - diff
  - nasm
  - rust
````

Now ```` ```rust ```` and ```` ```nasm ```` blocks process `@...@` and `$...$` like C++ code does, without `.embed_md` on each one. Because the list is an override, you must list the defaults again to keep them; a list of just `rust` would turn embedded Markdown off for C++ code. `.raw` still opts a single element out.

## Section numbers on stable names

By default, explicit stable names such as `[basic.life]{.sref}` render with a leading section number and the section title, as in "6.8.4 Lifetime [basic.life]". To turn the numbers off for every explicit stable name in the paper, set:

````yaml
number-srefs: false
````

Every `.sref` reference then renders as "Lifetime [basic.life]". This is the paper-wide version of writing `[basic.life]{- .sref}` or `[basic.life]{.unnumbered .sref}` on each one. The default is `number-srefs: true`.

## Unicode fonts

If you build PDF output from a paper with Unicode characters, you may want to choose specific fonts through Pandoc's standard [font variables](https://pandoc.org/MANUAL.html#fonts) in the front matter. For example, `monofont:` chooses the font for code elements:

````yaml
monofont: "DejaVu Sans Mono"
````

Code in the PDF is then set in DejaVu Sans Mono, which provides glyphs for a large share of Unicode characters. HTML output is not affected. To see which fonts are installed, `fc-list` lists them on most systems.

The other font keys are standard Pandoc LaTeX template variables that pass through because the template includes Pandoc's partials: `mainfont`, `mainfontoptions`, `sansfont`, `sansfontoptions`, `mathfont`, `mathfontoptions`, `mathspec`, `fontfamily`, `fontfamilyoptions`, `fontfamilies`, `CJKmainfont`, `CJKsansfont`, `CJKmonofont`, `CJKoptions`, `microtypeoptions`, `zero-width-non-joiner`, `fontenc`, `mainfontfallback`, `sansfontfallback`, `monofontfallback`, `luatexjapresetoptions`, and `luatexjafontspecoptions`. The framework does not document them; see the [LaTeX variables](https://pandoc.org/MANUAL.html#variables-for-latex) section of the Pandoc manual for what each one does.

## Page and color defaults

These front matter keys adjust the PDF page and its colors. None of them affects HTML, whose layout and colors come from the framework's stylesheet.

### Page layout

- `papersize:` changes the paper size from the framework default A4, which matches the C++ working draft. Write the bare size name, such as `papersize: letter`, because "paper" is appended for you.
- `fontsize:` changes the base font size from the framework default 10pt, which matches the C++ working draft.
- `geometry:` sets page margins as a list of geometry options. The framework defaults, copied from the C++ working draft, are `left=2.245cm`, `right=2.245cm`, `top=2.5cm`, and `bottom=2.5cm`, and setting `geometry` in a paper replaces all four.
- `classoption:` passes extra LaTeX document class options. The framework defaults are `oneside` and `final`, taken from the C++ working draft; setting the key replaces both.
- `documentclass:` switches the LaTeX document class from Pandoc's default `article`. Book-style classes such as book, memoir, and scrbook also get front matter, main matter, and back matter divisions.
- `linestretch:` adjusts body line spacing, for example `1.25`, and applies only after the title block and table of contents.
- `beamerarticle: true` loads the beamerarticle package before any other package.

`indent` and `pagestyle` are standard Pandoc LaTeX template variables that pass through because the template includes Pandoc's partials; see the Pandoc manual's [LaTeX variables](https://pandoc.org/MANUAL.html#variables-for-latex) section for them.

Because `geometry` is a list, set all four margins even if you only want to change one:

````yaml
papersize: letter
fontsize: 11pt
geometry:
  - left=2cm
  - right=2cm
  - top=2.5cm
  - bottom=2.5cm
linestretch: 1.25
````

This gives a letter-sized PDF with 11pt type, narrower side margins, and looser line spacing in the body.

### Link colors

PDF links are colored by default. Internal links (`linkcolor`), citations (`citecolor`), and URLs (`urlcolor`) are blue, and table of contents entries use `toccolor`, black by default. Setting any of these keys changes that color, and they accept named colors such as `Maroon`, `NavyBlue`, or `ForestGreen`:

````yaml
linkcolor: NavyBlue
citecolor: ForestGreen
urlcolor: Maroon
````

`filecolor`, `colorlinks`, and `boxlinks` are standard Pandoc LaTeX template variables that pass through because the template includes Pandoc's partials; see the Pandoc manual's [LaTeX variables](https://pandoc.org/MANUAL.html#variables-for-latex) section for them.

### Colors for changed wording

Three keys set the PDF colors for wording changes and `diff` code:

- Added text prints green (`addcolor: '006e28'`), both for `::: add` and `[...]{.add}` markup and for added lines in `diff` code.
- Removed text prints red (`rmcolor: 'bf0303'`), both for `::: rm` and `[...]{.rm}` markup and for removed lines in `diff` code.
- Unchanged lines in `diff` code print gray (`uccolor: '898887'`).

The values must be six-digit hex colors written without `#`; quote them as the framework does:

````yaml
addcolor: '006e28'
rmcolor: 'bf0303'
uccolor: '898887'
````

These are the defaults; put your own hex values in their place. In code blocks, the diff recoloring applies only to that block. HTML colors come from the framework stylesheet and are not affected by these keys.

## Language and text direction

The document language defaults to English (`lang: en`), which drives the HTML language attribute and PDF hyphenation. Set another language with `lang:` in the front matter:

````yaml
lang: de
````

In HTML, `lang:` and `dir:` (text direction) are written onto the page's root element. In PDF, `lang:` also sets the document class language, loads babel with language shorthands off, and fills the PDF's language metadata field.

Text marked with other `lang` attributes adds those languages to the PDF document class options. For PDF, `dir:` and the babel keys `babeloptions`, `shorthands`, and `babelfonts` are standard Pandoc LaTeX template variables that pass through because the template includes Pandoc's partials; see the Pandoc manual's [LaTeX variables](https://pandoc.org/MANUAL.html#variables-for-latex) section for them.

## Extra content in the head and body

### header-includes

`header-includes:` in the front matter injects extra raw content into the document preamble. For HTML, that means raw HTML in the page head, such as meta tags, scripts, or style overrides. For PDF, raw LaTeX in `header-includes:` lands after the template's font and common package setup and before hyperlink setup, so it can redefine commands and environments.

Be careful with this key. The framework's default metadata already sets `header-includes` to a LaTeX preamble that supplies macros PDF features rely on: margin paragraph numbers, the underline and strikeout package used for added and removed text, the not-proposed box and its colors, dash list bullets, the quote indent, and the bibliography's hanging indent. Setting `header-includes:` in your own front matter replaces that whole block rather than adding to it, so copy those lines into yours to keep those features. This applies even if you only meant to add something for HTML, because the one key feeds both formats.

### include-before and include-after

Two more keys insert raw content at fixed points, and they land in different places in each format:

- `include-before` content, set through Pandoc's `include-before-body` option, is inserted just above the title block in HTML. In PDF, `include-before:` content is inserted right after the title block and abstract, before the table of contents.
- `include-after` content, set through Pandoc's `include-after-body` option, is appended after the paper body, still inside the page wrapper, in HTML. In PDF, `include-after:` content goes at the very end of the document, after the bibliography.

## Other PDF options

A few more front matter keys affect PDF only.

`pdf-trailer-id:` pins the PDF trailer ID, for reproducible PDF builds; the template writes it for xelatex as well as for pdfTeX and LuaTeX. The value is placed as-is inside the trailer ID's square brackets, so check the Pandoc manual for its expected format before using it.

The template also has natbib and biblatex bibliography branches, which read `biblio-title:`; they stay inactive in the default build, because it formats citations with Pandoc's `citeproc`.

The remaining keys are standard Pandoc LaTeX template variables that pass through because the template includes Pandoc's partials: `links-as-notes`, `urlstyle`, `pdfstandard`, `hyperrefoptions`, `csquotes`, `csquotesoptions`, `biblio-style`, `natbiboptions`, and `biblatexoptions`. The framework does not document them; see the [LaTeX variables](https://pandoc.org/MANUAL.html#variables-for-latex) section of the Pandoc manual.

## Stylesheets and filters

You can add your own stylesheet or Pandoc filter by listing it under `css:` or `filters:` in your `DEFAULTS` file, which is applied after the framework's built-in defaults:

````yaml
# defaults.yaml
css:
  - my-styles.css
filters:
  - my-filter.py
````

A stylesheet listed this way ends up embedded in the self-contained HTML. Whether your list is appended to the framework's list or replaces it has not been tested, so check the output carefully after adding either key. If your filter needs Python packages, name them in a requirements file as described in [Extra Python packages](#extra-python-packages), and if you want `make serve` to notice edits to your filter, add it to `WATCHDEPS` as described in [The live server](03-building.md#the-live-server).

Previous: [Stable names and citations](09-stable-names-and-citations.md) | Next: [Output and troubleshooting](11-output-and-troubleshooting.md)

*2026-09-25 - claude-opus-5.5*
