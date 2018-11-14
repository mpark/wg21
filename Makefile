%.pdf: %.md
	pandoc template/header.yaml \
          $< \
          --number-section \
          --highlight-style=kate \
          --filter pandoc-citeproc \
          --filter template/tony-table.py \
          --syntax-definition template/cpp.xml \
          --syntax-definition template/diff.xml \
          --template template/wg21.latex \
          --toc \
          -o pdf/$@
