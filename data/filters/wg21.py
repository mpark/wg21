#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2022
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

import datetime
import os.path
import panflute as pf
import re

stable_names = {}
refs = {}
headers = {}

def wrap_elem(opening, elem, closing):
    if isinstance(elem, pf.Div):
        if elem.content and isinstance(elem.content[0], pf.Para):
            elem.content[0].content.insert(0, opening)
        else:
            elem.content.insert(0, pf.Plain(opening))
        if elem.content and isinstance(elem.content[-1], pf.Para):
            elem.content[-1].content.append(closing)
        else:
            elem.content.append(pf.Plain(closing))
    elif isinstance(elem, pf.Span):
        elem.content.insert(0, opening)
        elem.content.append(closing)

def prepare(doc):
    if doc.get_metadata('date') == 'today':
        doc.metadata['date'] = datetime.date.today().isoformat()

    document = doc.get_metadata('document')
    number = re.match("[PD]([0-9]+)R[0-9]+", document.upper())
    if number is not None:
        doc.metadata['number'] = number.group(1)
    else:
        pf.debug('mpark/wg21: document ', document, 'is in an unrecognized format')
    doc.metadata['pagetitle'] = pf.convert_text(
        pf.Plain(*doc.metadata['title'].content),
        input_format='panflute',
        output_format='markdown')

    datadir = doc.get_metadata('datadir')

    with open(os.path.join(datadir, 'annex-f'), 'r') as f:
        stable_names.update(line.split(maxsplit=1) for line in f)

    def highlighting(output_format):
        return pf.convert_text(
            '`-`{.default}',
            output_format=output_format,
            extra_args=[
              '--highlight-style', os.path.join(datadir, 'syntax', 'wg21.theme'),
              '--template', os.path.join(datadir, 'templates', 'highlighting'),
              '--metadata', 'title="-"',
            ])

    doc.metadata['highlighting-macros'] = pf.MetaBlocks(
        pf.RawBlock(highlighting('latex'), 'latex'))
    doc.metadata['highlighting-css'] = pf.MetaBlocks(
        pf.RawBlock(highlighting('html'), 'html'))

def divspan(elem, doc):
    """
    Non-code diffs: `add` and `rm` are classes that can be added to
    a `Div` or a `Span`. `add` colors the text with `addcolor` and
    `rm` colors the text `rmcolor`. For `Span`s, `add` underlines
    and `rm` strikes out the text.

    # Example

    ## `Div`

    Unchanged portion

    ::: add
    New paragraph

    > Quotes

    More new paragraphs
    :::

    ## `Span`

    > The return type is `decltype(`_e_(`m`)`)` [for the first form]{.add}.
    """

    def _color(html_color):
        wrap_elem(
            pf.RawInline(f'{{\\color[HTML]{{{html_color}}}', 'latex'),
            elem,
            pf.RawInline('}', 'latex'))
        elem.attributes['style'] = f'color: #{html_color}'

    def _nonnormative(name):
        wrap_elem(
            pf.Span(pf.Str('[ '), pf.Emph(pf.Str(f'{name.title()}:')), pf.Space),
            elem,
            pf.Span(pf.Str(' — '), pf.Emph(pf.Str(f'end {name.lower()}')), pf.Str(' ]')))

    def _diff(color, latex_tag, html_tag):
        if isinstance(elem, pf.Span):
            def protect_code(elem, doc):
                if isinstance(elem, pf.Code):
                    return pf.Span(pf.RawInline('\\mbox{', 'latex'),
                                   elem,
                                   pf.RawInline('}', 'latex'))
            elem.walk(protect_code)
            wrap_elem(
                pf.RawInline(f'\\{latex_tag}{{', 'latex'),
                elem,
                pf.RawInline('}', 'latex'))
            wrap_elem(
                pf.RawInline(f'<{html_tag}>', 'html'),
                elem,
                pf.RawInline(f'</{html_tag}>', 'html'))
        _color(doc.get_metadata(color))

    def pnum():
        num = pf.stringify(elem)

        if '.' in num:
            num = f'({num})'

        if doc.format == 'latex':
            return pf.RawInline(f'\\pnum{{{num}}}', 'latex')
        elif doc.format == 'html':
            return pf.Span(
                pf.RawInline(f'<a class="marginalized">{num}</a>', 'html'),
                classes=['marginalizedparent'])

        return pf.Superscript(pf.Str(num))

    def example(): _nonnormative('example')
    def note():    _nonnormative('note')
    def ednote():
        wrap_elem(pf.Str("[ Editor's note: "), elem, pf.Str(' ]'))
        _color('0000ff')
    def draftnote():
        audience = elem.attributes.get('audience')
        text = 'Drafting note' + (f' for {audience}' if audience is not None else '')
        wrap_elem(pf.Str(f'[ {text}: '), elem, pf.Str(' ]'))
        _color('0000ff')

    def add(): _diff('addcolor', 'uline', 'ins')
    def rm():  _diff('rmcolor', 'sout', 'del')

    if not any(isinstance(elem, cls) for cls in [pf.Div, pf.Span]):
        return None

    if 'pnum' in elem.classes and isinstance(elem, pf.Span):
        return pnum()

    if 'sref' in elem.classes and isinstance(elem, pf.Span):
        target = pf.stringify(elem)
        name = target.split('#')[0]
        number = stable_names.get(name)
        link = pf.Link(
            pf.Str(f'[{target}]'),
            url=f'https://wg21.link/{target}')
        if number is not None:
            return pf.Span(link) if 'unnumbered' in elem.classes else pf.Span(pf.Str(number), pf.Space(), link)
        else:
            pf.debug('mpark/wg21: stable name', name, 'not found')
            return link

    note_cls = next(iter(cls for cls in elem.classes if cls in {'example', 'note', 'ednote', 'draftnote'}), None)
    if note_cls == 'example':  example()
    elif note_cls == 'note':   note()
    elif note_cls == 'ednote': ednote(); return
    elif note_cls == 'draftnote': draftnote(); return

    diff_cls = next(iter(cls for cls in elem.classes if cls in {'add', 'rm'}), None)
    if diff_cls == 'add':  add()
    elif diff_cls == 'rm': rm()

