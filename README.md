# WG21: C++ Standards Committee Papers

- [P1260R0]: Pattern Matching - Targeted for C++23
- [P0655R1]: `visit<R>`: Explicit Return Type for `visit` - Accepted in C++20
- [D0080R1]: Tweaks to the Kona Variant
- [P0080R0]: Variant: Discriminated Union with Value Semantics - Not presented
- [N3887]: Consistent Metafunction Aliases - Accepted in C++14

[P1260R0]: https://wg21.link/P1260
[P0655R1]: https://wg21.link/P0655
[D0080R1]: pdf/D0080R1.pdf
[P0080R0]: https://wg21.link/P0080
[N3887]: https://wg21.link/N3887

## Framework

__TL;DR__: Written in [Pandoc Markdown], generated into PDF via [Pandoc].

[Pandoc Markdown]: https://pandoc.org/MANUAL.html#pandocs-markdown
[Pandoc]: https://pandoc.org/

## Generation

```bash
make <paper>.md    // Generates `github/<paper>.md` from `<paper>.pandoc`
make <paper>.pdf   // Generates `pdf/<paper>.pdf` from `<paper>.pandoc`
```

## Requirements

  - `pandoc 2`
  - `pandoc-citeproc`
  - `panflute`
  - `pdflatex`
  - `python3`
