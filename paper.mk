# Per-paper project layout:
#
#   wg21-papers/
#   |-- wg21 (submodule)
#   |-- p2806/
#   |   |-- Makefile
#   |   |-- p2806r4.md
#   |   `-- p2806r4.html
#   `-- p2996/
#       |-- Makefile
#       |-- p2996r13.md
#       `-- p2996r13.html
#
# In each per-paper Makefile:
#
#   include path/to/wg21/paper.mk
#
# With that in place, the following commands are available:
#
#   cd p2806
#   make p2806r4.html   # builds p2806r4.html from p2806r4.md
#   make p2806r4.latex  # builds p2806r4.latex from p2806r4.md
#   make p2806r4.pdf    # builds p2806r4.pdf from p2806r4.md
#
# You may also introduce explicit source-to-output mappings.
# For example, given a layout like:
#
#   wg21-papers/
#   |-- wg21 (submodule)
#   |-- p2806-do-expr/
#   |   |-- Makefile
#   |   |-- do-expr.md
#   |   `-- p2806r4.html
#   `-- p2996-reflection/
#       |-- Makefile
#       |-- reflection.md
#       `-- p2996r13.html
#
# In p2806-do-expr/Makefile:
#
#   include path/to/wg21/paper.mk
#   p2806r4.html: do-expr.md
#
# In p2996-reflection/Makefile:
#
#   include path/to/wg21/paper.mk
#   p2996r13.html: reflection.md
#
# With those mappings, you can use them to build:
#
#   cd p2806-do-expr
#   make p2806r4.html   # builds p2806r4.html from do-expr.md
#
#   cd p2996-reflection
#   make p2996r13.html  # builds p2996r13.html from reflection.md
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

DEFAULTS ?=
REQUIREMENTS ?=

include $(dir $(lastword $(MAKEFILE_LIST)))wg21.mk

%.html: %.md $(DEPS)
	$(PANDOC)

%.latex: %.md $(DEPS)
	$(PANDOC)

%.pdf: %.md $(DEPS)
	$(PANDOC)

%.html: $(DEPS)
	$(PANDOC)

%.latex: $(DEPS)
	$(PANDOC)

%.pdf: $(DEPS)
	$(PANDOC)

.DEFAULT_GOAL :=