def cmptable(table, doc):
    """
    Comparison Tables: Code blocks are the first-class entities that get added
    to the table. Each code block is pushed onto the current row.
    A horizontal rule (`---`) is used to move to the next row.

    In the first row, the last header (if any) leading upto the i'th
    code block is the header for the i'th column of the table.

    The last block quote (if any) is used as the caption.

    # Example

    ::: cmptable

    > compare inspect of unconstrained and constrained types

    ### Before
    ```cpp
    std::visit([&](auto&& x) {
      strm << "got auto: " << x;
    }, v);
    ```

    ### After
    ```cpp
    inspect (v) {
      <auto> x: strm << "got auto: " << x;
    }
    ```

    ---

    ```cpp
    std::visit([&](auto&& x) {
      using X = std::remove_cvref_t<decltype(x)>;
      if constexpr (C1<X>()) {
        strm << "got C1: " << x;
      } else if constexpr (C2<X>()) {
        strm << "got C2: " << x;
      }
    }, v);
    ```

    ```cpp
    inspect (v) {
      <C1> c1: strm << "got C1: " << c1;
      <C2> c2: strm << "got C2: " << c2;
    }
    ```

    :::

    # Generates

    Table: compare inspect of unconstrained and constrained types

    +------------------------------------------------+---------------------------------------------+
    | __Before__                                     | __After__                                   |
    +================================================+=============================================+
    | ```cpp                                         | ```cpp                                      |
    | std::visit([&](auto&& x) {                     | inspect (v) {                               |
    |   strm << "got auto: " << x;                   |   <auto> x: strm << "got auto: " << x;      |
    | }, v);                                         | }                                           |
    |                                                | ```                                         |
    +------------------------------------------------+---------------------------------------------+
    | std::visit([&](auto&& x) {                     | ```cpp                                      |
    |   using X = std::remove_cvref_t<decltype(x)>;  | inspect (v) {                               |
    |   if constexpr (C1<X>()) {                     |   <C1> c1: strm << "got C1: " << c1;        |
    |     strm << "got C1: " << x;                   |   <C2> c2: strm << "got C2: " << c2;        |
    |   } else if constexpr (C2<X>()) {              | }                                           |
    |     strm << "got C2: " << x;                   | ```                                         |
    |   }                                            |                                             |
    | }, v);                                         |                                             |
    +------------------------------------------------+---------------------------------------------+
    """

    if not isinstance(table, pf.Div):
        return None

    if not any(cls in table.classes for cls in ['cmptable', 'tonytable']):
        return None

    rows = []
    kwargs = {}

    headers = []
    widths = []
    examples = []

    header = pf.Null()
    caption = None
    width = 'ColWidthDefault'

    first_row = True
    table.content.append(pf.HorizontalRule())

    def warn(elem):
        pf.debug('mpark/wg21:', type(elem), pf.stringify(elem, newlines=False),
                 'in a comparison table is ignored')

    for elem in table.content:
        if isinstance(elem, pf.Header):
            if not isinstance(header, pf.Null):
                warn(header)

            if first_row:
                header = pf.Plain(*elem.content)
                width = (float(elem.attributes['width'])
                         if 'width' in elem.attributes else
                         'ColWidthDefault')
            else:
                warn(elem)
        elif isinstance(elem, pf.BlockQuote):
            if caption is not None:
                warn(caption)

            caption = pf.Caption(elem)
        elif isinstance(elem, pf.CodeBlock):
            if first_row:
                headers.append(header)
                widths.append(width)

                header = pf.Null()
                width = 'ColWidthDefault'

            codeblock = pf.Div(elem)
            wrap_elem(
                pf.RawInline('\\begin{minipage}[t]{\\linewidth}\\raggedright', 'latex'),
                codeblock,
                pf.RawInline('\\end{minipage}', 'latex'));

            examples.append(codeblock)
        elif isinstance(elem, pf.HorizontalRule) and examples:
            first_row = False

            rows.append(pf.TableRow(*[pf.TableCell(example) for example in examples]))
            examples = []
        else:
            warn(elem)

    if not all(isinstance(header, pf.Null) for header in headers):
        kwargs['head'] = pf.TableHead(pf.TableRow(*[pf.TableCell(header) for header in headers]))

    kwargs['caption'] = pf.Caption() if caption is None else caption
    kwargs['colspec'] = [('AlignDefault', w) for w in widths]
    return pf.Table(pf.TableBody(*rows), **kwargs)

