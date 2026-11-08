# Getting started

This file takes you from an empty machine to a built paper. After reading it you will know which tools to install for HTML and for PDF output, how to add the framework to your paper repository, how to build a first paper in both formats, and what the framework quietly sets up for you on that first build so you never have to install Pandoc or configure Python yourself.

## What you need

For HTML output you need only five things installed:

- `git`
- `curl`
- `make`
- `python3`
- `python3-venv`

PDF output additionally needs `xelatex`, which means a TeX installation. HTML builds and LaTeX source (`.latex`) builds never use it, and the framework does not install a TeX distribution for you, so if you only want HTML you can skip TeX entirely.

On macOS, install the prerequisites with Homebrew, and add MacTeX only if you want PDF output:

````bash
brew install python make

# For PDF output
brew install --cask mactex
````

On Ubuntu:

````bash
sudo apt-get install git curl make python3 python3-venv

# For PDF output
sudo apt-get install texlive-xetex
````

On Debian, the base packages are the same, but PDF output needs three more TeX Live packages than Ubuntu does:

````bash
sudo apt-get install git curl make python3 python3-venv

# For PDF output
sudo apt-get install texlive-xetex \
                     texlive-fonts-recommended \
                     texlive-latex-recommended \
                     texlive-latex-extra
````

A few things the install commands take for granted are worth checking before your first build:

- `python3` must be on your PATH with the standard `venv` module available. The framework never downloads Python; it uses whatever `python3` your shell finds.
- The build scripts use bash, curl, and tar, so all three must be present.
- On macOS, the Pandoc archive is unpacked with the stock macOS `tar` (bsdtar). If you have put GNU tar ahead of it on your PATH, the Pandoc install breaks.
- The first build needs network access to github.com (for Pandoc), the Python package index that pip uses (for the Python packages), wg21.link (for the citation data), and eel.is (for the stable-name data).

## A note for Windows users

> **Note:** The upstream documentation gives install instructions only for macOS, Ubuntu, and Debian. The build needs a Unix-like environment with bash, make, curl, and python3 with `venv`, and a native Windows shell stops the first build with the message `Unsupported OS: <name>.` because only Linux and macOS are accepted. Running the build under WSL, which reports itself as Linux, is the likely route, but it is not documented upstream. Follow the Ubuntu or Debian instructions inside your WSL distribution.

## Adding the framework to your repository

Add the framework to your own paper repository as a git submodule. Run this at the top of your paper repository:

````bash
git submodule add https://github.com/mpark/wg21.git
````

This checks the framework out into a directory named `wg21`. Next, create a `Makefile` at the top level containing a single line:

````make
include wg21/flat.mk
````

That line selects the flat layout, where every paper is a Markdown file in the top-level directory and the built outputs are collected in a `generated/` folder. Once you have a couple of papers and have built them as HTML, the repository looks like this:

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

