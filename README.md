# WG21: C++ Standards Committee Papers

## Status

- [P1371]: Pattern Matching
- [P1469]: Disallow `_` Usage in C++20 for Pattern Matching in C++23
- [P1260]: Pattern Matching - Requested to unify with [P1308R0]
- [P0655]: `visit<R>`: Explicit Return Type for `visit` - Accepted in C++20
- [D0080]: Tweaks to the Kona Variant - Encouraged to return with `P`-papers
- [P0080]: Variant: Discriminated Union with Value Semantics - Not presented
- [N3887]: Consistent Metafunction Aliases - Accepted in C++14

[P1371]: https://wg21.link/p1371
[P1469]: https://wg21.link/p1469
[P1308]: https://wg21.link/p1308
[P1260]: https://wg21.link/p1260
[P0655]: https://wg21.link/p0655
[D0080]: generated/D0080R1.pdf
[P0080]: https://wg21.link/p0080
[N3887]: https://wg21.link/n3887

## Formatting

Refer to [How I format my C++ papers][FMT] for an overview.

[FMT]: https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers

## Generation

Documents are generated in the `generated` directory by default, and
can be overridden by `OUTDIR=<outdir>`.

```bash
make <paper>.pdf               # `<paper>.md` -> `generated/<paper>.pdf`
make <paper>.pdf OUTDIR=pdf    # `<paper>.md` -> `pdf/<paper>.pdf`

make <paper>.html              # `<paper>.md` -> `generated/<paper>.html`
make <paper>.html OUTDIR=html  # `<paper>.md` -> `html/<paper>.html`
```

## Submodule

```bash
git submodule add https://github.com/mpark/wg21.git

make <paper>.pdf -f wg21/Makefile               # -> `generated/<paper>.pdf`
make <paper>.pdf -f wg21/Makefile OUTDIR=pdf    # -> `pdf/<paper>.pdf`

make <paper>.html -f wg21/Makefile              # -> `generated/<paper>.html`
make <paper>.html -f wg21/Makefile OUTDIR=html  # -> `html/<paper>.html`
```

## Examples

- [P1390]: Suggested Reflection TS NB Resolutions
- [P1361]: Integration of chrono with text formatting

[P1390]: https://wg21.link/p1390
[P1361]: https://wg21.link/p1361

## Requirements

  - `pdflatex`
  - `pandoc` (>= 2.7)
  - `pandoc-citeproc`
  - `python3`
  - `panflute`

### OS X

```bash
brew cask install mactex

brew install pandoc
brew install pandoc-citeproc

brew install python
pip3 install panflute
```