def header(elem, doc):
    if not isinstance(elem, pf.Header):
        return None

    if elem.identifier == 'bibliography':
        elem.classes.remove('unnumbered')

    url = f'#{elem.identifier}'
    headers[url] = pf.stringify(elem)

    elem.content.append(pf.Link(url=url, classes=['self-link']))

def table(elem, doc):
    if not isinstance(elem, pf.Table):
        return None

    def header(elem, doc):
        if not isinstance(elem, pf.Plain):
            return None

        return pf.Div(
            pf.Plain(pf.RawInline('\\centering\\arraybackslash', 'latex'),
                     pf.Strong(*elem.content)),
            attributes={'style': 'text-align:center'})

    if elem.head is not None:
        elem.head.walk(header)

def collect_refs(elem, doc):
    if not (isinstance(elem, pf.Div) and elem.identifier.startswith('ref-')):
        return None

    def find_urls(elem, doc):
        if isinstance(elem, pf.Link):
            urls.append(elem.url)
        return None

    urls = []
    elem.walk(find_urls)
    if len(urls) == 1:
        refs[f'#{elem.identifier}'] = urls[0]

def citation_link(elem, doc):
    if not (isinstance(elem, pf.Link) and elem.url.startswith("#ref-")):
        return None

    url = refs.get(elem.url)
    if url is None:
        return None

    elem.url = url
    return elem

def automatic_header_link(elem, doc):
    if not (isinstance(elem, pf.Link) and
           elem.url.startswith('#') and
           ('self-link' not in elem.classes) and
           pf.stringify(elem) == ""):
        return None

    if (header_text := headers.get(elem.url)) is None:
        pf.debug('mpark/wg21: cannot find automatic text for link to:', elem.url)
        return None

    return pf.Link(pf.Str(header_text), url=elem.url)

