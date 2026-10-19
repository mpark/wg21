OUTDIR := ../actual
output := $(OUTDIR)/presentation.slides.html
no_document_output := $(OUTDIR)/no-document.slides.html
title_preview_markdown := $(OUTDIR)/title-preview.render.md
title_preview_output := $(OUTDIR)/title-preview.html

include ../../flat.mk

.PHONY: check
check:
	@$(MAKE) clean
	@$(MAKE) html
	@test ! -e $(output)
	@test ! -e $(no_document_output)
	@$(MAKE) slides
	@grep -Fq '<title>Slides Test</title>' $(output)
	@grep -Fq '<p class="subtitle">Presentation Subtitle</p>' $(output)
	@grep -Fq '<p class="author">Slide Author</p>' $(output)
	@grep -Fq '<span class="title-value">D1234R5 ' $(output)
	@grep -Fq 'href="https://wg21.link/P1234" class="document-link">Latest</a>' $(output)
	@grep -Fq 'href="https://wg21.link/P1234/status" class="document-link">Status</a>' $(output)
	@grep -Fq '<span class="title-label">Project:</span><span class="title-value">Programming Language C</span>' $(output)
	@grep -Fq '<span class="title-value">WG21</span>' $(output)
	@grep -Fq '&lt;<a href="mailto:slides@example.com">slides@example.com</a>&gt;' $(output)
	@grep -Fq 'class="title-info"' $(no_document_output)
	@! grep -Fq 'Document #:' $(no_document_output)
	@! grep -Fq 'Project:' $(no_document_output)
	@grep -Eq '<p class="date">[0-9]{4}-[0-9]{2}-[0-9]{2}</p>' $(output)
	@grep -Fq '<div class="reveal">' $(output)
	@grep -Fq 'data:image/vnd.microsoft.icon;base64,' $(output)
	@grep -Fq 'Reveal.initialize' $(output)
	@grep -Fq 'RevealHighlight' $(output)
	@grep -Fq "slideNumber: 'c/t'" $(output)
	@grep -Fq -- '--r-background-color: #fff;' $(output)
	@grep -Fq -- '--r-main-font: serif;' $(output)
	@! grep -Fq 'source-sans-pro' $(output)
	@grep -Fq '<section id="overview" class="title-slide slide level1">' $(output)
	@grep -Fq '<section id="shared-formatting" class="slide level2">' $(output)
	@grep -Fq '<section id="proposal" class="title-slide slide level1">' $(output)
	@grep -Fq '<aside class="notes">' $(output)
	@grep -Fq 'code span.kw {' $(output)
	@grep -Fq -- '--add-color: #006e28;' $(output)
	@grep -Fq '<span class="kw">match</span>' $(output)
	@grep -Fq '<em>value</em>' $(output)
	@grep -Fq '<code data-noescape data-line-numbers="1|2" data-ln-start-from="7" class="nohighlight hljs sourceCode cpp">' $(output)
	@grep -Fq '<code data-noescape data-line-numbers="1-2|3" class="nohighlight hljs sourceCode javascript">' $(output)
	@grep -Fq '<code data-noescape class="nohighlight sourceCode default">' $(output)
	@grep -Fq '<code data-noescape data-line-numbers data-ln-start-from="9" class="nohighlight hljs sourceCode default">' $(output)
	@grep -Fq '<code data-noescape data-line-numbers="1|2" data-ln-start-from="7" class="nohighlight hljs">' $(output)
	@grep -Fq '<section id="animated-code" class="slide level2" data-auto-animate data-auto-animate-duration="0.5">' $(output)
	@grep -Fq '<pre data-id="code-animation" class="sourceCode cpp">' $(output)
	@! grep -Eq '<(div|code)[^>]*data-id="code-animation"' $(output)
	@grep -Fq '<div class="add">' $(output)
	@grep -Fq '<del>old</del>' $(output)
	@grep -Fq '<ins>new</ins>' $(output)
	@grep -Fq 'href="https://eel.is/c++draft/basic.scope"' $(output)
	@grep -Fq 'href="https://eel.is/c++draft/basic.life"' $(output)
	@grep -Fq 'href="https://wg21.link/p2688r5"' $(output)
	@grep -Fq 'Pattern Matching:' $(output)
	@grep -Fq '<h1 class="unnumbered">References</h1>' $(output)
	@! grep -Fq 'class="self-link"' $(output)
	@grep -Fq '<div class="table-wrapper">' $(output)
	@grep -Fq '<table class="cmptable">' $(output)
	@grep -Fq 'id="pnum-1"' $(output)
	@grep -Fq 'id="note-1" class="note" data-num="1"' $(output)
	@! grep -Fq 'deps/revealjs' $(output)
	@pandoc fixtures/title-preview.md -o $(title_preview_markdown) --standalone \
		--filter ../../data/filters/render.py
	@pandoc $(title_preview_markdown) -o $(title_preview_output) \
		--data-dir=../../data -M data-dir=../../data -d slides -d formatting \
		-M revealjs-url=$(REVEALJS_DIR)
	@grep -Fq 'class="title-preview"' $(title_preview_output)
	@grep -Fq 'class="title-info"' $(title_preview_output)
	@grep -Fq '<span class="title-label">Project:</span><span class="title-value">Programming Language C++</span>' $(title_preview_output)