The flat layout is not your only option. If you prefer one directory per paper, see [the per-paper layout](02-project-layouts.md#the-per-paper-layout). You do not have to choose one layout for the whole repository; a single repository can use both.

## Your first paper

A minimal working paper is a Markdown file that starts with a YAML front matter block between two `---` lines, followed by ordinary Markdown headings and prose. Save this as `p0000r0.md` next to your `Makefile`:

````markdown
---
title: My First Paper
document: P0000R0
date: 2026-01-01
audience: WG21
author:
  - name: Test Author
    email: <author@example.com>
---

# Introduction

This is my first paper.
````

A few details in that block matter. The `author` key is a YAML list of mappings (each entry starts with `- name:`), not a plain string. The `document` key uses the uppercase `PnnnnRn` form. The `date` uses ISO `YYYY-MM-DD`. The `email` is written in angle brackets; give every author one, because an author with only a `name` shows an empty `<>` line under Reply-to in the HTML output. Each key is covered in [Paper metadata](04-paper-metadata.md#the-front-matter-block).

Build it as PDF:

````bash
make p0000r0.pdf
````

This writes `generated/p0000r0.pdf`. The `generated/` folder is created automatically on the first build. The PDF opens with the title centered in large type and a right-aligned table with the rows Document #, Date, Project, Audience, and Reply-to. The Project row reads "Programming Language C++" even though you did not set it. A table of contents comes next, then the section "1 Introduction".

Build it as HTML:

````bash
make p0000r0.html
````

This writes `generated/p0000r0.html`, a single standalone file you can open in any browser. The title is centered at the top with the same table of facts under it, and because `P0000R0` has the expected P-number and revision form, the Document # row also shows [Latest] and [Status] links pointing at wg21.link.

A bare `make` builds every paper in the directory as HTML. The [Building papers](03-building.md#building-every-paper) file covers that and every other target.

## What the first build does

Your very first `make` takes longer than any later one, because it sets up everything the framework needs inside the `wg21` checkout. Nothing is installed system-wide, and every paper that includes this checkout shares the same setup.

### Pandoc

You never install Pandoc yourself. The first build downloads Pandoc 3.9.0.2 straight from the official jgm/pandoc GitHub releases into `deps/pandoc/3.9.0.2/` inside the wg21 checkout. Only the Pandoc executables are installed, not the whole release bundle. During builds this folder is placed first on the PATH, so any Pandoc already on your system is left untouched and is not used for paper builds.

The version is fixed by the framework. Trying to change the Pandoc version or its install folder from the make command line or from the shell environment has no effect, which means every co-author builds with the identical Pandoc and gets the same output.

Which Pandoc gets downloaded depends on your platform:

- On Linux, the build always downloads the x86-64 (amd64) Pandoc, regardless of your CPU. On ARM Linux (aarch64), the downloaded Pandoc will not run natively.
- On macOS, both Intel and Apple Silicon work: the build picks the download that matches the CPU reported by `uname -m`, such as `x86_64` or `arm64`.
- On any other operating system (native Windows shells, BSDs, and others), the first build stops before downloading with the message `Unsupported OS: <name>.` and exit code 1, where `<name>` is the output of `uname -s`.

The download shows no progress bar, but download errors still print. Every fetch is a clean install: the version folder is wiped and recreated before downloading, so a stale or corrupted copy is replaced rather than patched. The build reinstalls Pandoc whenever the framework's Pandoc installer changes. When you update the framework to a new pinned Pandoc version, the next build installs it side by side in its own `deps/pandoc/<version>/` folder and rebuilds your papers with it; older versions stay on disk until you run `make distclean`, which deletes the framework's downloaded tools and data.

### The Python environment

You never set up Python yourself either. The first build creates a Python virtual environment at `deps/python/` inside the wg21 checkout, using your system `python3`, and runs all of the framework's helper scripts with it. Its location is fixed by the framework and cannot be changed through make.

Inside that environment, a single pip command upgrades pip to its latest release and installs the framework's packages. The complete list is the six-line file `deps/requirements.txt` in pip requirements format: `panflute==2.3.1` followed by five bare package names, `beautifulsoup4`, `livereload`, `lxml`, `requests`, and `pyyaml`, with no version constraint on those five. Any extra requirements files you name are installed alongside them; [Your own defaults and packages](03-building.md#your-own-defaults-and-packages) explains how to name them.

To force a clean reinstall of the Python tooling, for example after upgrading your system Python, delete the framework's `deps/python` directory. The next build recreates it from scratch.

### Citation and stable-name data

The first build also downloads two sets of reference data into the `data/` folder of the wg21 checkout:

- It downloads the wg21.link paper index and generates the citation database `data/csl.json`. This is what lets you cite any WG21 paper without writing a bibliography entry.
- It downloads the list of stable names from the C++ working draft at `https://eel.is/c++draft` into `data/srefs.json`, and turns that into Markdown link definitions in `data/srefs.defs`. This is what makes `[basic.life]` a link.

None of these files ships with the framework, so every fresh checkout fetches them once. Each step reruns when the framework's generator for it changes. An HTTP error while fetching the stable-name list fails the build, and a failed wg21.link fetch stops the build without overwriting an existing good bibliography. The same downloads happen again, on demand, when you run `make update`; see [Refreshing citation and stable-name data](03-building.md#refreshing-citation-and-stable-name-data).

### If the first build fails

If a first-time setup fails or is interrupted, run `make` again. Generated data files are moved into place only after they are written successfully, so a half-written file never counts as done. A failed Pandoc download, including one that breaks off midway, deletes the half-populated Pandoc folder so the next build retries from scratch. If creating the Python environment or installing any package fails (for example a bad package name or a network error), the half-built environment is deleted and the build stops, so the next `make` retries cleanly.

### Why later builds are fast

After the first build, Pandoc, the Python environment, and the data files already exist, and make only redoes a step when that step's inputs change. Re-running `make` after editing one paper rebuilds only the papers whose source, or a framework input, changed.

Previous: [MPark/WG21 User Guide](README.md) | Next: [Project layouts](02-project-layouts.md)

*2026-09-25 - claude-opus-5.5*
