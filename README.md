# WG21: C++ Standards Committee Papers

## Status

- [P1260R0]: Pattern Matching - Requested to unify with [P1308R0]
- [P0655R1]: `visit<R>`: Explicit Return Type for `visit` - Accepted in C++20
- [D0080R1]: Tweaks to the Kona Variant - Encouraged to return with `P`-papers
- [P0080R0]: Variant: Discriminated Union with Value Semantics - Not presented
- [N3887]: Consistent Metafunction Aliases - Accepted in C++14

[P1308R0]: https://wg21.link/P1308
[P1260R0]: https://wg21.link/P1260
[P0655R1]: https://wg21.link/P0655
[D0080R1]: pdf/D0080R1.pdf
[P0080R0]: https://wg21.link/P0080
[N3887]: https://wg21.link/N3887

## Formatting

Refer to [How I format my C++ papers][FMT] for an overview.

[FMT]: https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers

## Generation

```bash
make <paper>.pdf  // Generates `pdf/<paper>.pdf` from `<paper>.pandoc`
make <paper>.md   // Generates `github/<paper>.md` from `<paper>.pandoc`
```

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
