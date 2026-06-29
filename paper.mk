# Per-paper project layout:
#
#   wg21-papers/
#   |-- wg21 (submodule)
#   |-- p2806/
#   |   |-- Makefile
#   |   |-- p2806r4.md
#   |   `-- p2806r4.html
#   `-- reflection/
#       |-- Makefile
#       |-- reflection.md
#       `-- p2996r13.html
#
# In p2806/Makefile:
#
#   include ../wg21/paper.mk

# With that in place, same-stem targets are available:
#
#   cd p2806
#   make p2806r4.html   # builds p2806r4.html from p2806r4.md
#   make                # also builds p2806r4.html from p2806r4.md
#
# You may also introduce explicit source-to-output mappings.
#
# In reflection/Makefile:
#
#   p2996r13.html: reflection.md
#   include ../wg21/paper.mk
#
# With that mapping, you can use:
#
#   cd reflection
#   make p2996r13.html  # builds p2996r13.html from reflection.md
#   make                # also builds p2996r13.html from reflection.md
#
# The following variables can be set before including this file:
#
#   - DEFAULTS := <path/to/defaults.yaml>
#
#     Passed to Pandoc as an additional defaults file.
#
#   - REQUIREMENTS := <path/to/requirements.txt>
#
#     Passed to Python virtual env to install additional packages.
#
# To set these variables at repo-level, create a top-level mk file with:
#
#   DEFAULTS := ...
#   REQUIREMENTS := ...
#   include path/to/wg21/paper.mk
#
# and from each of the per-paper Makefile, include that top-level mk file.

OUTDIR := .
DEFAULTS ?=
REQUIREMENTS ?=

include $(dir $(lastword $(MAKEFILE_LIST)))flat.mk

%.html: $(DEPS)
	$(PANDOC)

%.latex: $(DEPS)
	$(PANDOC)

%.pdf: $(DEPS)
	$(PANDOC)
