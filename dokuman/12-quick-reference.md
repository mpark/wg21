# Quick reference

This file folds the whole guide into lookup tables. It lists every Markdown syntax form, every front matter key with its default, every make target, and every make variable with its default, and each row links to the section that explains it in full. After reading it you will be able to recall the exact spelling of any construct or setting, check its default, and jump straight to the explanation when you need the details, without paging back through the guide.

## Markdown syntax

The tables follow the order of the guide, one topic each. In the Syntax column, `text`, `code`, and `id` stand for your own content.

**Headings and links**

| Syntax | What it does | Explained in |
|---|---|---|
| `# Heading`, `## Heading`, or a line underlined with `=` (level 1) or `-` (level 2) | Section heading, numbered automatically (1, 1.1, 1.1.1) and given a self-link | [Numbered and unnumbered headings](05-headings-and-formatting.md#numbered-and-unnumbered-headings) |
| `# Heading {-}`, `# Heading {.unnumbered}` | Heading without a section number, still listed in the table of contents | [Numbered and unnumbered headings](05-headings-and-formatting.md#numbered-and-unnumbered-headings) |
| `# Heading {- .unlisted}` | Unnumbered heading left out of the table of contents; `.unlisted` works only beside `-` or `.unnumbered` | [Headings left out of the table of contents](05-headings-and-formatting.md#headings-left-out-of-the-table-of-contents) |
| `## Heading {#id}` | Custom heading id that stays the same when you reword the heading | [Custom ids](05-headings-and-formatting.md#custom-ids) |
| `[Heading Text]`, `[Heading Text][]` | Link to a heading that shows the heading text | [Linking by heading text](05-headings-and-formatting.md#linking-by-heading-text) |
| `[text][Heading Text]`, `[text](#id)` | Link to a heading that shows your own text | [Linking by heading text](05-headings-and-formatting.md#linking-by-heading-text) |
| `[](#id)` | Link that fills in the target heading's current text (a framework extension) | [Links that fill in the heading text](05-headings-and-formatting.md#links-that-fill-in-the-heading-text) |
| `[text](#title-block-header)`, `[text](#toctitle)` | Link to the title block or the table of contents | [Fixed anchors](05-headings-and-formatting.md#fixed-anchors) |
| `[label]: https://...`, then `[label]` | Link target defined once and reused anywhere | [Other kinds of links](05-headings-and-formatting.md#other-kinds-of-links) |
| `<https://...>` | Clickable link that shows the URL itself | [Other kinds of links](05-headings-and-formatting.md#other-kinds-of-links) |

**Inline formatting, lists, and tables**

| Syntax | What it does | Explained in |
|---|---|---|
| `*text*`, `_text_` | Emphasis, in italics | [Emphasis and underline](05-headings-and-formatting.md#emphasis-and-underline) |
| `**text**`, `__text__` | Strong emphasis, in bold | [Emphasis and underline](05-headings-and-formatting.md#emphasis-and-underline) |
| `feas**ible**` | Emphasis on part of a word; only asterisks work inside a word | [Emphasis and underline](05-headings-and-formatting.md#emphasis-and-underline) |
| `[text]{.underline}` | Underline | [Emphasis and underline](05-headings-and-formatting.md#emphasis-and-underline) |
| `~~text~~` | Plain strikeout, not for wording changes | [Strikeout](05-headings-and-formatting.md#strikeout) |
| `2^10^` | Superscript | [Superscript and subscript](05-headings-and-formatting.md#superscript-and-subscript) |
| `` `constexpr`~opt~ `` | Subscript, as for an optional grammar element | [Superscript and subscript](05-headings-and-formatting.md#superscript-and-subscript) |
| `==text==`, `[text]{.mark}` | Highlight with a yellow background | [Highlighting](05-headings-and-formatting.md#highlighting) |
| `$\frac{a+b}{2}$` | Inline TeX math, typeset by LaTeX in PDF and shown as MathML in HTML | [Math](05-headings-and-formatting.md#math) |
| A line ending in `\` | Line break inside a paragraph | [Line breaks and quotes](05-headings-and-formatting.md#line-breaks-and-quotes) |
| `"text"`, `it's` | Straight quotes and apostrophes, printed as curly ones | [Line breaks and quotes](05-headings-and-formatting.md#line-breaks-and-quotes) |
| `<table>` and other raw HTML | Passed through to HTML output | [Raw HTML](05-headings-and-formatting.md#raw-html) |
| `` `generator<T>` `` | C++ with angle brackets, kept in backticks so it is not read as an HTML tag | [Raw HTML](05-headings-and-formatting.md#raw-html) |
| `- item` lines with no blank lines between them | Compact bulleted list, with long-dash bullets | [Lists](05-headings-and-formatting.md#lists) |
| `- item` lines separated by blank lines | Loose list, spaced more widely | [Lists](05-headings-and-formatting.md#lists) |
| A block indented two spaces under a `-` bullet | Code block, extra paragraph, or note inside the list item | [Lists](05-headings-and-formatting.md#lists) |
| `\| A \| B \|` rows with a `\| --- \| --- \|` separator | Pipe table; dash lengths set relative column widths | [Pipe tables](05-headings-and-formatting.md#pipe-tables) |
| `+---+` border lines with a `+===+` rule under the header | Grid table; cells can hold wording-change markup | [Grid tables](05-headings-and-formatting.md#grid-tables) |

**Code**

| Syntax | What it does | Explained in |
|---|---|---|
| `` `code` `` | Inline code, highlighted as C++ by default | [Inline code](06-code.md#inline-code) |
| `` `code`{.rust} `` | Inline code highlighted as another language | [Inline code](06-code.md#inline-code) |
| `` `code`{.default} `` | Inline code with no highlighting; also the way to show Markdown syntax literally | [Inline code](06-code.md#inline-code) |
| `` `3WAY`{.default}`<R>`{.cpp} `` | Code spans in different languages joined into one expression | [Combining inline code with other formatting](06-code.md#combining-inline-code-with-other-formatting) |
| ```` ``` ```` | Code block in a shaded box, not highlighted by default | [Code blocks](06-code.md#code-blocks) |
| ```` ```cpp ````, ```` ```rust ```` | Code block highlighted in the named language | [Code blocks](06-code.md#code-blocks) |
| ```` ```cpp {.numberLines startFrom=8} ```` | Numbered lines; `startFrom` sets the first number | [Line numbers](06-code.md#line-numbers) |
| ```` ```cpp {.not_proposed} ```` | Code marked as a design the paper does not propose, labeled "⊘ Not proposed" | [Code that is not proposed](06-code.md#code-that-is-not-proposed) |
| ```` ```mermaid ```` | Passed through as source text; no diagram is drawn | [Diagrams and other blocks](06-code.md#diagrams-and-other-blocks) |

**Embedded Markdown in code**

| Syntax | What it does | Explained in |
|---|---|---|
| `@...@` inside code | Parses the text between the delimiters as Markdown; on by default for `cpp`, `default`, and `diff` code, and must open and close on one line | [Embedded Markdown in code](06-code.md#embedded-markdown-in-code) |
| `@*text*@`, `$text$` | Italic term or placeholder inside code, such as `$unspecified$` | [Italic terms and placeholders](06-code.md#italic-terms-and-placeholders) |
| `$~i~$`, `$pp-tokens~opt~$` | Italic subscripted index, or italic name with an "opt" subscript | [Italic terms and placeholders](06-code.md#italic-terms-and-placeholders) |
| `@$...$@` | Typeset math inside code | [Math and highlighting inside code](06-code.md#math-and-highlighting-inside-code) |
| `@==text==@` | Yellow highlight on one part of the code | [Math and highlighting inside code](06-code.md#math-and-highlighting-inside-code) |
| `@[text]{.add}@`, `@[text]{.rm}@`, `@[old](new){.sub}@` | Added, removed, or substituted tokens inside code | [Marking tokens as added or removed](06-code.md#marking-tokens-as-added-or-removed) |
| `` @[`code`]{.add}@ `` | Change whose contents stay code, keeping C++ symbols literal while `$text$` still italicizes | [Keeping C++ symbols literal inside a change](06-code.md#keeping-c-symbols-literal-inside-a-change) |
| `\*` and an escaped space `\ ` inside `@...@` | Literal Markdown character; kept trailing space | [Keeping C++ symbols literal inside a change](06-code.md#keeping-c-symbols-literal-inside-a-change) |
| `@@...@@` | Fragment that itself contains the single `@` delimiter | [Keeping C++ symbols literal inside a change](06-code.md#keeping-c-symbols-literal-inside-a-change) |
| `// @[format.functions]{.sref}@` | Explicit stable name inside a code comment | [Stable names in code comments](06-code.md#stable-names-in-code-comments) |
| `{.raw}` | Turns embedded Markdown off for one element, so `@` and `$` print as typed; short for `md=none em=none` | [Turning embedded Markdown off](06-code.md#turning-embedded-markdown-off) |
| `{.embed_md}` | Turns embedded Markdown on for code in another language; short for `md=@ em=$` | [Turning embedded Markdown on for other languages](06-code.md#turning-embedded-markdown-on-for-other-languages) |
| `md=<symbol>`, `md=none` | Changes or disables the `@` delimiter on one element | [Changing the delimiters](06-code.md#changing-the-delimiters) |
| `em=<symbol>`, `em=none` | Changes or disables the `$` italics delimiter on one element | [Changing the delimiters](06-code.md#changing-the-delimiters) |

**Wording changes**

| Syntax | What it does | Explained in |
|---|---|---|
| `[text]{.add}` | Inline addition: green underline in PDF, underlined inserted text in HTML | [Inline additions and removals](07-wording.md#inline-additions-and-removals) |
| `[text]{.rm}` | Inline removal: red strikeout in PDF, struck-out text in HTML that readers can hide | [Inline additions and removals](07-wording.md#inline-additions-and-removals) |
| `[old](new){.sub}` | Substitution: old text struck out, new text inserted right after it with no space | [Substitutions](07-wording.md#substitutions) |
| `::: add` ... `:::` | Block of added wording, colored green in PDF without underline | [Blocks of added or removed wording](07-wording.md#blocks-of-added-or-removed-wording) |
| `::: rm` ... `:::` | Block of removed wording, colored red in PDF without strikeout | [Blocks of added or removed wording](07-wording.md#blocks-of-added-or-removed-wording) |
| `>` on every line, around an instruction and its change div | Editing instruction and its wording quoted as one block | [Quoting an editing instruction with its wording](07-wording.md#quoting-an-editing-instruction-with-its-wording) |
| `_attribute-specifier-seq_`, `_Returns:_` | Grammar terms, library element descriptions, and defined terms in italics | [Wording conventions](07-wording.md#wording-conventions) |
| ```` ```diff ```` with `-`, `+`, and space line prefixes | Whole-line code change: removed lines red, added lines green, unchanged lines gray | [Code changes](07-wording.md#code-changes) |
| `` `code`{.diff} `` | Inline code with the same diff coloring | [Code changes](07-wording.md#code-changes) |

**Paragraph numbers**

| Syntax | What it does | Explained in |
|---|---|---|
| `::: wording` ... `:::` | Turns on automatic numbering of paragraphs, notes, and examples; every counter restarts in each block | [The wording block](07-wording.md#the-wording-block) |
| `[1]{.pnum}` | Paragraph number in the margin, written by hand; works anywhere | [Writing paragraph numbers by hand](07-wording.md#writing-paragraph-numbers-by-hand) |
| `[2.1]{.pnum}` | Sub-paragraph number, shown as (2.1) | [Writing paragraph numbers by hand](07-wording.md#writing-paragraph-numbers-by-hand) |
| `[x]{.pnum}` | Placeholder label for an inserted paragraph; the next paragraph keeps its number | [Writing paragraph numbers by hand](07-wording.md#writing-paragraph-numbers-by-hand) |
| `[#]{.pnum}` | Automatic paragraph number; inside `::: wording` only | [Automatic numbers inside wording](07-wording.md#automatic-numbers-inside-wording) |
| `[#.#]{.pnum}` | Automatic sub-paragraph number under the current paragraph | [Automatic numbers inside wording](07-wording.md#automatic-numbers-inside-wording) |
| `[2.#]{.pnum}`, `[4.2.5]{.pnum}` | Pinned parent with an automatic child; pinned three-level number | [Multi-level numbers](07-wording.md#multi-level-numbers) |
| `[2.x]{.pnum}`, `[x.#]{.pnum}`, `[#.x.#]{.pnum}` | Literal labels printed as written, leaving the numeric count alone | [Literal labels](07-wording.md#literal-labels) |
| `#.` list items inside `::: wording` | List-based paragraphs (experimental): automatic numbers, and the list itself disappears | [Automatic numbers from list markers](07-wording.md#automatic-numbers-from-list-markers) |
| `6.` | Pins the paragraph number, but only when it opens a new list | [Pinning a number](07-wording.md#pinning-a-number) |
| `[...]` | Elision paragraph; ends a list so the next numeric marker pins, and inside a list item stays unnumbered with a real ellipsis | [Pinning a number](07-wording.md#pinning-a-number) |
| Nested `-` bullets or numbered items under a list item | Sub-paragraphs such as (2.1); a nested `4.` that opens a new list under paragraph 2 gives (2.4) | [Sub-paragraphs from nested lists](07-wording.md#sub-paragraphs-from-nested-lists) |
| `x.`, `x)` | Paragraph labeled `x` that does not advance the count; bullets under an `x)` paragraph give (x.1) | [Inserting paragraphs with x. and x)](07-wording.md#inserting-paragraphs-with-x-and-x) |
| Text or a block indented under a list item | Unnumbered continuation paragraph or code block belonging to that paragraph | [Continuation paragraphs, elisions, and nested blocks](07-wording.md#continuation-paragraphs-elisions-and-nested-blocks) |
| `a.`, `i.`, `A.`, a nested `#.`, a top-level `-` list | Stay ordinary lists with no paragraph numbers | [Lists that stay lists](07-wording.md#lists-that-stay-lists) |

**Notes, examples, and grammar**

| Syntax | What it does | Explained in |
|---|---|---|
| `[text]{.example}`, `::: example` | Example, shown as `[ Example 1: ... end example ]` | [Examples](07-wording.md#examples) |
| `::: {.example num=5}`, `::: {.example .unnumbered}` | Pinned or unnumbered example inside `::: wording` | [Numbering examples](07-wording.md#numbering-examples) |
| `::: {#my-example .example}`, `::: {.example .add}` | Example with your own id for its HTML link; example shown as added | [Numbering examples](07-wording.md#numbering-examples) |
| `[text]{.note}`, `::: note` | Note, shown as `[ Note: ... end note ]` | [Notes](07-wording.md#notes) |
| `::: {.note num=3}`, `::: {#my-note .note}` | Pinned note number; note with your own id | [Numbering notes](07-wording.md#numbering-notes) |
| `[text]{.ednote}`, `::: ednote` | Editor's note in blue, shown as `[ Editor's note: ... ]` and never numbered | [Editorial notes](07-wording.md#editorial-notes) |
| `[text]{.draftnote}`, `::: draftnote` | Drafting note in blue, shown as `[ Drafting note: ... ]` and never numbered | [Drafting notes](07-wording.md#drafting-notes) |
| `[text]{.draftnote audience="the reader"}`, `::: {.draftnote audience=CWG}` | Drafting note addressed to an audience, such as `[ Drafting note for CWG: ... ]` | [Drafting notes](07-wording.md#drafting-notes) |
| `> \| _selection-statement:_` followed by indented `> \|` lines | Grammar production as a line block in a blockquote, with indentation kept | [Grammar](07-wording.md#grammar) |
| `_condition_`, `` `switch (` `` | Nonterminal in italics; terminal as C++-highlighted code | [The pieces of a production](07-wording.md#the-pieces-of-a-production) |
| `_init-statement~opt~_`, `` `if constexpr`_~opt~_ ``, `` `constexpr`~_opt_~ `` | Optional nonterminal; optional terminal, in either markup order | [The pieces of a production](07-wording.md#the-pieces-of-a-production) |
| A quoted line without `\|`; an empty `>` line | Continues one long alternative; separates productions in one block | [Longer grammar blocks](07-wording.md#longer-grammar-blocks) |
| `[...]{.add}` around an alternative, `> ::: add` around whole productions | New alternative, underlined; new productions, colored but not underlined | [Changing grammar](07-wording.md#changing-grammar) |
| ```` > ```cpp ```` inside a numbered paragraph | Grammar shown as a highlighted code block | [Grammar as a code block](07-wording.md#grammar-as-a-code-block) |

**Comparison tables**

| Syntax | What it does | Explained in |
|---|---|---|
| `::: cmptable`, then `### Before` and `### After`, each above a code block | Side-by-side comparison table; first-row headings label the columns | [A before and after table](08-comparison-tables.md#a-before-and-after-table) |
| `::: tonytable` | Older alias for `::: cmptable` | [A before and after table](08-comparison-tables.md#a-before-and-after-table) |
| `---` inside the table | Starts a new row; no rule is drawn | [More rows](08-comparison-tables.md#more-rows) |
| A third heading and code block in the first row | A third column | [More columns](08-comparison-tables.md#more-columns) |
| A first-row code block with no heading | Unlabeled column; with no headings at all, no header row | [Unlabeled columns](08-comparison-tables.md#unlabeled-columns) |
| `> caption` inside the table | Table caption; if there are several, the last one is used | [A caption](08-comparison-tables.md#a-caption) |
| `### Before {width=2}` | Relative column width; set it on every column or on none | [Column widths](08-comparison-tables.md#column-widths) |
| `::: {.cmptable .wide}` | Extra class kept on the table for your own styling | [Extra classes](08-comparison-tables.md#extra-classes) |

**Stable names and citations**

| Syntax | What it does | Explained in |
|---|---|---|
| `[basic.life]` | Implicit stable name: a link to that section of the working draft, brackets kept | [Stable names](09-stable-names-and-citations.md#stable-names) |
| `[over.match]: https://isocpp.org` | Sends a stable name's link somewhere else | [Overriding a stable-name link](09-stable-names-and-citations.md#overriding-a-stable-name-link) |
| `[basic.life]{.sref}` | Explicit stable name with section number and title, as in "6.8.4 Lifetime [basic.life]"; adding `.title` changes nothing | [Explicit stable names](09-stable-names-and-citations.md#explicit-stable-names) |
| `[basic.life]{- .sref}`, `[basic.life]{.unnumbered .sref}` | Explicit stable name without the section number | [Dropping the section number](09-stable-names-and-citations.md#dropping-the-section-number) |
| `[basic.life](){.sref}` | Bracketed link only, without the title, the same result as the implicit form | [Dropping the section number](09-stable-names-and-citations.md#dropping-the-section-number) |
| `## [basic.life]{.sref} {- .unlisted}` | Stable name as a heading; its id is the stable name | [Stable names as headings](09-stable-names-and-citations.md#stable-names-as-headings) |
| `[basic.life]/1`, `[basic.life]{.sref}/2.1` | Link to a paragraph or sub-paragraph | [Linking to a paragraph](09-stable-names-and-citations.md#linking-to-a-paragraph) |
| `[basic.life#1]{.sref}` | Older paragraph form, deprecated | [Linking to a paragraph](09-stable-names-and-citations.md#linking-to-a-paragraph) |
| `[@P1240R2]` | Citation: a bracketed label linking to the paper, plus a References entry | [Citing papers](09-stable-names-and-citations.md#citing-papers) |
| `[@N3887]`, `[@CWG1234]`, `[@LWG1234]`, `[@EDIT1234]`, `[@SD6]` | Citations of N papers, committee issues, editorial issues, and standing documents | [What you can cite](09-stable-names-and-citations.md#what-you-can-cite) |
| `[@P2300]` | Bare P number with no revision; it does not resolve and prints a warning | [Always cite a revision](09-stable-names-and-citations.md#always-cite-a-revision) |
| `[@P2996R8]{.title}` | Citation that also shows the paper's title | [Showing the paper's title](09-stable-names-and-citations.md#showing-the-papers-title) |
| `[@P2996R8, 1]` | Older locator form; shows the title and ignores the locator | [Showing the paper's title](09-stable-names-and-citations.md#showing-the-papers-title) |
| `references:` list with `id`, `citation-label`, `title`, `author` (`family`, `given`), and `URL` | Manual reference for a source outside the wg21.link index | [Manual references](09-stable-names-and-citations.md#manual-references) |

## Front matter keys

Front matter keys go in the YAML block at the top of the paper. Setting a key in one paper's front matter overrides the framework default for that paper. A list-valued key such as `geometry`, `classoption`, `header-includes`, or `embedded-md-code-classes` replaces the framework's list as a whole, so write out every entry you want to keep; see [How settings are layered](10-customization.md#how-settings-are-layered). In the Default column, "none" means the key is not set unless you set it. Dotted names such as `highlighting.inline-code` stand for nested YAML keys.

**Title block and document properties**

| Key | Default | What it does | Explained in |
|---|---|---|---|
| `title` | none; always set it | Title at the top of the paper, the browser tab title, and the PDF Title field; the whole title block appears only when it is set | [Title and subtitle](04-paper-metadata.md#title-and-subtitle) |
| `subtitle` | none | Subtitle under the title | [Title and subtitle](04-paper-metadata.md#title-and-subtitle) |
| `document` | none; always set it | Document # row; a `PnnnnRn` or `DnnnnRn` value adds [Latest] and [Status] links in HTML | [Document number](04-paper-metadata.md#document-number) |
| `date` | none | Date row, shown as written in `YYYY-MM-DD` form; `date: today` stamps the build date | [Date](04-paper-metadata.md#date) |
| `audience` | none; always set it | Audience row; a list prints one group per line | [Audience](04-paper-metadata.md#audience) |
| `author`, with `name` and `email` in each entry | none | Reply-to row; give every author an `email` | [Authors](04-paper-metadata.md#authors) |
| `revises` | none | Revises row between Audience and Reply-to | [Other front matter keys](04-paper-metadata.md#other-front-matter-keys) |
| `abstract` | none | Abstract between the title block and the table of contents (PDF only) | [Abstract and thanks](04-paper-metadata.md#abstract-and-thanks) |
| `thanks` | none | Footnote on the title (PDF only) | [Abstract and thanks](04-paper-metadata.md#abstract-and-thanks) |
| `keywords` | none | A list, printed as one comma-separated keywords meta tag in HTML; any PDF effect comes from Pandoc's built-in partials; unrelated to `highlighting.keywords` | [Other front matter keys](04-paper-metadata.md#other-front-matter-keys) |
| `description` | none | Page summary for search engines and link previews (HTML only) | [Other front matter keys](04-paper-metadata.md#other-front-matter-keys) |
| `subject`, `author-meta` | none | Standard Pandoc variables for PDF document properties; the framework's template does not use them, and any effect comes from Pandoc's built-in partials; see the [Pandoc manual](https://pandoc.org/MANUAL.html#metadata-variables) | [Other front matter keys](04-paper-metadata.md#other-front-matter-keys) |

**Table of contents, section numbers, and references**

| Key | Default | What it does | Explained in |
|---|---|---|---|
| `toc` | on | `toc: false` removes the table of contents, and in HTML every contents feature | [Table of contents](04-paper-metadata.md#table-of-contents) |
| `toc-depth` | `3` | Heading levels in the table of contents; for HTML, set it at the very top of the first file | [Table of contents](04-paper-metadata.md#table-of-contents) |
| `toc-title` | "Contents" | Table of contents heading (PDF only; the HTML heading always reads "Contents") | [Table of contents](04-paper-metadata.md#table-of-contents) |
| `toccolor` | black | Link color of table of contents entries (PDF only) | [Table of contents](04-paper-metadata.md#table-of-contents) |
| `lof`, `lot` | none | `true` adds a list of figures or a list of tables after the contents (PDF only) | [Table of contents](04-paper-metadata.md#table-of-contents) |
| `secnumdepth` | 5 when numbering is on | Heading levels that get numbers (PDF only) | [Numbered and unnumbered headings](05-headings-and-formatting.md#numbered-and-unnumbered-headings) |
| `reference-section-title` | "References" | Heading of the generated References section | [The References section](09-stable-names-and-citations.md#the-references-section) |
| `references` | none | Manual references, usually in a metadata block at the end of the paper | [Manual references](09-stable-names-and-citations.md#manual-references) |

**Code, stable names, and language**

| Key | Default | What it does | Explained in |
|---|---|---|---|
| `highlighting.inline-code` | `cpp` | Default language for inline code; `default` makes it plain | [Default language for code](10-customization.md#default-language-for-code) |
| `highlighting.code-block` | `default` | Default language for code blocks; `cpp` makes them C++ | [Default language for code](10-customization.md#default-language-for-code) |
| `highlighting.keywords.cpp` | none | Extra C++ keywords, as a list or a single value; other languages are ignored | [Extra C++ keywords](10-customization.md#extra-c-keywords) |
| `embedded-md-code-classes` | `cpp`, `default`, `diff` | Code classes that get embedded Markdown; your list replaces the default | [Which code gets embedded Markdown](10-customization.md#which-code-gets-embedded-markdown) |
| `number-srefs` | `true` | `false` drops the section number from every explicit stable name | [Section numbers on stable names](10-customization.md#section-numbers-on-stable-names) |
| `lang` | `en` | Document language: the HTML language attribute, PDF hyphenation, and babel | [Language and text direction](10-customization.md#language-and-text-direction) |
| `dir` | none | Text direction, written onto the HTML page's root element; for PDF, a standard Pandoc LaTeX variable (passes through); see the [Pandoc manual](https://pandoc.org/MANUAL.html#variables-for-latex) | [Language and text direction](10-customization.md#language-and-text-direction) |
| `babeloptions`, `shorthands`, `babelfonts` | see the Pandoc manual | Standard Pandoc LaTeX variables (pass through; PDF only); see the [Pandoc manual](https://pandoc.org/MANUAL.html#variables-for-latex) | [Language and text direction](10-customization.md#language-and-text-direction) |

**Page layout and colors**

| Key | Default | What it does | Explained in |
|---|---|---|---|
| `papersize` | A4 | Paper size, written bare, such as `letter` (PDF only) | [Page layout](10-customization.md#page-layout) |
| `fontsize` | 10pt | Base font size (PDF only) | [Page layout](10-customization.md#page-layout) |
| `geometry` | `left=2.245cm`, `right=2.245cm`, `top=2.5cm`, `bottom=2.5cm` | Page margins; your list replaces all four (PDF only) | [Page layout](10-customization.md#page-layout) |
| `classoption` | `oneside`, `final` | Extra LaTeX document class options; your list replaces both (PDF only) | [Page layout](10-customization.md#page-layout) |
| `documentclass` | `article` (Pandoc's default) | LaTeX document class (PDF only) | [Page layout](10-customization.md#page-layout) |
| `linestretch` | none | Body line spacing, such as `1.25` (PDF only) | [Page layout](10-customization.md#page-layout) |
| `beamerarticle` | none | `true` loads the beamerarticle package first (PDF only) | [Page layout](10-customization.md#page-layout) |
| `indent`, `pagestyle` | see the Pandoc manual | Standard Pandoc LaTeX variables (pass through; PDF only); see the [Pandoc manual](https://pandoc.org/MANUAL.html#variables-for-latex) | [Page layout](10-customization.md#page-layout) |
| `linkcolor`, `citecolor`, `urlcolor` | blue | Colors of internal links, citations, and URLs (PDF only) | [Link colors](10-customization.md#link-colors) |
| `filecolor`, `colorlinks`, `boxlinks` | see the Pandoc manual | Standard Pandoc LaTeX variables (pass through; PDF only); see the [Pandoc manual](https://pandoc.org/MANUAL.html#variables-for-latex) | [Link colors](10-customization.md#link-colors) |
| `addcolor` | `'006e28'` | Color of added text and added `diff` lines (PDF only) | [Colors for changed wording](10-customization.md#colors-for-changed-wording) |
| `rmcolor` | `'bf0303'` | Color of removed text and removed `diff` lines (PDF only) | [Colors for changed wording](10-customization.md#colors-for-changed-wording) |
| `uccolor` | `'898887'` | Color of unchanged `diff` lines (PDF only) | [Colors for changed wording](10-customization.md#colors-for-changed-wording) |

**Fonts**

| Key | Default | What it does | Explained in |
|---|---|---|---|
| `monofont` | none (Latin Modern family) | Font for code in the PDF, such as `"DejaVu Sans Mono"`, the usual choice for Unicode characters in code; HTML output is not affected | [Unicode fonts](10-customization.md#unicode-fonts) |
| `mainfont`, `mainfontoptions`, `sansfont`, `sansfontoptions`, `mathfont`, `mathfontoptions`, `mathspec`, `fontfamily`, `fontfamilyoptions`, `fontfamilies`, `CJKmainfont`, `CJKsansfont`, `CJKmonofont`, `CJKoptions`, `microtypeoptions`, `zero-width-non-joiner`, `fontenc`, `mainfontfallback`, `sansfontfallback`, `monofontfallback`, `luatexjapresetoptions`, `luatexjafontspecoptions` | see the Pandoc manual | Standard Pandoc LaTeX variables (pass through); see the [Pandoc manual](https://pandoc.org/MANUAL.html#variables-for-latex) | [Unicode fonts](10-customization.md#unicode-fonts) |

**Extra content and other PDF options**

| Key | Default | What it does | Explained in |
|---|---|---|---|
| `header-includes` | framework LaTeX preamble | Raw content for the HTML head and the PDF preamble; yours replaces the preamble that PDF features rely on, so copy its lines into yours | [Extra content in the head and body](10-customization.md#extra-content-in-the-head-and-body) |
| `include-before`, `include-after` | none | Raw content before or after the paper body; the exact spot differs between HTML and PDF | [Extra content in the head and body](10-customization.md#extra-content-in-the-head-and-body) |
| `pdf-trailer-id` | none | Pins the PDF trailer ID, for reproducible PDF builds; the value goes as-is inside the trailer ID's brackets, so check the Pandoc manual for its format (PDF only) | [Other PDF options](10-customization.md#other-pdf-options) |
| `biblio-title` | none | Read only by the template's natbib and biblatex branches, which stay inactive in the default build because it formats citations with `citeproc` | [Other PDF options](10-customization.md#other-pdf-options) |
| `links-as-notes`, `urlstyle`, `pdfstandard`, `hyperrefoptions`, `csquotes`, `csquotesoptions`, `biblio-style`, `natbiboptions`, `biblatexoptions` | see the Pandoc manual | Standard Pandoc LaTeX variables (pass through; PDF only); see the [Pandoc manual](https://pandoc.org/MANUAL.html#variables-for-latex) | [Other PDF options](10-customization.md#other-pdf-options) |

Pandoc-level settings go in your own defaults file rather than in front matter: `number-sections`, `table-of-contents`, `template`, `csl`, `bibliography`, `pdf-engine`, `css`, `filters`, `resource-path`, `id-prefix`, and `html-math-method`. See [Your own defaults file](10-customization.md#your-own-defaults-file).

## Make targets

Run each target as `make <target>`. They work in both layouts; in the flat layout outputs land in `generated/`, and in the per-paper layout they land next to the source.

| Target | What it does | Explained in |
|---|---|---|
| `<paper>.html` | Builds one paper as a single self-contained HTML page | [Building one paper](03-building.md#building-one-paper) |
| `<paper>.pdf` | Builds one paper as PDF through `xelatex` | [Building one paper](03-building.md#building-one-paper) |
| `<paper>.latex` | Builds one paper as LaTeX source; the extension is `.latex`, not `.tex` | [Building one paper](03-building.md#building-one-paper) |
| `generated/<paper>.pdf` | Builds one paper by its full output path | [Building one paper](03-building.md#building-one-paper) |
| `all` (bare `make`) | Builds every paper in `DEFAULT_FORMAT` | [Building every paper](03-building.md#building-every-paper) |
| `html` | Builds every paper as HTML | [Building every paper](03-building.md#building-every-paper) |
| `pdf` | Builds every paper as PDF | [Building every paper](03-building.md#building-every-paper) |
| `latex` | Builds every paper as LaTeX source | [Building every paper](03-building.md#building-every-paper) |
| `clean` | Deletes the built outputs of the current papers; exactly what it removes depends on the layout | [Cleaning up](03-building.md#cleaning-up) |
| `distclean` | Deletes the downloaded Pandoc, the Python environment, and the generated citation and stable-name data, for every paper in the repository | [Cleaning up](03-building.md#cleaning-up) |
| `update` | Refreshes the citation and stable-name data from wg21.link and eel.is | [Refreshing citation and stable-name data](03-building.md#refreshing-citation-and-stable-name-data) |
| `serve` | Builds every paper in the default format, then rebuilds on each save and serves the output directory at `http://127.0.0.1:8000` | [The live server](03-building.md#the-live-server) |
| `serve <target>` | The same for one target; HTML pages reload in the browser, and PDFs only rebuild | [The live server](03-building.md#the-live-server) |
| `-C <paper-dir>` before any target | Runs the target in a per-paper directory from the repository root, as in `make -C p0000 clean` | [Same-stem mode](02-project-layouts.md#same-stem-mode) |
| `check`, `expected`, `MANUAL.html`, `MANUAL.pdf`, `MANUAL.latex` | For framework contributors only: the framework's tests and its own User's Guide | [For framework contributors](11-output-and-troubleshooting.md#for-framework-contributors) |

## Make variables

Set make variables in your Makefile before the `include` line; assignments after it are too late. `OUTDIR`, `DEFAULT_FORMAT`, `DEFAULTS`, and `REQUIREMENTS` can also be overridden for one run from the command line or the environment, as described in [One-off overrides](03-building.md#one-off-overrides), and `SERVE_HOST` and `SERVE_PORT` can be passed on the command line.

| Variable | Default | What it does | Explained in |
|---|---|---|---|
| `OUTDIR` | `generated` (always `.` in the per-paper layout) | Flat-layout output directory; `.` writes outputs next to their sources | [Choosing the output directory](03-building.md#choosing-the-output-directory) |
| `DEFAULT_FORMAT` | `html` | What a bare `make` and a bare `make serve` build: `html`, `pdf`, or `latex`, lowercase | [Building every paper](03-building.md#building-every-paper) |
| `DEFAULTS` | empty; flat and same-stem directories pick up `defaults.yaml` | Your own Pandoc defaults file, applied after the framework's | [Your own defaults and packages](03-building.md#your-own-defaults-and-packages) |
| `REQUIREMENTS` | empty; flat and same-stem directories pick up `requirements.txt` | Extra pip requirements files for the build's Python environment | [Your own defaults and packages](03-building.md#your-own-defaults-and-packages) |
| `SERVE_HOST` | `127.0.0.1` | Preview server host; `0.0.0.0` makes the preview reachable from other devices | [The live server](03-building.md#the-live-server) |
| `SERVE_PORT` | `8000` | Preview server port | [The live server](03-building.md#the-live-server) |
| `WATCHDEPS` | unset; the framework appends its own list | Extra files for `make serve` to watch | [The live server](03-building.md#the-live-server) |
| `PAPER_RULE` | unset | Per-paper mapping in the form `<paper-id>:<source-stem>`, such as `p2996r13:reflection` | [Mapping a source file to a paper number](02-project-layouts.md#mapping-a-source-file-to-a-paper-number) |
| `DEPS` | set by the framework | Public list of the framework files every paper build depends on, apart from the paper's own Markdown, for your own rules | [Rules of your own](02-project-layouts.md#rules-of-your-own) |
| `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, `PIP_CERT` | none | Exported from `local.mk` to point the build's downloads at an organization's CA certificate bundle | [Sharing and local settings](02-project-layouts.md#sharing-and-local-settings) |

Previous: [Output and troubleshooting](11-output-and-troubleshooting.md) | Back to the start: [MPark/WG21 User Guide](README.md)

*2026-09-25 - claude-opus-5.5*
