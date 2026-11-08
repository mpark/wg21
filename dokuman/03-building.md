# Building papers

Everything you do with the framework goes through `make`. After reading this file you will know every target and variable an author uses: how to build one paper or all of them in any format, where the output goes, which Markdown files count as papers, how to add your own Pandoc defaults and Python packages, how to clean up, how to refresh the citation and stable-name data, how to preview a paper live while you edit, and what the build errors and warnings from make itself mean.

Most examples here use the flat layout, where outputs land in `generated/`. In the per-paper layout the same targets exist but outputs land next to the source; [Project layouts](02-project-layouts.md#the-per-paper-layout) covers the differences.

## Building one paper

Ask make for the output file you want, named after the paper's Markdown file:

````bash
make p2806r4.html    # builds generated/p2806r4.html from p2806r4.md
make p2806r4.latex   # builds generated/p2806r4.latex from p2806r4.md
make p2806r4.pdf     # builds generated/p2806r4.pdf from p2806r4.md
````

The HTML target produces a single self-contained web page. The LaTeX target produces the intermediate LaTeX source; note that the extension is `.latex`, not `.tex`. The PDF target typesets the paper through LaTeX with `xelatex`, so it is the only one that needs TeX installed.

The bare file name, such as `p2806r4.html`, is a shortcut for the file inside the output directory, and make always checks whether that real output file is up to date. You can also request the full output path directly:

````bash
make generated/p2806r4.pdf
````

Every paper build runs the pinned Pandoc on your Markdown with the framework's data directory and its built-in defaults. Build papers through make rather than running Pandoc by hand: the framework's defaults point at its own data directory, which make hands to Pandoc on every build, so a hand-run Pandoc without that same data directory breaks those paths.

Format targets can be combined in one command, and you can set the output directory on the command line at the same time. This renders every paper in the directory to both HTML and LaTeX in `<dir>`:

````bash
make OUTDIR=<dir> html latex
````

### What gets rebuilt

Re-running `make` after editing one paper rebuilds only the papers whose source, or a framework input, changed. Papers also rebuild automatically when the framework itself changes, for example after you update the `wg21` submodule. Every output depends on the framework's citation style, defaults files, filters, syntax-highlighting definitions and theme, HTML and LaTeX templates, stylesheets and scripts, favicon, default metadata, and helper scripts, plus the installed Pandoc, the Python environment, and the downloaded citation and stable-name data. Editing your own defaults file (described below) also rebuilds every paper.

Editing a Makefile alone does not force papers to rebuild. If you change a make variable and want to see its effect on papers that are already up to date, run `make clean` first.

## Building every paper

A bare `make`, which is the same as `make all`, builds every paper in the default format. The default format is HTML unless you configure otherwise. Three more targets build every paper in one specific format:

````bash
make         # builds all papers in the default format (HTML unless changed)
make html    # builds all papers in HTML format
make latex   # builds all papers in LaTeX format
make pdf     # builds all papers in PDF format
````

### Setting make variables

You configure the build by assigning make variables in your Makefile above the `include` line. Assignments placed after the include come too late for settings such as `OUTDIR` and `DEFAULT_FORMAT`, so keep them all above it. The first variable most people set is `DEFAULT_FORMAT`.

### DEFAULT_FORMAT

`DEFAULT_FORMAT` chooses what a bare `make` builds, and also what a `make serve` with no paper named builds. It takes `html`, `pdf`, or `latex`, and defaults to `html`. To make PDF the default:

````make
DEFAULT_FORMAT := pdf
include wg21/flat.mk
````

In the per-paper layout, the same line before `include ../wg21/paper.mk` changes what a bare `make` and a bare `make serve` build in that directory, in both same-stem and mapped modes.

You can override the default format for a single run without editing the Makefile:

````bash
make DEFAULT_FORMAT=latex
make -C p2806 DEFAULT_FORMAT=latex   # produces p2806/p2806r4.latex instead of the HTML
````

The value is checked. A mistyped `DEFAULT_FORMAT` in the flat layout or in a same-stem per-paper directory stops the build immediately, before anything is built, with:

````text
DEFAULT_FORMAT must be one of html, pdf, latex
````

The values are lowercase and case-sensitive, so `PDF` or `tex` fail. Because the check runs as soon as make reads the layout file, it aborts every make run, including `make clean`. In a mapped per-paper directory the value is not checked up front; a bad value there fails as an unknown make target instead, so spell it exactly `html`, `pdf`, or `latex`.

### One-off overrides

Any of the settings `OUTDIR`, `DEFAULT_FORMAT`, `DEFAULTS`, and `REQUIREMENTS` can be overridden for one build from the command line or the environment, without editing the Makefile:

````bash
make pdf OUTDIR=out
make DEFAULT_FORMAT=pdf
````

A command-line value beats a Makefile assignment, and an environment value is used when the Makefile does not set one.

## Choosing the output directory

`OUTDIR` sets the flat layout's output directory and defaults to `generated`. To build into `out/` instead:

````make
OUTDIR := out
include wg21/flat.mk
````

The output directory is created automatically on the first build, including nested paths, and its timestamp never forces rebuilds.

One value is special. Setting `OUTDIR := .` writes built papers right next to their sources, for example `p2806r4.html` beside `p2806r4.md`. Only the literal value `.` has this effect. Be careful with it: with `OUTDIR` set to `.`, `make clean` deletes every top-level `.html`, `.pdf`, and `.latex` file that shares a base name with a paper, including any you maintain by hand.

In the per-paper layout, `OUTDIR` has no effect. Outputs always land next to the source there, and an `OUTDIR` set in the per-paper Makefile is overwritten.

## Which Markdown files get built

In the flat layout, every `.md` file in the top-level directory is a paper, with three exceptions. Repository documents named exactly `CHANGELOG.md`, `LICENSE.md`, and `README.md` are never built as papers. The match is case-sensitive, so any other top-level `.md` file, such as `readme.md` or `NOTES.md`, is treated as a paper and built. Markdown files in subdirectories are never built.

A same-stem per-paper directory follows the same rule for the files in that directory. A mapped per-paper directory builds only the one source named in its `PAPER_RULE` and ignores every other Markdown file there.

## Your own defaults and packages

Two variables let you extend what the framework does for every paper: `DEFAULTS` adds a Pandoc defaults file of your own, and `REQUIREMENTS` adds Python packages to the build environment. This section covers how to name them; [Customization](10-customization.md#your-own-defaults-file) covers what to put in them.

### DEFAULTS

`DEFAULTS` names your own Pandoc defaults file. It is empty by default. The file is applied after the framework's built-in defaults, so its settings layer on top of theirs. It can come from the Makefile, the environment, or the command line, as in `make DEFAULTS=...`. Editing the file it names rebuilds your papers, and `make serve` watches it too.

````make
DEFAULTS := pandoc-defaults.yaml
include wg21/flat.mk
````

In the flat layout you often do not need the variable at all: a file named exactly `defaults.yaml` in the top-level directory is used as the extra defaults file automatically. `defaults.yml` is not detected. Setting `DEFAULTS` explicitly replaces the automatic file rather than adding to it.

### REQUIREMENTS

`REQUIREMENTS` names one or more pip requirements files whose packages are installed into the build's Python environment alongside the framework's own, for example packages your own Pandoc filters need. It is empty by default. Each file is handed to pip, and editing a named file rebuilds the Python environment.

````make
REQUIREMENTS := requirements.txt filter-requirements.txt
include wg21/flat.mk
````

In the flat layout, a top-level `requirements.txt` is used for `REQUIREMENTS` automatically.

### Automatic pickup in each layout

- In the flat layout, a top-level `defaults.yaml` and a top-level `requirements.txt` are picked up automatically.
- In a same-stem per-paper directory, a `defaults.yaml` or `requirements.txt` placed in that directory is picked up automatically for the papers there.
- In a mapped per-paper directory there is no automatic pickup, so name a local file explicitly with `DEFAULTS := defaults.yaml` or `REQUIREMENTS := requirements.txt` before the include.

To stop a `defaults.yaml` or `requirements.txt` from being picked up, set the matching variable to empty before the include:

````make
DEFAULTS :=
include wg21/flat.mk
````

## Cleaning up

`make clean` deletes built papers; `make distclean` deletes the downloaded toolchain and data.

### make clean

In the flat layout, `make clean` deletes the HTML, LaTeX, and PDF output of every current top-level paper from the output directory. It leaves the output directory itself, unrelated files in it, and the downloaded Pandoc and Python toolchain alone. It only removes outputs that match the `.md` files present right now, so outputs of papers you deleted or renamed are left behind for you to remove by hand. With `OUTDIR := .`, remember that it also deletes hand-maintained files that share a paper's base name.

In the per-paper layout, what `make clean` removes depends on the directory's mode:

- In a same-stem directory, it deletes the HTML, PDF, and LaTeX outputs for every Markdown file in that directory and leaves the sources alone.
- In a mapped directory, it deletes exactly the mapped paper's outputs (for example `p2806r4.html`, `p2806r4.pdf`, and `p2806r4.latex`) and leaves the source and every other file alone.
- In an explicit-rule directory, it removes only the same-stem outputs (such as `reflection.html`), not the mapped ones.

### make distclean

`make distclean` wipes the downloaded Pandoc (every version), the Python environment, and the generated citation and stable-name files (`data/csl.json`, `data/srefs.json`, and `data/srefs.defs` in the wg21 checkout). The next build downloads and regenerates all of them. You can run it from any paper directory in either layout; it acts on the shared framework checkout, so it affects every paper in the repository.

## Refreshing citation and stable-name data

The citation database and the stable-name index are downloaded once, on the first build, and then kept. They do not update themselves. `make update` refreshes both from the latest wg21.link and eel.is data:

````bash
make update
````

It forces both to regenerate even when they look up to date, and your papers then rebuild on the next build. It needs internet access to wg21.link and eel.is. If a fetch fails, the previous data files stay in place, so a failed update never leaves you worse off.

Run it when a citation or stable name you expect to work does not resolve. Two build warnings point you here: the "stable name not found" warning and the "stale local paper index" warning, both covered in [Output and troubleshooting](11-output-and-troubleshooting.md#warnings). Stable-name links track the working draft as of the day the data was fetched, so a name added to the draft later needs `make update`, and so does a paper published after your last fetch.

Like `make distclean`, `make update` can be run from any paper directory in either layout, and it affects every paper in the repository.

## The live server

`make serve` runs a local preview server that rebuilds your paper whenever you save and reloads it in your browser. Put `serve` in front of the target you would normally build:

````bash
make serve p2806r4.html   # rebuilds and live-reloads generated/p2806r4.html
make serve p2806r4.pdf    # rebuilds generated/p2806r4.pdf
make serve                # rebuilds and serves all papers in the default format
````

The server builds the target first, then re-runs `make <target>` whenever a watched file changes. Everything after `serve` on the command line becomes the rebuild command, so a plain `make serve` rebuilds the default goal (every paper in the default format) and `make serve p2996r13.pdf` rebuilds that PDF.

The server's site root is the paper output directory, so `make serve p2806r4.html` makes the paper available at `http://127.0.0.1:8000/p2806r4.html` in either layout. The server does not open a browser tab for you; open that address yourself.

### HTML versus PDF previews

For HTML, the page open in your browser refreshes itself after each rebuild, and a stylesheet change triggers a full page reload. For PDF, `make serve <paper>.pdf` rebuilds the PDF on every change, but live reload is only provided for HTML pages. To preview a PDF live, pair `make serve` with a PDF viewer that reloads the file when it changes, such as Skim.

### Host and port

`SERVE_HOST` and `SERVE_PORT` change the preview server's address. Define them in your Makefile before including `flat.mk` or `paper.mk`, or pass them on the command line.

`SERVE_HOST` defaults to `127.0.0.1`, which is reachable only from your own machine. To open the preview from another device, such as a tablet, listen on all interfaces:

````bash
make serve p2806r4.html SERVE_HOST=0.0.0.0
````

`SERVE_PORT` defaults to `8000`. When port 8000 is taken, pick another:

````bash
make serve SERVE_PORT=8080
````

### What the server watches

`make serve` notices edits to your paper sources, your `DEFAULTS` and `REQUIREMENTS` files, every Makefile involved (yours and the framework's), and the framework's templates, stylesheets, scripts, filters, citation style, syntax files, data generators, installers, and its own `deps/requirements.txt`.

To make it watch extra files, for example a filter script of your own, set `WATCHDEPS` in your Makefile before the include. The framework appends its own watch list to yours:

````make
WATCHDEPS := my-filter.py
include wg21/flat.mk
````

### When a build fails

If the first build fails, `make serve` stops with an error instead of starting the server, so fix the paper before previewing. Once the preview is running, a failed rebuild prints make's error in the terminal but leaves the server up, and the next save tries again.

### The live server in the per-paper layout

In a per-paper directory, `make serve p2806r4.html` rebuilds and live-reloads that paper, served from the paper directory itself at `http://127.0.0.1:8000/p2806r4.html` by default. No extra Makefile content is needed. A bare `make serve` in a same-stem directory rebuilds and live-reloads whatever a bare `make` would build there, that is every paper in the directory in the default format. In a mapped directory, a bare `make serve` rebuilds and live-reloads the mapped paper whenever its source (such as `reflection.md`) changes, and `make serve p2996r13.pdf` rebuilds the PDF on each save.

## When make cannot find your paper

In a per-paper directory without `PAPER_RULE`, if you ask make for a target that has no Markdown input, usually because of a typo in the paper name, the build stops with a clear error and a "Did you mean" hint naming the closest-matching `.md` file in the current directory:

````text
No Markdown input found for target 'P2806r4.html'. Did you mean 'p2806r4.html'? (names are case-sensitive)
````

The general form is `No Markdown input found for target '<target>'. Did you mean '<suggestion>'?`, and the details work like this:

- Only one suggestion is ever offered.
- The ` (names are case-sensitive)` note appears only when your name and the suggestion differ in letter case alone. Other typos get the suggestion without the note.
- The suggestion keeps any directory prefix and the file extension you typed and swaps in only the corrected paper name, so you can copy it straight back into `make`. For example, `make P2300R8.latex` with `p2300r8.md` present suggests `p2300r8.latex`. A wrong directory or a wrong extension is passed through unchanged, not flagged.
- Suggestions come only from `.md` files sitting directly in the directory where you run `make`, so papers kept in subdirectories are never offered.

When nothing in the directory is a close enough match, you get the bare error with no guess, so a missing paper file is not confused with a typo:

````text
No Markdown input found for target '<target>'
````

In the flat layout and in a mapped per-paper directory, a mistyped name never reaches this check. Make stops with its own error instead, with no suggestion, so compare the name against your `.md` files yourself:

````text
make: *** No rule to make target 'P2806r4.html'.  Stop.
````

## Deprecated entry points

Older paper repositories include the framework's top-level `Makefile` instead of a layout file:

````make
include wg21/Makefile
````

That still builds while you migrate. The old include forwards to the flat layout, and variables set before it (`OUTDIR`, `DEFAULT_FORMAT`, `DEFAULTS`, `REQUIREMENTS`) still take effect. It does print a deprecation warning on every make run, and the warning does not stop the build:

````text
wg21/Makefile:18: Makefile includes deprecated wg21/Makefile; include wg21/flat.mk or wg21/paper.mk instead. See https://mpark.github.io/wg21/MANUAL.html#project-layouts
````

The warning names the including makefile and reuses the same path prefix you used for the submodule, so a per-paper `include ../wg21/Makefile` suggests `../wg21/flat.mk` or `../wg21/paper.mk`. One quirk: if another file, such as `local.mk`, was included just before the deprecated include, the warning names that file instead of your Makefile.

To migrate, replace the include with `include wg21/flat.mk` when all your papers sit in one directory. That is a one-line change with no change in behavior. If you use one directory per paper, put `include ../wg21/paper.mk` in each per-paper Makefile instead, as described in [Project layouts](02-project-layouts.md#the-per-paper-layout).

## Command and variable reference

The sections above explain each of these in full, except `PAPER_RULE` and `DEPS`, which [Project layouts](02-project-layouts.md) covers. The targets an author uses:

| Target | What it does |
|---|---|
| `<paper>.html` | Builds one paper as HTML |
| `<paper>.pdf` | Builds one paper as PDF |
| `<paper>.latex` | Builds one paper as LaTeX source |
| `all` (bare `make`) | Builds every paper in `DEFAULT_FORMAT` |
| `html` | Builds every paper as HTML |
| `pdf` | Builds every paper as PDF |
| `latex` | Builds every paper as LaTeX source |
| `clean` | Deletes built outputs of the current papers |
| `serve [target]` | Builds, then rebuilds on change and serves the output directory |
| `update` | Refreshes citation and stable-name data |
| `distclean` | Deletes the downloaded Pandoc, the Python environment, and generated data |

The variables, all set before the `include` line or on the command line:

| Variable | What it does | Default |
|---|---|---|
| `OUTDIR` | Flat-layout output directory | `generated` (always `.` in the per-paper layout) |
| `DEFAULT_FORMAT` | Format for bare `make` and bare `make serve` | `html` |
| `DEFAULTS` | Your own Pandoc defaults file | empty; flat and same-stem pick up `defaults.yaml` |
| `REQUIREMENTS` | Extra pip requirements files | empty; flat and same-stem pick up `requirements.txt` |
| `SERVE_HOST` | Preview server host | `127.0.0.1` |
| `SERVE_PORT` | Preview server port | `8000` |
| `PAPER_RULE` | Per-paper `<paper-id>:<source-stem>` mapping | unset |
| `WATCHDEPS` | Extra files for `make serve` to watch | unset; the framework appends its own list |
| `DEPS` | Public list of a paper build's dependencies, for your own rules | set by the framework |

Previous: [Project layouts](02-project-layouts.md) | Next: [Paper metadata](04-paper-metadata.md)

*2026-09-25 - claude-opus-5.5*
