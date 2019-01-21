%.pdf: %.md
	pandoc template/header.yaml $< template/footer.md \
       --filter pandoc-citeproc \
       --filter template/diff.py \
       --filter template/tonytable.py \
       --highlight-style kate \
       --number-sections \
       --syntax-definition template/cpp.xml \
       --syntax-definition template/diff.xml \
       --template template/wg21.latex \
       --output pdf/$@
