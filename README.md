# `MPark/WG21`

A [Pandoc](https://pandoc.org)-based framework for improving the **authoring**
and **reviewing** experience of C++ proposals for WG21.

## Documentation

In short, you write your papers in Markdown with various C++ proposal-specific
extensions, and the framework produces the paper either in HTML or PDF.

The detailed documentation is **written with the framework itself** (see
[MANUAL.md](MANUAL.md)), and published as a user's guide in HTML and PDF:

  - [User's Guide, rendered as HTML](https://mpark.github.io/wg21/MANUAL.html)
  - [User's Guide, rendered as PDF](https://mpark.github.io/wg21/MANUAL.pdf)

## Testing

The framework has rendering tests and per-paper Makefile layout tests under
[tests](tests). The expected HTML and LaTeX output for the rendering tests is
checked in under [tests/expected](tests/expected).

From the repository root:

```sh
make check         # run rendering and paper.mk tests
```

From [tests](tests), the following commands are available:

```sh
cd tests

make check         # run rendering and paper.mk tests
make expected      # overwrite the checked-in HTML/LaTeX expected/ output

make heading.html  # build a specific test case into generated/heading.html

make               # build all of the test cases in all formats into generated/
make html          # build all of the test cases in HTML format into generated/
make latex         # build all of the test cases in LaTeX format into generated/
make pdf           # build all of the test cases in PDF format into generated/
```

`make check` verifies that the rendered HTML and LaTeX have not changed, and
also checks the per-paper Makefile layout. If a rendering change is expected,
run `make expected`, review the diff, and check in the updated files under
[tests/expected](tests/expected).

## Resources

- [Example paper repository](https://github.com/mpark/wg21-papers)
- [How I format my C++ papers](https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers)
- [WG21 Paper in Markdown](https://www.youtube.com/watch?v=8yReHZOw6QY)

## License

Distributed under the Boost Software License, Version 1.0. See [LICENSE.md](LICENSE.md).
