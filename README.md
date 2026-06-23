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

The framework has rendering tests under [tests](tests). The expected HTML and
LaTeX output is checked in under [tests/gold](tests/gold).

From [tests](tests), run:

```sh
make check       # render HTML/LaTeX into out/ and compare against gold/
make update-gold # overwrite the checked-in HTML/LaTeX gold output
make tests       # render HTML, LaTeX, and PDF into out/ for inspection
```

`make check` verifies that the rendered HTML and LaTeX have not changed. If a
change is expected, review the diff, run `make update-gold`, and check in the
updated files under [tests/gold](tests/gold) with the source change.

You can also run `make html`, `make latex`, or `make pdf` in [tests](tests) to
render just one output format into `tests/out`.

## Resources

- [Example paper repository](https://github.com/mpark/wg21-papers)
- [How I format my C++ papers](https://mpark.github.io/programming/2018/11/16/how-i-format-my-cpp-papers)
- [WG21 Paper in Markdown](https://www.youtube.com/watch?v=8yReHZOw6QY)

## License

Distributed under the Boost Software License, Version 1.0. See [LICENSE.md](LICENSE.md).
