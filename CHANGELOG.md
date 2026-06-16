# Changelog

This changelog is derived from the Git history. The repository does not use
version tags, so entries are grouped by year and month and focus on high-level
features, paper milestones, and large implementation changes.

## 2026

### June 2026

- Added `MANUAL.md` as the source for the up-to-date user's guide, generated
  `MANUAL.html` and `MANUAL.pdf`, and changed GitHub Pages deployment to
  publish the manual as the project website.
- Trimmed `README.md` down to a project overview and links to the generated
  manual instead of duplicating detailed framework documentation.
- Added a `render` filter for manual examples that show Markdown source next
  to the rendered output without relying on the older side-by-side test tool.
- Added `::: wording` support for automatic paragraph-number handling in
  proposed wording, including nested bullet and decimal lists, pinned numbers,
  and suppressed numbering.
- Added paragraph suffix stable references such as `[stable.name]/1`, and
  improved stable-name data generation through `srefs.json` and `srefs.md`.
- Added explicit embedded-Markdown opt-in and delimiter customization for code
  elements while preserving default embedded-Markdown behavior for configured
  code languages.
- Factored formatting filters so generated fragments are processed more
  consistently with top-level documents.
- Switched generated HTML math rendering from MathJax to MathML.
- Refreshed C++ syntax highlighting around an upstream KDE syntax definition,
  a smaller WG21-specific syntax patch, and YAML-provided highlighting CSS and
  LaTeX macros.
- Fixed LaTeX output for PDF metadata, title and table-of-contents link
  targets, and inline highlighted code inside strikeout, underline, and mark
  spans.
- Improved build behavior by avoiding unnecessary virtual-environment rebuilds
  during `make update` and writing generated reference files through temporary
  outputs before replacing existing files.
- Upgraded the framework to Pandoc 3.9.0.2 and Panflute 2.3.1, including
  refreshed default HTML and LaTeX templates.
- Updated WG21-specific template patches so they apply cleanly on top of the
  Pandoc 3.9.0.2 defaults with a smaller set of local changes.
- Adjusted CSL and citation-title handling for Pandoc 3.x while preserving
  WG21-style reference rendering.
- Moved static WG21 HTML overrides into a separate `wg21.css` file, leaving
  template-driven color rules in `wg21.html`.
- Fixed generated table styling for Pandoc 3.x HTML output, including the
  document information table in the title block.
- Disabled raw HTML parsing for Markdown input so C++-style angle brackets are
  not silently treated as HTML tags, and changed browser page titles to use
  plain text rather than Markdown serialization.
- Fixed LaTeX output for highlighted inline code in comparison-table captions.
- Removed older local workarounds that are no longer needed with Pandoc 3.x
  and its bundled syntax-highlighting CSS.
- Hardened dependency and generated-data setup so failed Pandoc, Python,
  reference, and annex downloads do not leave partial targets behind.

### May 2026

- Added interactive HTML controls for generated papers, including toggles for
  syntax highlighting and deleted wording.
- Added GitHub Pages deployment support and tooling for publishing side-by-side
  rendered test output.
- Expanded proposed-wording support with substitution syntax, written as
  `[old text](new text){.sub}`, and improved HTML rendering for insertions,
  deletions, and inline code.
- Continued expanding the rendering test document.

### April 2026

- Added paragraph-level stable-reference links such as `[stable.name#1]{.sref}`.
- Reworked embedded Markdown processing so code annotations are handled before
  syntax highlighting.
- Added `$...$` shorthand for italicized embedded Markdown in code, equivalent
  to `@_..._@`.
- Refactored code-element processing for better performance and cleaner
  rendering behavior.

## 2025

### June 2025

- Improved mobile rendering behavior for generated HTML.

### January 2025

- Extended embedded Markdown support beyond C++ and diff code to additional
  languages such as NASM and Rust.
- Added automatic cross-reference text for links to document sections, using
  empty links such as `[](#section-id)`.
- Added support for inserting referenced paper titles through citation syntax
  such as `[@P1240R2]{.title}`.
- Added initial project website content for GitHub Pages.
- Expanded user-facing documentation for references, examples, notes, embedded
  Markdown, and installation.

## 2024

### December 2024

- Extended stable-name references to support names without paragraph numbers,
  such as `[stable.name]{.sref}` and `[stable.name]{.unnumbered .sref}`.
- Added draft-note support with `::: draftnote` blocks and `.draftnote` spans.
- Made dependency tracking more extensible for projects with additional Python
  requirements.

### March 2024

- Changed citation rendering so paper references link directly to the cited
  documents.
- Improved bibliography and no-reference handling for generated output.

### February 2024

- Changed inline code defaults so C++ papers get C++ highlighting without
  additional markup.

## 2023

### November 2023

- Added MathJax support for generated papers.
- Split paper sources out of this repository into `mpark/wg21-papers`.
- Repositioned this repository as the reusable framework for writing WG21
  papers.

## 2022

### June 2022

