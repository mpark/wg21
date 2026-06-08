#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2022
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

import os.path
import json
import panflute as pf
import re

refs = {}
srefs = {}
headers = {}
document_pattern = r"[PD]([0-9]+)R[0-9]+"

def prepend_elem(elem, *prefix):
    assert(all(isinstance(e, pf.Inline) for e in prefix))

    if elem.content and isinstance(elem.content[0], pf.Para):
        elem.content[0].content[0:0] = prefix
    elif elem.content and isinstance(elem.content[0], pf.Plain):
        elem.content[0] = pf.Para(*prefix, *elem.content[0].content)
    else:
        elem.content.insert(0, pf.Plain(*prefix))

def append_elem(elem, *suffix):
    assert(all(isinstance(e, pf.Inline) for e in suffix))

    if elem.content and isinstance(elem.content[-1], pf.Para):
        elem.content[-1].content.extend(suffix)
    elif elem.content and isinstance(elem.content[-1], pf.Plain):
        elem.content[-1] = pf.Para(*elem.content[-1].content, *suffix)
    else:
        elem.content.append(pf.Plain(*suffix))

def wrap_elem(opening, elem, closing):
    if isinstance(elem, pf.Div):
        prepend_elem(elem, opening)
        append_elem(elem, closing)
    elif isinstance(elem, pf.Span):
        elem.content.insert(0, opening)
        elem.content.append(closing)

def protect_code(elem, doc):
    if isinstance(elem, pf.Code):
        return pf.Span(pf.RawInline(r'\mbox{', 'latex'),
                       elem,
                       pf.RawInline('}', 'latex'))

def convert_fragments(fragments, input_format):
    """
    Converts a list of fragment texts into panflute elements
    in a single invocation of `pf.convert_text`.

    A fragment is essentially a piece of raw Markdown text that we need to parse
    ourselves. Examples are the "new text" portion of [old text](new text){.sub}
    syntax, and embedded Markdown in Code elements within @.
    """
    # This separates the fragments structurally in a list, and
    # injects an empty span []{} in front of the fragment such that a fragment
    # that starts with a - (dash) doesn't get interpreted as a nested list.
    result = pf.convert_text(
               '\n'.join(f'- []{{}}{fragment}' for fragment in fragments),
               input_format=input_format,
               output_format='panflute')
    assert(len(result) == 1)
    lst = result[0]
    assert(isinstance(lst, pf.BulletList))
    assert(len(lst.content) == len(fragments))
    process_subs(lst, input_format)
    for item in lst.content:
        assert(len(item.content) == 1)
        plain = item.content[0]
        assert(isinstance(plain, pf.Plain))
        marker = plain.content.pop(0)
        assert(isinstance(marker, pf.Span) and not marker.content)
        yield plain

def process_subs(elem, input_format):
    """
    Processes [old text](new text){.sub} elements under a given element
    by essentially producing [old text]{.rm}[new text]{.add}.

    The complexity is in the fact that (new text) is interpreted as a URL,
    so we unquote/unescape and treat it as a fragment.
    """
    adds = []
    fragments = []
    def subs(elem, doc):
        if not (isinstance(elem, pf.Link) and 'sub' in elem.classes):
            return None

        classes = [c for c in elem.classes if c != 'sub']
        rm = pf.Span(*elem.content, classes=['rm']+classes)
        add = pf.Span(classes=['add']+classes)
        adds.append(add)

        import html, urllib.parse
        fragments.append(html.unescape(urllib.parse.unquote(elem.url)))
        return pf.Span(rm, add)

    elem.walk(subs)
    assert(len(adds) == len(fragments))
    if adds:
        for add, item in zip(adds, convert_fragments(fragments, input_format)):
            add.content = item.content

def prepare(doc):
    if doc.get_metadata('date') == 'today':
        import datetime
        doc.metadata['date'] = datetime.date.today().isoformat()

    document = doc.get_metadata('document')
    number = re.match(document_pattern, document.upper())
    if number is not None:
        doc.metadata['number'] = number.group(1)
    else:
        pf.debug(f"""[WARNING] mpark/wg21: {document} is an unrecognized format; expected "{document_pattern}".
            This means that [Latest] and [Status] links will be missing.""")

    title = pf.convert_text(
        pf.Plain(*doc.metadata['title'].content),
        input_format='panflute',
        output_format='markdown')
    doc.metadata['pagetitle'] = title   # HTML
    doc.metadata['title-meta'] = title  # PDF

    datadir = doc.get_metadata('datadir')
    with open(os.path.join(datadir, 'srefs.json'), 'r') as f:
        srefs.update(json.load(f))

    def highlighting(output_format):
        return pf.convert_text(
            '`-`{.default}',
            input_format='markdown',
            output_format=output_format,
            extra_args=[
              '--syntax-highlighting', os.path.join(datadir, 'syntax', 'wg21.theme'),
              '--template', os.path.join(datadir, 'templates', 'highlighting'),
              '--metadata', 'title="-"',
            ])

    doc.metadata['highlighting-macros'] = pf.MetaBlocks(
        pf.RawBlock(highlighting('latex'), 'latex'))
    doc.metadata['highlighting-css'] = pf.MetaBlocks(
        pf.RawBlock(highlighting('html'), 'html'))

    process_subs(doc, doc.get_metadata('from'))

