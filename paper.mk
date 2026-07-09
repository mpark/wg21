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
#   PAPER_RULE := p2996r13:reflection
#   include ../wg21/paper.mk
#
# With that mapping, you can use:
#
#   cd reflection
#   make p2996r13.html  # builds p2996r13.html from reflection.md
#   make                # also builds p2996r13.html from reflection.md

OUTDIR := .

ifeq ($(PAPER_RULE),)
include $(dir $(lastword $(MAKEFILE_LIST)))flat.mk
else
DEFAULT_FORMAT ?= html

paper_id := $(word 1,$(subst :, ,$(PAPER_RULE)))
paper_src := $(word 2,$(subst :, ,$(PAPER_RULE)))

.PHONY: all html pdf latex
all: $(DEFAULT_FORMAT)
html: $(paper_id).html
pdf: $(paper_id).pdf
latex: $(paper_id).latex

include $(dir $(lastword $(MAKEFILE_LIST)))base.mk

.PHONY: clean
clean:
	rm -f $(paper_id).html $(paper_id).pdf $(paper_id).latex

$(paper_id).html $(paper_id).pdf $(paper_id).latex: $(paper_src).md $(DEPS)
	$(PANDOC)
endif