class CodeElems:
    """
    High-level description of embedded markdown handling:

      1. Collect relevant code elements
      2. Pick a unique placeholder prefix
      3. Replace embedded markdown fragment with a placeholder.
         Same fragments are assigned the same placeholder.
      4. All of the fragments are batched and converted in a single
         `convert_text` invocation, and stored in `converted_fragments`.
      5. All of the code elements are batched and converted in a single
         `convert_text` invocation.
      6. Restore the embedded markdown fragments into the batch converted
         code text, by doing a recursive regex substitution with
         `converted_fragments` as the look-up table.
      7. Split the batch converted code text into individual elements, and
         update the code elements with the fully processed elements.
    """
    code_elems = []
    code_elems_iter = None

    # Code elements for which embedded markdown is allowed
    embedded_md_classes = ['cpp', 'default', 'diff', 'nasm', 'rust']

    placeholder_prefix = None

    # Unique list of fragments, kept track in `fragment_idx`.
    fragments = []

    # Mapping from embedded md fragment to its index within `fragments`
    fragment_idx = {}
    
    converted_fragments = None

    @staticmethod
    def init(elem, doc):
        if isinstance(elem, pf.Header) and doc.format == 'latex':
            elem.walk(lambda elem, doc:
                elem.classes.append('raw')
                if any(isinstance(elem, cls) for cls in [pf.Code, pf.CodeBlock])
                else None)

        # Mark code elements within colored divspan as default.
        if any(isinstance(elem, cls) for cls in [pf.Div, pf.Span]) and \
           any(cls in elem.classes for cls in ['add', 'rm', 'ednote', 'draftnote']):
            elem.walk(lambda elem, doc:
                elem.classes.insert(0, 'default')
                if any(isinstance(elem, cls) for cls in [pf.Code, pf.CodeBlock])
                else None)

        if not any(isinstance(elem, cls) for cls in [pf.Code, pf.CodeBlock]):
            return None

        # As `walk` performs post-order traversal, this is
        # guaranteed to run before the 'raw' code path.
        if not elem.classes:
            if isinstance(elem, pf.Code):
                cls = doc.get_metadata('highlighting.inline-code', 'default')
            elif isinstance(elem, pf.CodeBlock):
                cls = doc.get_metadata('highlighting.code-block', 'default')
            elem.classes.append(cls)


    @staticmethod
    def collect(elem, doc):
        if not any(isinstance(elem, cls) for cls in [pf.Code, pf.CodeBlock]):
            return None

        if 'raw' in elem.classes or not any(cls in elem.classes for cls in CodeElems.embedded_md_classes):
            return None

        CodeElems.code_elems.append(elem)

    @staticmethod
    def update(elem, doc):
        if not any(isinstance(elem, cls) for cls in [pf.Code, pf.CodeBlock]):
            return None

        if 'raw' in elem.classes or not any(cls in elem.classes for cls in CodeElems.embedded_md_classes):
            return None

        code_elem = next(CodeElems.code_elems_iter)
        result = None
        if isinstance(elem, pf.Code):
            result = pf.RawInline(code_elem, doc.format)
        elif isinstance(elem, pf.CodeBlock):
            result = pf.RawBlock(code_elem, doc.format)

        if 'diff' not in elem.classes:
            return result

        # For HTML, this is handled via CSS in `data/templates/wg21.html`.
        command = '\\renewcommand{{\\{}}}[1]{{\\textcolor[HTML]{{{}}}{{#1}}}}'

        uc = command.format('NormalTok', doc.get_metadata('uccolor'))
        add = command.format('VariableTok', doc.get_metadata('addcolor'))
        rm = command.format('StringTok', doc.get_metadata('rmcolor'))

        if isinstance(elem, pf.Code):
            return pf.Span(
                pf.RawInline(uc, 'latex'),
                pf.RawInline(add, 'latex'),
                pf.RawInline(rm, 'latex'),
                result)
        elif isinstance(elem, pf.CodeBlock):
            return pf.Div(
                pf.RawBlock('{', 'latex'),
                pf.RawBlock(uc, 'latex'),
                pf.RawBlock(add, 'latex'),
                pf.RawBlock(rm, 'latex'),
                result,
                pf.RawBlock('}', 'latex'))

    @staticmethod
    def _compute_unique_placeholder(texts):
        import uuid
        while True:
             placeholder = f'X{uuid.uuid4().hex.upper()}X'
             if not any(placeholder in text for text in texts):
                 return placeholder

    @staticmethod
    def _convert_fragments(fragments, doc):
        separator = CodeElems._compute_unique_placeholder(fragments)
        # -smart to disable Pandoc smart extension
        pf_fragments = (
            pf.Plain(*fragment.content).walk(CodeElems.init, doc).walk(divspan, doc)
            for fragment
            in pf.convert_text(f'\n\n{separator}\n\n'.join(fragments), input_format='markdown-smart'))
        text = pf.convert_text(
            pf_fragments,
            input_format='panflute',
            output_format=doc.format,
            extra_args=[
                '--syntax-definition',
                os.path.join(doc.get_metadata('datadir'), 'syntax', 'isocpp.xml'),
                '--wrap',
                'none'])

        if doc.format == 'latex':
            # The normal text mode such as "template<class" gets translated
            # to "template\textless class" rather than "text\textless{}class".
            text = text.replace(r'\textless ', r'\textless{}') \
                       .replace(r'\textgreater ', r'\textgreater{}') \
                       .replace(r'\textasciitilde ', r'\textasciitilde{}') \
                       .replace(r'\textbackslash ', r'\textbackslash{}') \
                       .replace(r'\textbar ', r'\textbar{}') \
                       .replace(r'\textquotesingle ', r'\textquotesingle{}')

        return text.split('{1}{0}{1}'.format(separator, '\n\n' if doc.format == 'latex' else '\n'))

    @classmethod
    def _store_fragment(cls, fragment):
        if (idx := cls.fragment_idx.get(fragment)) is None:
            idx = len(cls.fragments)
            cls.fragments.append(fragment)
            cls.fragment_idx[fragment] = idx

        return f'{cls.placeholder_prefix}{idx}X'

    @classmethod
    def _process_fragment(cls, text, i, closing, wrap=lambda fragment: fragment):
        """
        Returns the placeholder for the parsed embedded Markdown region and
        the index where parsing should continue.

        For @@FOO @BAR@ BAZ@@, store:
          PH1 -> BAR
          PH2 -> FOO PH1 BAZ
        The outer @@...@@ parse returns PH2, and the inner @...@ parse
        returns PH1.
        """
        pieces = []
        start = i

        while i < len(text):
            if text[i] == '\n':
                return None

            if text.startswith(closing, i):
                pieces.append(text[start:i])
                placeholder = cls._store_fragment(wrap(''.join(pieces)))
                return placeholder, i + len(closing)

            result = None

            if closing == '@@' and text.startswith('@', i):
                result = cls._process_fragment(text, i + 1, '@')
            elif text.startswith('$', i):
                result = cls._process_fragment(
                    text, i + 1, '$', lambda fragment: f'*{fragment}*')

            if result is not None:
                pieces.append(text[start:i])
                placeholder, i = result
                pieces.append(placeholder)
                start = i
                continue

            i += 1

        return None

    @classmethod
    def _replace_fragments_with_placeholders(cls, text):
        pieces = []
        start = 0
        i = 0

        while i < len(text):
            result = None
            if text.startswith('@@', i):
                result = cls._process_fragment(text, i + 2, '@@')
            elif text.startswith('@', i):
                result = cls._process_fragment(text, i + 1, '@')
            elif text.startswith('$', i):
                result = cls._process_fragment(
                    text, i + 1, '$', lambda fragment: f'*{fragment}*')

            if result is not None:
                pieces.append(text[start:i])
                placeholder, i = result
                pieces.append(placeholder)
                start = i
                continue

            i += 1

        pieces.append(text[start:])
        return ''.join(pieces)

    @classmethod
    def run(cls, doc):
        doc.walk(cls.init)
        doc.walk(cls.collect)
        if not cls.code_elems:
            return

        cls.placeholder_prefix = cls._compute_unique_placeholder(elem.text for elem in cls.code_elems)
        for elem in cls.code_elems:
            elem.text = cls._replace_fragments_with_placeholders(elem.text)

        cls.converted_fragments = cls._convert_fragments(cls.fragments, doc)

        def intersperse(lst, item):
            result = [item] * (len(lst) * 2 - 1)
            result[0::2] = lst
            return result

        # Intersperse the separator and batch convert all of the code elements at once.
        separator = cls._compute_unique_placeholder(elem.text for elem in cls.code_elems)
        text = pf.convert_text(
            intersperse(
                [pf.Plain(elem) if isinstance(elem, pf.Code) else elem for elem in cls.code_elems],
                pf.Plain(pf.RawInline(separator, doc.format))),
            input_format='panflute',
            output_format=doc.format,
            extra_args=[
                '--syntax-definition',
                os.path.join(doc.get_metadata('datadir'), 'syntax', 'isocpp.xml')])

        placeholder_re = re.compile(fr'{cls.placeholder_prefix}(\d+)X')
        def restore_fragments(text):
            return placeholder_re.sub(
                lambda match: restore_fragments(cls.converted_fragments[int(match.group(1))]),
                text)

        text = restore_fragments(text)

        # Workaround for https://github.com/jgm/skylighting/issues/91.
        if doc.format == 'latex':
            text = text.replace('<', '\\textless{}') \
                       .replace('>', '\\textgreater{}')

        code_elems = text.split('{1}{0}{1}'.format(separator, '\n' if doc.format == 'latex' else ''))

        assert(len(cls.code_elems) == len(code_elems))

        cls.code_elems = code_elems
        cls.code_elems_iter = iter(cls.code_elems)
        doc.walk(cls.update)

def finalize(doc):
    CodeElems.run(doc)

if __name__ == '__main__':
  pf.run_filters([
      divspan,
      cmptable,
      # after `cmptable` because...
      header, # doesn't apply to the "headers" in comparison table.
      table,  # also applies to tables generated by `cmptable`.
      *[collect_refs, citation_link],
      automatic_header_link, # needs to be after `header`
  ], prepare, finalize)