def strikeout(elem, doc):
    # In Pandoc 3.x, strikeouts use the \st from soul package.
    # This requires that code elements within has to be protected via mbox.
    # Pandoc handles this manually, but since we handle the code elements
    # rendering manually, we need to inject the protection manually as well.
    if doc.format == 'latex' and isinstance(elem, pf.Strikeout):
        elem.walk(protect_code)

def sref(elem, doc):
    if not (isinstance(elem, (pf.Link, pf.Span)) and 'sref' in elem.classes):
        return None

    target = pf.stringify(elem)
    # Support paragraph numbers: e.g. [basic.scope.scope#2.1]{.sref}
    name, _, pnum = target.partition('#')
    # Also support paragraph numbers as a suffix: e.g. [basic.scope.scope]/2.1
    # If the explicit paragraph number is specified, it takes precedence over
    # the suffix. e.g. [basic.life#1]{.sref}/2, the /2 is left as plain text.
    if (
        not pnum and
        isinstance(elem.next, pf.Str) and
        (match := re.match(r'/([0-9]+(?:\.[0-9]+)*)(.*)',
                           elem.next.text))
    ):
        pnum, elem.next.text = match.groups()
        target = f'{name}#{pnum}'

    link = pf.Link(
        pf.Str(f'[{name}]' + (f'/{pnum}' if pnum else '')),
        url=f'https://eel.is/c++draft/{target}')
    info = srefs.get(name)
    if info is None:
        pf.debug(f"""[WARNING] mpark/wg21: stable name {name} not found.
            Tip: run `make update` to refresh the local databases, including stable names""")
        return link

    number, title = info
    link.title = f'{number} {title}'
    result = pf.Span()
    if 'unnumbered' not in elem.classes:
        result.content.append(pf.Str(number))
        result.content.append(pf.Space())
    if 'title' in elem.classes:
        result.content.append(pf.Str(title))
        result.content.append(pf.Space())
    if result.content:
        result.content.append(link)
        return result

    return link

