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

%.html: %.md
	pandoc template/header.yaml $< template/footer.md \
       --self-contained \
       --filter pandoc-citeproc \
       --filter template/diff.py \
       --filter template/tonytable.py \
       --highlight-style kate \
       --number-sections \
       --syntax-definition template/cpp.xml \
       --syntax-definition template/diff.xml \
       --template template/wg21.html \
       --table-of-contents \
       --output html/$@
