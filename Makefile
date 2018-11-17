%.pdf: %.pandoc
	pandoc template/header.yaml \
         $< \
         --filter pandoc-citeproc \
         --filter template/tony-table.py \
         --highlight-style kate \
         --number-sections \
         --syntax-definition template/cpp.xml \
         --syntax-definition template/diff.xml \
         --template template/wg21.latex \
         --output pdf/$@

%.md: %.pandoc
	pandoc template/header.yaml \
         $< \
         --filter pandoc-citeproc \
         --filter template/tony-table.py \
         --to gfm \
         --output github/$@