- Upgraded the framework to a newer Pandoc baseline.

### April 2022

- Improved HTML generation and added convenience targets for building all HTML,
  LaTeX, or PDF outputs.

### February 2022

- Added licensing for the reusable framework portion of the repository.

## 2021

### October 2021

- Improved generated-document readability on mobile devices.

### July 2021

- Started work on the next pattern matching paper revision, `D1371R4`.

## 2020

### December 2020

- Reworked framework dependencies around a local Pandoc installation for more
  stable builds.
- Reorganized reference and bibliography data around CSL JSON.
- Updated templates and build support for newer Pandoc behavior.

### October 2020

- Added published `P1371R2` and `P1371R3` artifacts.

### September 2020

- Finalized `P1371R3` with major design updates for pattern matching and
  `inspect`.

### August 2020

- Added `D2211R0`, "Exhaustiveness Checking for Pattern Matching".
- Continued design work on expression-only `inspect` and pattern matching
  examples.

### July 2020

- Added a new `P1371R3` revision.

### May 2020

- Improved generated HTML metadata.

### February 2020

- Improved generated-output dependency handling.

### January 2020

- Created and finalized `P1371R2`, including major updates to pattern syntax,
  `let` behavior, and `inspect` semantics.
- Added stable-name reference support.
- Added nested embedded Markdown for code blocks and inline code.
- Moved the build system to Pandoc defaults files and made source, output,
  dependency, bibliography, and highlighting behavior more configurable.
- Renamed Tony Table support to comparison-table support, using
  `::: cmptable` blocks.
- Added audience rendering to generated title headers.

## 2019

### October 2019

- Improved generated-output setup and documented additional platform
  requirements.

### September 2019

- Documented Unicode support for code blocks.

### June 2019

- Expanded the framework into a richer WG21 paper generator with HTML, LaTeX,
  citations, references, syntax highlighting, paragraph numbers, and Makefile
  integration.
- Added automatic reference linking and stable-reference date support.
- Added embedded Markdown parsing inside code blocks and inline code.
- Added custom C++ syntax highlighting and WG21-themed highlighting output.
- Added comparison-table support with `::: cmptable` blocks and early rendering
  tests.
- Finalized `P1371R1` after substantial pattern matching design work.

### May 2019

- Added automatic reference-link support.
- Added paragraph-number markup and C++ draft-inspired HTML styling.
- Expanded formatting documentation.
- Forked pattern matching work toward `P1371R1`.

### April 2019

- Restructured generation around a `generated` output directory.
- Added LaTeX build support and updated Pandoc templates.
- Added reusable paper markup for examples, notes, editorial notes, strikeout,
  underline, and local metadata overrides, using classes such as `.example`,
  `.note`, and `.ednote`.

### March 2019

- Added documentation and examples for papers generated with the framework.

### February 2019

- Added `D1469R1` with wording.

### January 2019

- Added `P1469R0`.
- Developed and finalized `P1371R0`, including design discussion,
  expression-pattern disambiguation, refutability, wildcard syntax, and
  examples.
- Migrated paper sources back to Markdown and added early HTML-generation
  support.
- Added support for richer paper metadata such as multiple audiences and email
  addresses.

## 2018

### December 2018

- Continued refining pattern matching examples and syntax.

### November 2018

- Heavily revised `D1260R1` with major pattern matching features including
  binding patterns, expression `inspect`, dereference patterns, designated
  extractors, expression-pattern pinning, and polymorphic handling.
- Added San Diego meeting material for pattern matching.
- Added Tony Table support and label-based citations.
- Added document-diff markup for additions and removals, using `.add` and `.rm`
  classes.
- Renamed the pattern matching draft to `D1371R0`.

### October 2018

- Developed pattern matching into `P1260R0` and started `D1260R1`.
- Added support for intermediate LaTeX generation.
- Improved paragraph-number handling.

### August 2018

- Published `P0655R1`.

### July 2018

- Added and finalized `D0655R1`.
- Continued early pattern matching work.

### June 2018

- Began the repository's pattern matching paper work.

## 2017

### November 2017

- Replaced the shell-based PDF generation script with a Makefile.

### October 2017

- Added the first Markdown-based paper infrastructure.
- Converted `N3887` to Markdown.
- Started and developed `D0655R0`, later renamed to `P0655R0`.
- Added early framework support for syntax highlighting and proposed wording
  diffs.
- Moved generated PDFs into a dedicated directory.

### June 2017

- Refreshed generated PDF artifacts.

## 2016

### March 2016

- Added revisioned `P0080R0` sources.
- Added the `N3887` PDF and unpublished `D0080R1` draft.

## 2015

### October 2015

- Refined `P0080` wording and examples for variant-related behavior.

### September 2015

- Added and finalized the initial `P0080R0` paper submission.

### May 2015

- Updated repository metadata and documentation.

## 2014

### January 2014

- Created the repository.
- Added the "Consistent Metafunction Aliases" paper, later assigned paper
  number `N3887`.
