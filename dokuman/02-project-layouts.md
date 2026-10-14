# Project layouts

The framework gives you two ways to arrange a paper repository, and you can mix them freely. After reading this file you will be able to set up the flat layout (all papers side by side in one directory) or the per-paper layout (one directory per paper), keep a paper's source under a descriptive name while publishing it under its paper number, share make settings across papers, keep machine-specific settings out of git, and add make rules of your own without breaking the standard targets.

The framework ships two Makefile fragments for these layouts, `flat.mk` and `paper.mk`. You do not have to choose one: a single repository can use both, for example a flat set of small papers at the top level plus a directory for one large paper.

Wherever the framework sits (typically as the `wg21` git submodule), every paper that includes it shares one Pandoc install, one Python environment, and one set of downloaded data, because the framework finds its own files relative to where it sits. The checkout can have any path and any submodule name.

## The flat layout

In the flat layout, every paper is a Markdown file in one top-level directory, and the top-level `Makefile` contains one line:

````make
include wg21/flat.mk
````

Outputs are collected in a shared `generated/` directory. A typical flat-layout repository looks like this:

````text
wg21-papers/
|-- wg21 (submodule)
|-- Makefile
|-- p2806r4.md
|-- p2996r13.md
`-- generated/
    |-- p2806r4.html
    `-- p2996r13.html
````

