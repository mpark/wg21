# Stable names and citations

WG21 papers constantly point at two things: sections of the working draft and other committee documents. The framework handles both for you. Write a stable name in brackets and it links to the draft; write a citation key and it links to the paper and lands in a References section you never have to write. After reading this file you will be able to link to any section or paragraph of the working draft, show its number and title automatically, cite papers, issues, and standing documents, add references of your own, and fix the warnings the build prints when a name or citation does not resolve.

## Stable names

Writing a working-draft stable name in plain square brackets, such as `[basic.life]`, makes it a link to `https://eel.is/c++draft/basic.life`, when that stable name exists. This is called an implicit stable name, and you do not define the link yourself:

````markdown
The object's lifetime has ended; see [basic.life].
````

The link text keeps its brackets, `[basic.life]`, in both formats. In HTML, hovering the link shows the section number and title as a tooltip, such as "6.8.4 Lifetime". In PDF no section number is shown.

This is typically how you quote standard wording with its original cross-references intact:

````markdown
> [...] whose lifetime has begun and has not ended ([basic.life]).
````

The quoted text keeps `[basic.life]` exactly where the standard has it, now as a working link.

### Which names link

Every stable-name reference links to its section at `https://eel.is/c++draft/<stable-name>`. Clauses, subclauses at any depth, and annexes can all be referenced, because every numbered heading in the draft has a stable-name entry; unnumbered draft headings are skipped. Section titles in stable-name references are clean and readable, with the draft's decorations stripped.

