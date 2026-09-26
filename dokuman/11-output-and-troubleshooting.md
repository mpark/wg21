# Output and troubleshooting

You write one Markdown file, but your readers see a PDF or an HTML page, and the two are not identical. This file describes exactly what each reader gets, lines the two formats up side by side, and then lists every warning and error the build can print, with its cause and fix. After reading it you will know what to expect from each output and how to get past anything the build complains about.

## What PDF readers get

### The first page

PDF output opens with a WG21-style header on page one: the title centered in large type, followed by a right-aligned two-column table of paper facts (Document #, Date, Project, Audience, an optional Revises row, and Reply-to), instead of Pandoc's stock LaTeX title. The abstract, if you set one, follows the header, then the table of contents under its "Contents" heading. Table of contents entries print in black by default, while links in the body are blue.

### Structure and navigation

- Sections are numbered 1, 1.1, 1.1.1, and so on, and level-4 and level-5 headings print on their own line rather than running into the following paragraph.
- Every PDF has a bookmark outline, the viewer's sidebar of headings.
- The PDF includes document metadata and working link targets for the title and the table of contents. Its Title field is the paper's title, and its Creator field reads "mpark/wg21" instead of Pandoc's default.
- Internal links, citations, and URLs are blue. Citations of wg21.link documents link straight to the paper.

### Page and type

The page is A4 with the C++ working draft's margins, the base font size is 10pt, and the fonts are the default Latin Modern family unless you choose others. Paragraphs are block style, with no first-line indent and space between paragraphs. Block quotes are indented by a narrow 0.2 inch instead of LaTeX's wider default. Bullet lists are marked with long dashes at every nesting level, matching the working draft's style. Bibliography entries that use an indented block are rendered on a new line with a hanging indent. Math is typeset by LaTeX, with amsmath and amssymb always available.

### Wording and code

- Paragraph numbers from `[1]{.pnum}` markup are placed in the left margin in small raised type, as in the C++ working draft.
- Inline additions are green and underlined, inline removals red and struck out, and whole `::: add` and `::: rm` blocks are colored green or red without underline or strikeout.
- `*emphasis*` stays italic while added and removed text still get underline and strikeout, including inside highlighted code blocks, and `.add` and `.rm` spans keep working inside highlighted code blocks.
- Code blocks marked `.not_proposed` print as a callout with a purple left bar, a pale lavender background, and a "⊘ Not proposed" label.
- Inline code works inside strikeouts, underlines, and `[...]{.mark}` highlights, and inline code in table captions, including comparison table captions written as block quotes, does not break the build.
- Long comparison tables break across pages, with the column headers such as Before and After repeated at the top of each page.
- In embedded-Markdown or keyword-highlighted code, spacing after `<`, `>`, `~`, `\`, `|`, and `'` is correct, so text like `template<class` renders without a stray space.

### PDF limitations

- Avoid nesting strikeout, underline, and highlight inside one another, because those constructs do not nest in PDF and the result is broken.
- Embedded Markdown and custom keywords are not applied to inline code inside section headings, so `@...@` there is not expanded; HTML output does process it. Inline code in a heading is plain monospace without highlighting, and the PDF bookmark drops the code formatting.
- With the usual `name:` and `email:` authors, the PDF's Author property stays empty; see `author-meta:` under [Other front matter keys](04-paper-metadata.md#other-front-matter-keys).

## What HTML readers get

### A single self-contained file

Each HTML paper is a single standalone file. Its stylesheets, scripts, and images such as the favicon are embedded in the `.html`, so it renders correctly when emailed, uploaded to the mailing, or opened offline with no companion files.

HTML papers are styled like the C++ standard draft with no setup, through three stylesheets applied in a fixed order: standard-wording styles, then WG21 paper styles, then table-of-contents styles. Every paper includes a browser-tab favicon embedded in the page. The page head marks every page with an "mpark/wg21" generator tag, which identifies papers built with this framework, and a machine-readable `dcterms.date` meta tag from the `date:` value. An author meta tag appears only when plain-text author metadata can be derived, so papers with the usual structured `name:` and `email:` authors have none. Pages read comfortably on phones and tablets: they declare a device-width viewport and still allow pinch zoom.

The browser tab shows the paper's title, converted back to Markdown text so inline code keeps its backticks. The Document # row adds [Latest] and [Status] links when the document number has the expected form. Math written as `$...$` is rendered as native MathML by default, with no MathJax script to load. Every table is wrapped in a container with the class `table-wrapper`. Every line of a code block has its own linkable anchor, and every margin paragraph number is a self-link whose target paragraph is highlighted when a reader follows a link to it. Editorial and drafting notes are blue in the light theme and a lighter blue in the dark theme.

### The table of contents

The HTML table of contents is a "Contents" navigation panel placed before the paper body, holding the list of section headings. Its heading always reads "Contents"; `toc-title:` has no effect on it. On wide screens it sits as a sidebar:

- A reading-progress bar at the top fills from left to right as the reader scrolls. It shows empty when the page is too short to scroll.
- An "Expand"/"Collapse" button expands or collapses all nested entries, and its label flips to match the current state. Papers with only top-level sections show no button, because it is hidden when the outline has no nested sections.
- On a large enough screen the complete outline is shown automatically when it fits in the sidebar without an inner scrollbar, and a collapsed outline otherwise, and this default is re-checked as the window is resized. A reader who clicks Expand or Collapse keeps that choice for the rest of the visit, overriding the automatic default even across window resizes, but the choice is not saved across reloads. After the outline is expanded or collapsed, the highlighted entry is scrolled back into view.
- The entry for the section currently at the top of the screen is highlighted, and the highlight moves as the reader scrolls; the first entry stays highlighted until the reader scrolls past the first heading. After a reader jumps to a section through a link, the highlight lands on that same section. Every parent entry above the highlighted one is marked as part of the active path, and in the collapsed outline only the current chapter's subsections unfold while the rest stay folded. The sidebar scrolls itself just enough to keep the highlighted entry visible below its header.

On narrower screens (below 90em wide), the paper shows a fixed top bar with the paper title, the view controls, and a "Contents" button that opens the table of contents in a modal dialog with a close button. The page switches live between the fixed sidebar and the compact top bar as the window is resized. The dialog behaves like this:

- Opening it lands on the reader's current position, with the current section highlighted and scrolled to the middle of the list.
- Readers can dismiss it with its close button, by tapping the dimmed area outside it, or by pressing Escape. While it is open, the paper underneath does not scroll.
- Tapping an entry closes the dialog and jumps to that section, and the address bar is updated to the section link as a new history entry.
- Widening the window or rotating a device into the sidebar layout while the dialog is open closes it automatically.
- On older browsers without native modal dialog support, the dialog still opens and closes.

A few behaviors keep this robust. Section highlighting stays accurate in papers with images, math, or diagrams that shift the layout after the page first appears, because positions are re-measured once everything has loaded. Highlight and progress updates are batched to at most once per screen refresh, so scrolling long papers stays smooth. Screen-reader users can tell which section is current and whether the outline or the small-screen menu is expanded, because the controls and entries expose accessibility state that stays in sync with what is shown. Highlighting and small-screen jumps work for sections whose anchors contain special or non-ASCII characters.

With `toc: false`, the paper has none of this: no sidebar, top bar, dialog, or contents script. A paper whose contents list has no links to real headings likewise gets no interactive contents behavior, and any contents list present stays a plain static list. The small-screen top bar, the dialog, and the folded-outline styling turn on only when the page contains every part of the small-screen table of contents.

### View controls

Every HTML paper gives its readers an on-page view controls panel with three controls, with no opt-in needed from the author:

- A "Theme" switcher with three buttons, "System" (◐), "Light" (☀), and "Dark" (☾), with "System" selected by default.
- A "No syntax highlighting" checkbox, which strips syntax colors from code while keeping added and removed text colors and comment styling, and leaves `diff` blocks alone.
- A "Hide deleted text" checkbox, which removes struck-out text so readers can read proposed wording as it would look after the change. It works on removals marked inline as `[old text]{.rm}` or through `[old text](new text){.sub}` substitutions, but not on block-level `::: rm` sections.

Where the panel appears depends on the table of contents. Without one (`toc: false`), it is a sticky pill at the top right of the page. With one on wide screens, it is a fixed card above the sidebar contents. With one on narrower screens, it sits in the fixed top bar next to the "Contents" button. On phones and narrow windows, when the paper has a table of contents, the controls compact themselves: theme buttons show icons only, the checkbox labels shorten to "No highlight" and "Hide deleted", and an active checkbox is visibly highlighted in the top bar.

Keyboard and screen-reader users can operate the controls: each theme button has a spoken label and hover tooltip ("Use system theme", "Use light theme", "Use dark theme") and announces whether it is active, and each checkbox is a labeled form control. When readers print an HTML paper, the controls disappear from the printout and the page prints with light styling regardless of the on-screen theme.

### The theme switch

Dark mode turns on automatically when the reader's system prefers a dark color scheme. Choosing "System" makes the paper follow the operating system or browser dark-mode preference. Choosing "Light" keeps a light page even when the system is in dark mode, and choosing "Dark" gives the dark page regardless of system settings.

A manually chosen Light or Dark theme is remembered across visits in the browser's local storage, and it is reapplied to other papers from the same site. Choosing "System" clears the saved choice. When browser storage is unavailable, for example a paper opened as a local file in some browsers, the choice still applies to the current page. The saved theme is applied immediately as the page loads, avoiding a flash of the wrong color scheme, and the active theme button is marked as pressed.

The two checkboxes work differently from the theme: both start unchecked on every page load and are not remembered between visits.

## HTML and PDF side by side

Most constructs look the same in both formats. These are the places they differ, gathered from the files before this one:

| Feature | PDF | HTML |
|---|---|---|
| Title block | Right-aligned table on page one | Table under the centered title |
| [Latest] and [Status] links | None | After the document number |
| `abstract:` and `thanks:` | Shown | Dropped |
| `description:` | Ignored | Page summary in the head |
| `subject:` | Left to Pandoc's built-in LaTeX partials; see the Pandoc manual | Ignored |
| Table of contents | Contents pages plus bookmarks | Sidebar, or top bar and dialog |
| Contents heading | `toc-title:`, default "Contents" | Always "Contents" |
| Headings nested under an unlisted heading | Listed in contents | Left out of contents |
| Implicit stable names | No section number | Tooltip with number and title |
| Paragraph numbers | Small raised margin numbers | Margin self-links with target highlight |
| Change and diff colors | `addcolor`, `rmcolor`, `uccolor` | Framework stylesheet |
| Inline code in headings | Plain monospace | Highlighted |
| Math | Typeset by LaTeX | MathML |
| Reader controls | None | Theme, highlighting, hide deleted |
| Page, font, and link color keys | Apply | Ignored |
| `header-includes:` | LaTeX preamble | Raw HTML in the head |

The prose sections above, and the files they came from, explain each row.

## Warnings

Every diagnostic the framework prints while rendering a paper is a warning that starts with `[WARNING] mpark/wg21:`, appears in the terminal, and does not stop the build. Your output is still written; the warning tells you what in it is missing or ignored.

### Document number in an unrecognized format

````text
[WARNING] mpark/wg21: Document number '<document>' is an unrecognized format; expected "[PD]([0-9]+)R[0-9]+".
          This just means that [Latest] and [Status] links will be missing.
````

Cause: the `document:` value does not fit the P or D, digits, R, digits form. Effect: the HTML has no [Latest] and [Status] links; the PDF prints the value as written. Fix: write the number as `PnnnnRn` or `DnnnnRn`, for example `P2806R4`. See [Document number](04-paper-metadata.md#document-number).

### Stable name not found

````text
[WARNING] mpark/wg21: stable name <name> not found.
          Tip: run `make update` to refresh the local databases, including stable names
````

Cause: an explicit stable name is missing from the local stable-name data, either because the data is older than the draft or because the name is misspelled. Effect: the reference renders as just the bracketed link to eel.is, with no section number, title, or tooltip. Fix: run `make update`; if the warning remains, check the name against the draft. See [Explicit stable names](09-stable-names-and-citations.md#explicit-stable-names).

### Automatic paragraph number outside wording

````text
[WARNING] mpark/wg21: automatic paragraph number <num> ignored outside of ::: wording
````

Cause: a `#` in a paragraph number, such as `[#]{.pnum}`, outside a `::: wording` div. Effect: the `#` is not replaced with a number. Fix: wrap the wording in `::: wording`, or write the number explicitly. See [The wording block](07-wording.md#the-wording-block).

### No automatic text for a link

````text
[WARNING] mpark/wg21: cannot find automatic text for link to: #<anchor>
````

Cause: an empty link `[](#anchor)` points at something other than a heading, for example because of a mistyped id. Effect: the link is left with no text. Fix: point it at a real heading id, or give the link text. See [Referring to sections](05-headings-and-formatting.md#referring-to-sections).

### Content ignored in a comparison table

````text
[WARNING] mpark/wg21: <element type> <element text> in a comparison table is ignored
````

Causes: a heading placed after the first `---` of a comparison table; two headings before the same first-row code block (the earlier one is dropped); or any content other than headings, code blocks, block quotes, and `---` inside `::: cmptable`, such as paragraphs, lists, or nested divs. The element text is flattened onto one line. Effect: that element is dropped from the table. Fix: keep headings in the first row, one per code block, and move other content outside the div. See [Comparison tables](08-comparison-tables.md#warnings-from-comparison-tables).

### Comparison table widths

````text
[WARNING] mpark/wg21: cmptable widths must be specified for all columns or none.
          <table dump>

          Ignoring the specified widths and defaulting to even column widths.
````

`<table dump>` stands for a dump of the table's internal structure. Cause: `width` is set on some first-row headings but not all. Effect: the table falls back to equal widths. Fix: set `width` on every column or on none.

### Citation without a revision

````text
[WARNING] mpark/wg21: citation P2300 requires a revision. (e.g. `[@P2300R0]`)
````

Cause: an unresolved citation of a bare paper number, a key made of an uppercase `P` plus digits only. Every such citation gets its own warning line naming the paper number. Effect: the citation does not resolve. Fix: add the revision you mean; `R0` in the message is only an example. This is not a stale-data problem, so the build does not suggest `make update` for it. See [Citing papers](09-stable-names-and-citations.md#citing-papers).

### Missing citations

````text
[WARNING] mpark/wg21: missing citations may indicate a stale local paper index.
          Tip: run `make update` to refresh it
````

Cause: any other unresolved citation, such as `[@P9999R99]`. The tip is printed once per document no matter how many citations are unresolved. Fix: run `make update`; if the warning remains, check the key or add a manual reference. See [Missing citations](09-stable-names-and-citations.md#missing-citations).

### Messages from make and Python

Two more messages do not have the `[WARNING] mpark/wg21:` prefix and also leave the build running:

- A Makefile that includes the framework's `Makefile` instead of a layout file prints a deprecation warning on every make run, for example `wg21/Makefile:18: Makefile includes deprecated wg21/Makefile; include wg21/flat.mk or wg21/paper.mk instead. See https://mpark.github.io/wg21/MANUAL.html#project-layouts`. Fix: include `flat.mk` or `paper.mk` instead, as described in [Deprecated entry points](03-building.md#deprecated-entry-points).
- The HTML build reads `toc-depth` only from the metadata block at the very top of the first Markdown file, so a `toc-depth` in a block placed lower in the file is ignored. If the file does not begin with a metadata block at all, the HTML build also prints a Python error traceback in the terminal. Either way the build keeps going at the default depth. Fix: move `toc-depth` into the metadata block at the top of the first Markdown file. See [Table of contents](04-paper-metadata.md#table-of-contents).

## Errors

Build-system errors stop make. Here is each one, with its cause and fix.

### No Markdown input found

````text
No Markdown input found for target 'P2806r4.html'. Did you mean 'p2806r4.html'? (names are case-sensitive)
````

Cause: in a per-paper directory without `PAPER_RULE`, you asked make for a target that has no Markdown input, usually a typo in the paper name. The hint names the closest-matching `.md` file in the current directory, keeping any directory prefix and the extension you typed, and the case note appears only when the names differ in letter case alone. The flat layout and mapped per-paper directories never print this message; there, the same typo gives make's own `No rule to make target` error with no suggestion. When nothing is a close enough match, you get the bare `No Markdown input found for target '<target>'`. Fix: copy the suggestion back into `make`, or check that the paper file exists in the directory where you run `make`. See [When make cannot find your paper](03-building.md#when-make-cannot-find-your-paper).

### DEFAULT_FORMAT must be one of html, pdf, latex

````text
DEFAULT_FORMAT must be one of html, pdf, latex
````

Cause: a mistyped `DEFAULT_FORMAT` in the flat layout or a same-stem directory, such as `PDF` or `tex`. The check aborts every make run, including `make clean`, before anything is built. Fix: use exactly `html`, `pdf`, or `latex`, lowercase. In a mapped per-paper directory a bad value fails as an unknown make target instead of printing this message.

### Unsupported OS

````text
Unsupported OS: <name>.
````

Cause: the first build ran on an operating system other than Linux or macOS, such as a native Windows shell or a BSD; `<name>` is the output of `uname -s`. The build stops with exit code 1 before downloading. Fix: build on Linux or macOS, or on Windows under an environment that reports Linux, such as WSL. See [A note for Windows users](01-getting-started.md#a-note-for-windows-users).

### Other failures that stop the build

- Missing `title` or `document`: the framework reads both without a fallback, so leaving either out makes the filter stop with a Python error instead of a friendly warning, and the build fails. Fix: set both.
- An HTTP error while fetching the stable-name list fails the build, and a failed wg21.link fetch stops the build without overwriting an existing good bibliography. Fix: check your network access to eel.is and wg21.link (and, if your organization uses its own CA certificates, the CA bundle settings described in [Sharing and local settings](02-project-layouts.md#sharing-and-local-settings)), then run `make` again.
- A failed Pandoc download or Python environment install deletes its partial directory and stops the build. Fix: run `make` again; the next build retries from scratch.
- On macOS, a GNU tar placed ahead of the stock `tar` on PATH breaks the Pandoc install. Fix: make sure the stock macOS `tar` comes first for the build.
- On ARM Linux (aarch64), the build downloads the x86-64 Pandoc, which will not run natively.
- `make serve` stops with an error instead of starting the server when the first build fails. Fix: build the paper successfully first. Once the server is running, later failures print make's error but leave the server up.

## For framework contributors

If you work on the framework itself, run `make check` from inside a framework checkout (for example `make -C wg21 check`; bare `make` inside its `tests` directory does the same) to run the rendering, warning, option, and per-paper layout tests, which compare rendered HTML and LaTeX, not PDF, against checked-in expected files. After an intentional rendering change, `make expected` in `tests` overwrites those files so you can review and commit the diff. The User's Guide builds with `make MANUAL.html`, `make MANUAL.pdf`, or `make MANUAL.latex` into `generated/`, and its ```` ```render ```` blocks and `::: render` divs work only there, not in papers.

Previous: [Customization](10-customization.md) | Next: [Quick reference](12-quick-reference.md)

*2026-09-25 - claude-opus-5.5*
