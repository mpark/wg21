%.pdf: %.md
	pandoc template/header.yaml \
          $< \
          --filter pandoc-citeproc \
          --filter template/tony-table.py \
          --highlight-style=kate \
          --number-section \
          --syntax-definition template/cpp.xml \
          --syntax-definition template/diff.xml \
          --table-of-contents \
          --template template/wg21.latex \
          -o pdf/$@
