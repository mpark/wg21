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
[D0080]: pdf/D0080R1.pdf
[P0080]: https://wg21.link/p0080
[N3887]: https://wg21.link/n3887

## Formatting

Refer to [How I format my C++ papers][FMT] for an overview.

[FMT]: https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers

## Generation

```bash
make <paper>.pdf  // Generates `pdf/<paper>.pdf` from `<paper>.md`
make <paper>.html  // Generates `html/<paper>.html` from `<paper>.md`
```

## Examples

- [P1390]: Suggested Reflection TS NB Resolutions
- [P1361]: Integration of chrono with text formatting

[P1390]: https://wg21.link/p1390
[P1361]: https://wg21.link/p1361

## Requirements

  - `pdflatex`
  - `pandoc`
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