The example paper repository, [mpark/wg21-papers](https://github.com/mpark/wg21-papers), uses this layout.

You add a paper just by dropping its `.md` file into the top-level directory. It is picked up by `make`, `make html`, `make latex`, `make pdf`, and `make clean` with no Makefile edits. Only top-level `.md` files are papers; `.md` files in subdirectories are never built. A few repository documents are also skipped, which [Which Markdown files get built](03-building.md#which-markdown-files-get-built) covers.

Each top-level Markdown file becomes a build target with the same stem:

````bash
make p2806r4.html   # builds generated/p2806r4.html from p2806r4.md
make p2806r4.pdf    # builds generated/p2806r4.pdf from p2806r4.md
````

You do not have to name the source file after its paper number. A file called `do-expr.md` gives the targets `do-expr.html` and `do-expr.pdf`, producing `generated/do-expr.html` and `generated/do-expr.pdf`. The WG21 paper submission system renames the uploaded file to the paper number and revision anyway, so `do-expr.html` becomes `P2806R4.html` when you submit it. The document number printed in the paper's title block comes from the paper's `document:` front matter field, never from the file name.

Including `flat.mk` also gives you three shared targets, `make serve`, `make update`, and `make distclean`, which [Building papers](03-building.md#the-live-server) explains.

## The per-paper layout

In the per-paper layout, each paper sits in its own directory with its own `Makefile`, and that Makefile includes `paper.mk` by a relative path. For a paper directory one level below the repository root, `p2806/Makefile` contains:

````make
include ../wg21/paper.mk
````

Outputs are always written into the paper's own directory, right next to the Markdown source. A typical per-paper repository looks like this:

````text
wg21-papers/
|-- wg21 (submodule)
|-- p2806/
|   |-- Makefile
|   |-- p2806r4.md
|   `-- p2806r4.html
`-- p2996_reflection/
    |-- Makefile
    |-- reflection.md
    `-- p2996r13.html
````

The repository [brevzin/cpp_proposals](https://github.com/brevzin/cpp_proposals) uses this layout. A paper directory can sit one level down or deeper; you just adjust the relative path in the `include` line, and no other path setup is needed.

Each per-paper directory runs in one of two modes. Leave the `PAPER_RULE` variable unset and the directory builds outputs named after each Markdown file (same-stem mode, described here). Set `PAPER_RULE` and the directory builds a named paper from a differently named source (mapped mode, described in [Mapping a source file to a paper number](#mapping-a-source-file-to-a-paper-number)). Different directories in the same repository can use different modes. In the tree above, `p2806/` is a same-stem directory and `p2996_reflection/` is a mapped one.

### Same-stem mode

With no mapping set, same-stem targets work automatically:

````bash
cd p2806
make p2806r4.html   # builds p2806r4.html from p2806r4.md
make                # also builds p2806r4.html from p2806r4.md
````

`make p2806r4.pdf` and `make p2806r4.latex` do the same for PDF and LaTeX, writing into the paper directory. You can also build from the repository root with `make -C`: in a directory `p0000/` holding `p0000r0.md` and a one-line Makefile, `make -C p0000` builds `p0000/p0000r0.html`.

A bare `make` in a same-stem directory builds every Markdown file in that directory, except `README.md`, `CHANGELOG.md`, and `LICENSE.md`, in the default format (HTML unless you change it). With one paper per directory, that is just that paper. Likewise, `make html`, `make pdf`, or `make latex` builds every paper in the directory in that format, and `make clean` deletes the HTML, PDF, and LaTeX outputs for every Markdown file in the directory while leaving the sources alone. From the root, that is `make -C p0000 clean`.

The flat layout has an `OUTDIR` variable for choosing the output directory. It does nothing here: in the per-paper layout every built file lands next to its source, and an `OUTDIR` set in the per-paper Makefile before the include is overwritten.

`make update` and `make distclean` can be run from any paper directory in either mode. Both act on the shared framework checkout, so they affect every paper in the repository.

## Mapping a source file to a paper number

Often you want to keep a paper's source under a stable descriptive name across revisions, and publish it under the official paper number. The `PAPER_RULE` variable does that in a per-paper directory. Put it in the Makefile before the `include` line:

````make
PAPER_RULE := p2996r13:reflection
include ../wg21/paper.mk
````

This registers `p2996r13.html`, `p2996r13.pdf`, and `p2996r13.latex` as outputs built from `reflection.md`. The format is `<paper-id>:<source-stem>`. The source is written without `.md` (the framework adds it), and the paper id is written without a format extension. The mapping must be set before the include, and its outputs are written next to the source in the same folder, not into a `generated/` folder.

With the mapping in place, these commands work in that directory:

````bash
cd p2996_reflection
make p2996r13.html   # builds p2996r13.html from reflection.md
make                 # also builds p2996r13.html from reflection.md
````

`make p2996r13.pdf` and `make p2996r13.latex` build the PDF and LaTeX. `make html`, `make pdf`, and `make latex` build only the mapped paper in that format. `make clean` deletes exactly the mapped paper's HTML, PDF, and LaTeX outputs and leaves the source and every other file in the directory alone. Setting `DEFAULT_FORMAT := pdf` or `DEFAULT_FORMAT := latex` before the include changes what a bare `make` produces.

Mapped targets are named by paper id, not by source name. In a directory with `PAPER_RULE := p2806r4:do-expr`, `make p2806r4.pdf` works, but `make do-expr.html` is not the mapped target. A mapped directory builds only the mapped paper: same-stem targets like `make reflection.html` are not available there, and any other Markdown files in the directory are ignored by bare `make`, `make html`, `make pdf`, and `make latex`. The mapping takes a single `output:source` pair, so a mapped directory holds exactly one paper; anything written after the first pair is ignored.

The payoff comes at revision time. To publish the next revision, edit only the mapping line, from `p2996r13` to `p2996r14`, with no file renames. Remember to update the `document:` field in the paper's front matter too, since that, not the mapping, is what prints in the title block.

Mapped outputs rebuild automatically when either the source or the framework's own templates, filters, styles, or reference data change, and the Pandoc and Python toolchain is installed on the first build, just as in the other modes.

Two conveniences of same-stem directories are missing in mapped mode. A `defaults.yaml` or `requirements.txt` in the directory is not picked up automatically; name it explicitly with `DEFAULTS := defaults.yaml` or `REQUIREMENTS := requirements.txt` before the include. And a misspelled `DEFAULT_FORMAT` is not caught up front with a clear message; it fails as an unknown make target instead. Both variables are explained in [Building papers](03-building.md#your-own-defaults-and-packages).

### The older explicit-rule form

Before `PAPER_RULE` existed, you mapped a paper number onto a differently named source by writing a plain make rule, and that form still works:

````make
p2996r13.html: reflection.md
include ../wg21/paper.mk
````

`paper.mk` supplies the build recipe, and the result is the same paper the `PAPER_RULE` form produces. The explicit rule maps only the outputs you name, so each format needs its own line, such as `p2996r13.pdf: reflection.md` or `p2996r13.latex: reflection.md`.

Put the explicit rule above the `include` line. Make's default goal is the first rule it reads, so with the rule on top a bare `make` (and a bare `make serve`) builds the mapped paper. If the rule comes after the include, a bare `make` falls back to same-stem behavior and builds `reflection.html` from `reflection.md`. In an explicit-rule directory, `make clean` removes only the same-stem outputs (`reflection.html`, `reflection.pdf`, `reflection.latex`) and leaves the mapped `p2996r13` outputs for you to delete by hand.

Prefer `PAPER_RULE` over explicit rules when you want automatic rebuilds after framework updates. An explicit-rule output depends only on the Markdown file it names, so it is not rebuilt when framework templates, filters, or reference data change, and the framework's Pandoc and Python toolchain is not installed on demand for it.

## Sharing and local settings

Settings in make are just variable assignments, and the framework's settings belong before the `include` line. The User's Guide recommends two conventional files to keep those assignments organized. The framework itself never reads either file; each works only because your own Makefile includes it.

### Shared settings in config.mk

To share make settings across all per-paper directories, create a top-level `config.mk` next to the `wg21` submodule. For example, to make every paper default to PDF:

````make
# config.mk
DEFAULT_FORMAT := pdf
````

Then include it from each paper's Makefile, before `paper.mk`:

````make
# p2806/Makefile
include ../config.mk
include ../wg21/paper.mk
````

### Machine-specific settings in local.mk

The User's Guide recommends keeping machine-specific or organization-specific environment variables and other local settings in a `local.mk` file next to the top-level `Makefile`:

````text
wg21-papers/
|-- wg21 (submodule)
|-- Makefile
|-- local.mk
|-- p2806r4.md
|-- p2996r13.md
`-- generated/
````

In the flat layout, load it only where it exists by putting an optional include at the top of the `Makefile`, before the layout include. The leading dash makes the include optional, so machines without a `local.mk` build normally:

````make
# Makefile
-include local.mk
include wg21/flat.mk
````

In the per-paper layout, add the optional include to each paper's Makefile after `include ../config.mk` and before `include ../wg21/paper.mk`:

````make
# p2806/Makefile
include ../config.mk
-include ../local.mk
include ../wg21/paper.mk
````

List `local.mk` in `.gitignore` and create it only on machines that need it. The checked-in `Makefile` then stays the same everywhere.

A common use is pointing the build's downloads at an organization's CA certificate bundle. Each of these lines goes in `local.mk`; the first covers the build in general, the second covers Python HTTP downloads, and the third covers pip package installs:

````make
export SSL_CERT_FILE      := /etc/ssl/certs/ca-certificates.crt
export REQUESTS_CA_BUNDLE := /etc/ssl/certs/ca-certificates.crt
export PIP_CERT           := /etc/ssl/certs/ca-certificates.crt
````

## Rules of your own

Variables go before the `include` line, but your own rules should go after it. The reason is make's default goal: when you type a bare `make`, make runs the first rule it reads. The layout file's first rule is the one that builds all papers in the default format, so including the layout file before your own rules keeps a bare `make` doing that. Any rule written above the include becomes the default instead.

````make
include wg21/flat.mk

.PHONY: everything
everything: html pdf
````

Here a bare `make` still builds every paper as HTML, `make everything` builds every paper as both HTML and PDF, and every standard framework target (`html`, `latex`, `pdf`, `clean`, and the per-file targets) keeps working. If you put the include at the end instead, your first rule becomes what a bare `make` runs. The framework's own test suite does exactly that, so a bare `make` there runs its `check` target.

A few facts help when you write recipes:

- Recipes in a Makefile that includes the framework run under bash.
- In those recipes, `pandoc` and `python3` resolve to the pinned Pandoc and the build environment's Python, not to whatever is on your system.
- Command-line tools installed by your extra requirements files can be used directly in recipes, because the environment's `bin` directory is on the PATH for every recipe.
- The framework exposes a public `DEPS` list of the framework files every paper build depends on (templates, filters, the pinned Pandoc and Python toolchain, and the downloaded data), apart from the paper's own Markdown, so your rules can depend on the same things a paper build does.

You can also split one paper across several Markdown files by listing more than one `.md` prerequisite on its output target. The `.md` files are passed to Pandoc in the order listed, and non-Markdown prerequisites are ignored. For example, in a per-paper directory using the explicit-rule form:

````make
p2996r13.html: reflection.md appendix.md
include ../wg21/paper.mk
````

This builds `p2996r13.html` from `reflection.md` followed by `appendix.md`. Keep the front matter at the top of the first file; some settings, such as the HTML table of contents depth, are read only from there.

Previous: [Getting started](01-getting-started.md) | Next: [Building papers](03-building.md)

*2026-09-25 - claude-opus-5.5*