The list of names comes from the stable-name data downloaded on your first build, described in [What the first build does](01-getting-started.md#what-the-first-build-does). Stable-name references track the latest C++ working draft at eel.is/c++draft as of the day the data was fetched, not a published ISO standard such as C++20 or C++23, so numbers and titles match what the draft showed then. A name added to the draft after your last fetch needs `make update`, covered in [Refreshing citation and stable-name data](03-building.md#refreshing-citation-and-stable-name-data).

A name that does not exist is not linked. So square brackets used for other purposes, such as `[...]` elisions, do not turn into links. The flip side is that any bracketed word that exactly matches a stable name links even when it was not meant as a reference.

### Overriding a stable-name link

A Markdown reference-link definition with the same name overrides where a stable name links:

````markdown
Override [over.match] to something else.

[over.match]: https://isocpp.org
````

`[over.match]` now links to `https://isocpp.org` instead of eel.is. The link text then loses its brackets and reads "over.match", as with any reference link, in both formats.

### Showing the syntax literally

Stable-name syntax inside a plain inline code span stays literal and does not become a link, which is how to show `` `[basic.life]{.sref}` `` as source in a paper.

## Explicit stable names

Adding the `.sref` class to a bracketed span makes an explicit stable-name reference:

````markdown
Modify section [basic.life]{.sref}:
````

It renders the draft's leading section number and section title automatically, as in "6.8.4 Lifetime [basic.life]". The number and title are plain text and only the bracketed name is the link. This looks the same in PDF and HTML, and in HTML the link also has the hover tooltip.

Explicit stable names are bracketed spans, so other span classes can be combined with `.sref`. A typical use is an editing instruction such as `Modify section [basic.life]{.sref}:` or `Remove [expr.post.incr]{.sref}/2:`. An explicit stable-name reference always links to the online draft, even when the paper has its own heading for that stable name.

Choose the form by how the reference should read. Implicit `[basic.life]` shows only the bracketed name as a link, while explicit `[basic.life]{.sref}` also spells out the leading section number and title. Otherwise the two get the same treatment: the same link to the eel.is section, the same hover tooltip, and the same paragraph suffixes.

### Dropping the section number

Adding the `-` class drops the leading section number from one explicit stable name:

````markdown
[basic.life]{- .sref}
````

This gives "Lifetime [basic.life]". In HTML the hover tooltip still shows the number. `.unnumbered` is the long form of `-`, as in `[basic.life]{.unnumbered .sref}`.

The `-` form works for clauses and annexes too, and it works inside parentheses:

````markdown
[lex]{- .sref} and [depr]{- .sref}, as described in ([cpp.error]{- .sref}).
````

`[lex]{- .sref}` gives "Lexical conventions [lex]" and `[depr]{- .sref}` gives "Compatibility features [depr]".

To drop the numbers from every explicit stable name in a paper at once, use `number-srefs: false`, covered in [Section numbers on stable names](10-customization.md#section-numbers-on-stable-names).

Explicit stable-name references include the section title by default. Adding `.title` to a stable-name reference does nothing, so `{.sref .title}` renders exactly like `{.sref}`.

Putting `.sref` on a link instead of a span, for example `[basic.life](){.sref}`, gives only the bracketed `[basic.life]` link without the section title, the same result as the implicit form.

### Stable names as headings

An explicit stable name can serve as a section heading when replacing or updating a large body of standard wording:

````markdown
## [basic.life]{.sref} {- .unlisted}

## [intro.compliance.general]{.sref} {-}
````

The second heading renders as "4.1.1 General [intro.compliance.general]", and its table of contents entry shows the same text. The heading classes work as in [Headings and formatting](05-headings-and-formatting.md#numbered-and-unnumbered-headings): `-` removes the paper's own section number, and `.unlisted` also keeps the heading out of the table of contents.

A heading titled with a stable-name reference gets the stable name itself as its id, so `### [intro.compliance.general]{.sref} {-}` can be linked as `#intro.compliance.general`.

To use the paper's own heading numbering for a wording heading instead of the draft's, put an unnumbered explicit stable name in a normally numbered heading:

````markdown
## [basic.life]{- .sref}
````

The heading is numbered by the paper, followed by "Lifetime [basic.life]".

### When a stable name is not found

An explicit stable name missing from the local database prints this warning (an implicit one is simply left unlinked):

````text
[WARNING] mpark/wg21: stable name <name> not found.
Tip: run `make update` to refresh the local databases, including stable names
````

The reference then renders as just the bracketed link to eel.is, with no section number, title, or tooltip. Run `make update`, and if the warning persists, check the spelling against the draft.

## Linking to a paragraph

Appending `/pnum` to an implicit stable name links to a specific paragraph, where `pnum` is dot-separated integers such as `1` or `2.1`:

````markdown
Refer to a specific paragraph [basic.life]/1, or a sub-paragraph [basic.life]/2.1.
````

`[basic.life]/1` links to paragraph 1 and `[basic.life]/2.1` to paragraph 2.1, and the suffix becomes part of the link text. In HTML, the hover tooltip appends ", paragraph N", as in "6.8.4 Lifetime, paragraph 1".

The same suffix works right after a `.sref` span:

````markdown
Change [basic.life]{.sref}/2.1 as follows:
````

This renders as "6.8.4 Lifetime [basic.life]/2.1", with the suffix moved inside the link text. Punctuation after a paragraph suffix stays ordinary text, so `[expr.call]{.sref}/3.` keeps the trailing period outside the link.

The older form `[basic.scope.scope#2.1]{.sref}` still cites a paragraph but is deprecated. `[basic.life#1]{.sref}` displays as `[basic.life]/1`, and when the `#` form is used a following `/N` suffix is not absorbed and stays plain text. Prefer the `/pnum` suffix in new papers.

## Citing papers

A paper is cited in running text with `[@paper]`:

````markdown
This direction was suggested in [@P1240R2].
````

The citation shows as a bracketed label such as `[P1240R2]` and is a link, in both PDF and HTML. Cited documents are linked automatically, and the paper also gets an entry in the References section at the end. Citations are resolved automatically on every build, with no extra flag and no bibliography file of your own.

### What you can cite

Every kind of document the wg21.link index tracks can be cited, and no entry type is filtered out:

| Kind | Key form | Example |
|---|---|---|
| N paper | `Nxxxx` | `[@N3887]` |
| P paper, with revision | `PxxxxRn` | `[@P1371R1]` |
| Committee issue | `CWGxxxx`, `EWGxxxx`, `LWGxxxx`, `LEWGxxxx`, `FSxxxx` | `[@CWG1234]`, `[@LWG1234]` |
| Editorial issue (GitHub edit) | `EDITxxx` | `[@EDIT1234]` |
| Standing document | `SDx` | `[@SD6]` |

A key found in the index becomes a link to its wg21.link address, so `[@N3887]` links to `https://wg21.link/n3887` and lists "[N3887] Michael Park. 2013-12-26. Consistent Metafunction Aliases." in the References. Entries list every author, as in "[P1371R1] Sergei Murzin, Michael Park, David Sankel, Dan Sarginson." `[@SD6]` lists "[SD6] SG10 Feature Test Recommendations." References entries show the exact publication date (year, month, and day) when the index has one; in-text citations show no date.

Link or citation syntax inside a code span stays literal, which is how to show `` `[@N4762]`{.default} `` in a paper about citations.

### Always cite a revision

Cite P papers with a revision. An unresolved citation of a bare paper number such as `[@P2300]` prints:

````text
[WARNING] mpark/wg21: citation P2300 requires a revision. (e.g. `[@P2300R0]`)
````

This applies to keys made of an uppercase `P` plus digits only. To fix it, copy the example from the warning, which is the same paper number with `R0` appended, then change the `R` number to the revision you actually mean; `R0` is only an example, not the latest revision. Every revision-less paper citation in the paper gets its own warning line naming the paper number, so the build output lists all of them. A bare paper number does not resolve at all, and it is not counted as a missing citation, so the build does not suggest `make update` for it: the fix is to add a revision, not to refresh the data.

### Showing the paper's title

Adding the `.title` class to a citation includes the cited paper's title in the running text:

````markdown
This direction was suggested in [@P2996R8]{.title}.
````

`[@P2996R8]{.title}` renders as the single link `[P2996R8] (Reflection for C++26)`, in both formats, and the paper still gets a normal References entry. No setup is needed.

The `.title` span must hold exactly one bare citation, and `title` must be its only class. Forms like `[see @P1240R2]{.title}` or `[@P1240R2]{.title .note}` fall back to a plain citation without the title. Adding an `#id` or key=value attributes to the span does not stop it from working.

The older locator form gives the same title display: adding any locator to a citation, as in `[@P2996R8, 1]`, shows the title, and the locator value itself is ignored. For the same reason, do not put a page or section locator on a citation, such as `[@N4861, p. 5]`: the WG21 citation style shows the paper title in its place and never prints "p. 5".

## Where citation links go

A citation whose References entry has exactly one link jumps straight to that URL, so wg21.link citations take the reader directly to the cited paper, in both PDF and HTML. Only entries with zero or several links jump to their entry in the References section instead.

## The References section

A References section is appended at the end of the paper automatically. It lists every cited key alphabetically, each under its citation key in brackets, with author, date, title, and link:

````text
[N4762] Richard Smith. 2018-07-07. Working Draft, Standard for Programming Language C++. https://wg21.link/n4762
````

References are rendered in WG21 style. The generated bibliography sits under a "References" heading by default, and `reference-section-title:` in the front matter retitles it:

````yaml
reference-section-title: Bibliography
````

The References section is numbered like the other sections, for example appearing as "2 References" in the table of contents of a paper with one other top-level section. In PDF, the link at the end of each entry starts on its own indented line. Papers that cite nothing are handled cleanly by the bibliography generation.

### Manual references

References for sources outside the wg21.link index are added with a `references:` list in a YAML metadata block, opened and closed with `---` and typically placed at the bottom of the document:

````yaml
---
references:
  - id: PAT
    citation-label: Patterns
    title: "Pattern Matching in C++"
    author:
      - family: Park
        given: Michael
    URL: https://github.com/mpark/patterns
---
````

Each field has one job:

- `id` is the key you cite in text, so `- id: PAT` is cited as `[@PAT]`.
- `citation-label` controls the bracketed label shown in the bibliography, so `citation-label: Patterns` produces the entry `[Patterns]`. Typically `id` and `citation-label` are kept the same.
- `title` sets the reference's title.
- `author` lists its authors, each with `family` and `given` name fields.
- `URL` attaches its link.

With that block in place, `[@PAT]` in the text becomes a citation labeled `[Patterns]`, it links to the URL because the entry has exactly one link, and the References section lists it alongside the wg21.link entries. A manual reference without a `URL` has no link, so its citation jumps to its References entry instead.

## Missing citations

A citation that does not resolve, other than a bare P number, such as `[@P9999R99]`, prints one summary warning and the build continues:

````text
[WARNING] mpark/wg21: missing citations may indicate a stale local paper index.
Tip: run `make update` to refresh it
````

The stale-index tip is printed once per document, no matter how many citations are unresolved. In the output, an unresolved citation shows its key followed by a question mark, such as P9999R99?, instead of a linked label. The usual cause is a paper published after your last data fetch, so run `make update` to refresh the citation data, as described in [Refreshing citation and stable-name data](03-building.md#refreshing-citation-and-stable-name-data). If the warning persists, check the key for a typo, or add the document as a manual reference.

Previous: [Comparison tables](08-comparison-tables.md) | Next: [Customization](10-customization.md)

*2026-09-25 - claude-opus-5.5*
