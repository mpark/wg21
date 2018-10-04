# WG21: C++ Standards Committee Papers

- [N3887]: Consistent Metafunction Aliases
- [P0080R0]: Variant: Discriminated Union with Value Semantics
- [D0080R1]: Tweaks to the Kona Variant
- [P0655R1]: `visit<R>`: Explicit Return Type for `visit`

[N3887]: pdf/N3887.pdf
[P0080R0]: pdf/P0080R0.pdf
[D0080R1]: pdf/D0080R1.pdf
[P0655R1]: pdf/P0655R1.pdf

## Generation

```bash
make <paper>.latex  // Generates `latex/<paper>.latex` from `<paper>.md`
make <paper>.pdf    // Generates `pdf/<paper>.pdf` from `<paper>.md`
```

## Requirements

  - `pandoc 2`
  - `pandoc-citeproc`
  - `pdflatex`