def wording(elem, doc):
    if not (isinstance(elem, pf.Div) and 'wording' in elem.classes):
        return None

    def get_list_type(elem):
        if isinstance(elem, pf.OrderedList):
            if elem.style == 'DefaultStyle' and elem.delimiter == 'DefaultDelim':
                return '#.'
            elif elem.style == 'Decimal' and elem.delimiter == 'Period':
                return '1.'
            elif elem.style == 'LowerAlpha' and elem.delimiter == 'OneParen' and elem.start == 24:
                return 'x)'
            return None
        elif isinstance(elem, pf.BulletList):
            return '-'
        return None

    def process_list(elem, parents, start):
        list_type = get_list_type(elem)
        if list_type is None:
            return None

        # '#.' is only supported at the top-level, '-' is only supported nested.
        if list_type == '#.' and parents:
            return None

        if list_type == '-' and not parents:
            return None

        if list_type == '1.':
            start = elem.start - 1

        for item in elem.content:
            number = parents
            if list_type == 'x)':
                number += ('x',)
            else:
                start += 1
                number += (start,)

            process_block(item, number)
            pnum = pf.Span(pf.Str('.'.join(map(str, number))), classes=['pnum'])
            prepend_elem(item, pnum, pf.Space())

        result = []
        if not parents:
            result.extend(block for item in elem.content for block in item.content)
        elif isinstance(elem, pf.OrderedList):
            result.append(pf.BulletList(*elem.content))
        else:
            result.append(elem)

        return start, result

    def process_block(elem, parents=(), start=0):
        content = []
        for block in elem.content:
            result = process_list(block, parents, start)
            if result is not None:
                start, blocks = result
                content.extend(blocks)
                continue
            if isinstance(block, pf.Div):
                start = process_block(block, parents, start)
            content.append(block)
        elem.content = content
        return start

    process_block(elem)
    return elem

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
            pf.Span(pf.Str('[ '), pf.Emph(pf.Str(f'{name.title()}:')), pf.Space()),
            elem,
            pf.Span(pf.Str(' — '), pf.Emph(pf.Str(f'end {name.lower()}')), pf.Str(' ]')))

    def _diff(color, latex_tag, html_tag):
        if isinstance(elem, pf.Span):
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

    # We need to stick to using 'uline' and 'sout' from the ulem package rather
    # than migrating to the soul package like Pandoc 3.x specifically for cases
    # where we want to strikeout/underline **within** a highlighted code block.
    # We could use the soul package for other cases, but keeping it consistent
    # seems simpler at least for now.
    def add(): _diff('addcolor', 'uline', 'ins')
    def rm():  _diff('rmcolor', 'sout', 'del')

    if not isinstance(elem, (pf.Div, pf.Span)):
        return None

    if 'pnum' in elem.classes and isinstance(elem, pf.Span):
        return pnum()

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

    if not any(c in {'cmptable', 'tonytable'} for c in table.classes):
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
        pf.debug('[WARNING] mpark/wg21:', type(elem), pf.stringify(elem, newlines=False),
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

def caption(elem, doc):
    # Code elements in table captions need to be protected.
    # See https://github.com/jgm/pandoc/pull/11139
    if doc.format == 'latex' and isinstance(elem, pf.Caption):
        elem.walk(lambda e, _:
            pf.Span(pf.RawInline(r'\protect', 'latex'), e)
            if isinstance(e, pf.Code)
            else None)

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
        pf.debug('[WARNING] mpark/wg21: cannot find automatic text for link to:', elem.url)
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
    # Code elements for which embedded markdown is allowed
    embedded_md_classes = {'cpp', 'default', 'diff', 'nasm', 'rust'}

    placeholder_prefix = None

    # Unique list of fragments, kept track in `fragment_idx`.
    fragments = []

    # Mapping from embedded md fragment to its index within `fragments`
    fragment_idx = {}
    
    @staticmethod
    def init(elem, doc):
        if isinstance(elem, pf.Header) and doc.format == 'latex':
            elem.walk(lambda elem, _:
                elem.classes.append('raw')
                if isinstance(elem, (pf.Code, pf.CodeBlock))
                else None)

        # Mark code elements within colored divspan as default.
        if isinstance(elem, (pf.Div, pf.Span)) and \
           any(c in {'add', 'rm', 'ednote', 'draftnote'} for c in elem.classes):
            elem.walk(lambda elem, _:
                elem.classes.insert(0, 'default')
                if isinstance(elem, (pf.Code, pf.CodeBlock))
                else None)

        if not isinstance(elem, (pf.Code, pf.CodeBlock)):
            return None

        # As `walk` performs post-order traversal, this is
        # guaranteed to run before the 'raw' code path.
        if not elem.classes:
            if isinstance(elem, pf.Code):
                c = doc.get_metadata('highlighting.inline-code', 'cpp')
            elif isinstance(elem, pf.CodeBlock):
                c = doc.get_metadata('highlighting.code-block', 'default')
            elem.classes.append(c)

    @staticmethod
    def _compute_unique_placeholder(texts):
        import uuid
        while True:
             placeholder = f'X{uuid.uuid4().hex.upper()}X'
             if not any(placeholder in text for text in texts):
                 return placeholder

    @staticmethod
    def _convert_blocks(blocks, token, doc):
        def intersperse(lst, item):
            result = [item] * (len(lst) * 2 - 1)
            result[0::2] = lst
            return result

        text = pf.convert_text(
            intersperse(blocks, pf.Plain(pf.RawInline(token, doc.format))),
            input_format='panflute',
            output_format=doc.format,
            extra_args=[
                '--syntax-definition',
                os.path.join(doc.get_metadata('datadir'), 'syntax', 'isocpp.xml'),
                '--wrap', 'none'])

        if doc.format == 'latex':
            # The normal text mode such as "template<class" gets translated
            # to "template\textless class" rather than "text\textless{}class".
            text = text.replace(r'\textless ', r'\textless{}') \
                       .replace(r'\textgreater ', r'\textgreater{}') \
                       .replace(r'\textasciitilde ', r'\textasciitilde{}') \
                       .replace(r'\textbackslash ', r'\textbackslash{}') \
                       .replace(r'\textbar ', r'\textbar{}') \
                       .replace(r'\textquotesingle ', r'\textquotesingle{}')

        sep = f'\n\n{token}\n\n' if doc.format == 'latex' else f'\n{token}\n'
        return text, sep

    @classmethod
    def _convert_fragments(cls, fragments, doc):
        if not fragments:
            return []

        blocks = [
            plain.walk(divspan, doc).walk(CodeElems.init, doc)
            # -raw_html to avoid <T> in foo<T> to be interpreted as an HTML tag.
            # -smart to avoid things like ... to get transformed into \dots
            for plain in convert_fragments(
                fragments, f"{doc.get_metadata('from')}-raw_html-smart")
        ]
        token = cls._compute_unique_placeholder(fragments)
        text, sep = cls._convert_blocks(blocks, token, doc)
        result = text.split(sep)
        assert(len(result) == len(fragments))
        return result

    @classmethod
    def _store_fragment(cls, fragment):
        if (idx := cls.fragment_idx.get(fragment)) is None:
            idx = len(cls.fragments)
            cls.fragments.append(fragment)
            cls.fragment_idx[fragment] = idx

        # Spaces are added here to make the syntax highlighter parse properly.
        # For example, given something like `constexpr$~opt~$`, the constexpr
        # keyword will not be highlighted properly without the spaces.
        return f' {cls.placeholder_prefix}{idx} '

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

        elems = []
        containers = []
        def code(elem, doc):
            if (
                isinstance(elem, (pf.Code, pf.CodeBlock)) and
                'raw' not in elem.classes and
                any(c in cls.embedded_md_classes for c in elem.classes)
            ):
                elems.append(elem)
                container = (
                    pf.RawInline('', doc.format)
                    if isinstance(elem, pf.Code)
                    else pf.RawBlock('', doc.format))
                if 'diff' in elem.classes and doc.format == 'latex':
                    container = pf.Span() if isinstance(elem, pf.Code) else pf.Div()
                containers.append(container)
                return container

        doc.walk(code)
        if not elems:
            return

        cls.placeholder_prefix = cls._compute_unique_placeholder(elem.text for elem in elems)

        for elem in elems:
           elem.text = cls._replace_fragments_with_placeholders(elem.text)

        converted_fragments = cls._convert_fragments(cls.fragments, doc)

        # Intersperse the separator and batch convert all of the code elements at once.
        text, sep = cls._convert_blocks(
            [pf.Plain(elem) if isinstance(elem, pf.Code) else elem for elem in elems],
            cls._compute_unique_placeholder(elem.text for elem in elems),
            doc)

        # The spaces in the ends are optional because of situations like:
        # `$unspecified$ f();` that ends up like ` PH  f();`, and the markdown
        # parser ends up eating the leading space. The resulting sinppet becomes
        # somerthing ilke <code>PH  f();</code>, so optionally ignore the spaces.
        placeholder_re = re.compile(fr' ?{cls.placeholder_prefix}(\d+) ?')
        def restore_fragments(text):
            return placeholder_re.sub(
                lambda match: restore_fragments(converted_fragments[int(match.group(1))]),
                text)

        text = restore_fragments(text)
        results = text.split(sep)
        assert(len(results) == len(elems))

        # For HTML, this is handled via CSS in `data/templates/wg21.html`.
        command = '\\renewcommand{{\\{}}}[1]{{\\textcolor[HTML]{{{}}}{{#1}}}}'
        colors = [
          command.format('NormalTok', doc.get_metadata('uccolor')),
          command.format('VariableTok', doc.get_metadata('addcolor')),
          command.format('StringTok', doc.get_metadata('rmcolor')),
        ]

        for elem, container, result in zip(elems, containers, results):
            if isinstance(container, (pf.RawInline, pf.RawBlock)):
                container.text = result
                continue

            if isinstance(container, pf.Span):
                container.content = [
                    *(pf.RawInline(color, 'latex') for color in colors),
                    pf.RawInline(result, 'latex')]
            elif isinstance(container, pf.Div):
                container.content = [
                    pf.RawBlock('{', 'latex'),
                    *(pf.RawBlock(color, 'latex') for color in colors),
                    pf.RawBlock(result, 'latex'),
                    pf.RawBlock('}', 'latex')]

def finalize(doc):
    CodeElems.run(doc)

if __name__ == '__main__':
  pf.run_filters([
      strikeout,
      wording,
      sref,
      divspan,
      cmptable,
      # after `cmptable` because...
      header,  # doesn't apply to the "headers" in comparison table.
      table,   # also applies to tables generated by `cmptable`.
      caption, # also applies to captions generated by `cmptable`.
      *[collect_refs, citation_link],
      automatic_header_link, # needs to be after `header`
  ], prepare, finalize)
