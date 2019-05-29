#!/usr/bin/env python3

"""
"""

import html
import json
import os.path
import panflute as pf
import re
import tempfile

escape_char = '@'
escape_span = re.compile('{ec}(.*?){ec}'.format(ec=escape_char))

def prepare(doc):
    datadir = doc.get_metadata('datadir')

    kate = pf.run_pandoc(args=['--print-highlight-style', 'kate'])
    json_styles = json.loads(kate)

    json_styles['background-color'] = '#' + doc.get_metadata('shadecolor')
    text_styles = json_styles['text-styles']
    text_styles['BuiltIn'] = text_styles['Normal']
    text_styles['Comment']['italic'] = True
    text_styles['ControlFlow'] = text_styles['DataType']
    text_styles['Keyword'] = text_styles['DataType']
    text_styles['Variable']['text-color'] = '#' + doc.get_metadata('addcolor')
    text_styles['String']['text-color'] = '#' + doc.get_metadata('rmcolor')

    with tempfile.NamedTemporaryFile('w', suffix='.theme') as f:
        json.dump(json_styles, f)
        f.flush()

        def highlighting(output_format):
            return pf.convert_text(
                '`_`{.cpp}',
                output_format=output_format,
                extra_args=[
                    '--highlight-style', f.name,
                    '--template', os.path.join(datadir, 'template', 'highlighting')
                ])

        doc.metadata['highlighting-macros'] = pf.MetaBlocks(
            pf.RawBlock(highlighting('latex'), 'latex'))
        doc.metadata['highlighting-css'] = pf.MetaBlocks(
            pf.RawBlock(highlighting('html'), 'html'))

def protect_code(elem, doc):
    if isinstance(elem, pf.Code):
        return pf.Span(pf.RawInline('\\mbox{', 'latex'), elem, pf.RawInline('}', 'latex'))

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

    def _wrap(opening, closing):
        if isinstance(elem, pf.Div):
            if elem.content and isinstance(elem.content[0], pf.Para):
                elem.content[0].content.list.insert(0, opening)
            else:
                elem.content.list.insert(0, pf.Plain(opening))
            if elem.content and isinstance(elem.content[-1], pf.Para):
                elem.content[-1].content.list.append(closing)
            else:
                elem.content.list.append(pf.Plain(closing))
        elif isinstance(elem, pf.Span):
            elem.content.list.insert(0, opening)
            elem.content.list.append(closing)

    def _color(color):
        html_color = doc.get_metadata(color)
        _wrap(pf.RawInline('{{\\color[HTML]{{{}}}'.format(html_color), 'latex'),
              pf.RawInline('}', 'latex'))
        elem.attributes['style'] = 'color: #{}'.format(html_color)

    def _nonnormative(name):
        _wrap(pf.Span(pf.Str('[ '), pf.Emph(pf.Str('{}:'.format(name.title()))), pf.Space),
              pf.Span(pf.Str(' — '), pf.Emph(pf.Str('end {}'.format(name.lower()))), pf.Str(' ]')))

    def _diff(color, latex_tag, html_tag):
        if isinstance(elem, pf.Span):
            elem.walk(protect_code)
            _wrap(pf.RawInline('\\{}{{'.format(latex_tag), 'latex'),
                  pf.RawInline('}', 'latex'))
            _wrap(pf.RawInline('<{}>'.format(html_tag), 'html'),
                  pf.RawInline('</{}>'.format(html_tag), 'html'))
        _color(color)

    def pnum():
        num = pf.stringify(elem)

        if not num.replace('.', '').isdigit():
            raise SyntaxError('`pnum` must be integrals with optional `.` separators.')

        if '.' in num:
            num = '({})'.format(num)

        if doc.format == 'latex':
            return pf.RawInline('\\pnum{{{}}}'.format(num), 'latex')

        if doc.format == 'html':
            return pf.RawInline(
                '<div class="marginalizedparent">' \
                    '<a class="marginalized">{}</a>' \
                '</div>'.format(num), 'html')

        return pf.Superscript(pf.Str(num))

    def example(): _nonnormative('example')
    def note():    _nonnormative('note')
    def ednote():
        _wrap(pf.Str("[ Editor's note: "), pf.Str(' ]'))
        _color('ednotecolor')

    def add(): _diff('addcolor', 'uline', 'ins')
    def rm():  _diff('rmcolor', 'sout', 'del')

    if not isinstance(elem, pf.Div) and not isinstance(elem, pf.Span):
        return None

    clses = list(reversed(elem.classes))

    if 'pnum' in clses and isinstance(elem, pf.Span):
        return pnum()

    note_cls = next(iter(cls for cls in clses if cls in {'example', 'note', 'ednote'}), None)
    if note_cls == 'example':  example()
    elif note_cls == 'note':   note()
    elif note_cls == 'ednote': ednote(); return

    diff_cls = next(iter(cls for cls in clses if cls in {'add', 'rm'}), None)
    if diff_cls == 'add':  add()
    elif diff_cls == 'rm': rm()

def tonytable(table, doc):
    """
    Tony Tables: CodeBlocks are the first-class entities that get added
    to the table. The last (if any) header leading upto a CodeBlock is
    the header that gets attached to the table cell with the CodeBlock.

    Each CodeBlock entry is pushed onto the current row. Horizontal rule
    is used to move to the next row.

    # Example

    ::: tonytable

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

    +------------------------------------------------+-------------------------------------------------+
    | __Before__                                     | __After__                                       |
    +------------------------------------------------+-------------------------------------------------+
    | ```cpp                                         | ```cpp                                          |
    | std::visit([&](auto&& x) {                     | inspect (v) {                                   |
    |   strm << "got auto: " << x;                   |   <auto> x: strm << "got auto: " << x;          |
    | }, v);                                         | }                                               |
    |                                                | ```                                             |
    +------------------------------------------------+-------------------------------------------------+
    | std::visit([&](auto&& x) {                     | ```cpp                                          |
    |   using X = std::remove_cvref_t<decltype(x)>;  | inspect (v) {                                   |
    |   if constexpr (C1<X>()) {                     |   <C1> c1: strm << "got C1: " << c1;            |
    |     strm << "got C1: " << x;                   |   <C2> c2: strm << "got C2: " << c2;            |
    |   } else if constexpr (C2<X>()) {              | }                                               |
    |     strm << "got C2: " << x;                   | ```                                             |
    |   }                                            |                                                 |
    | }, v);                                         |                                                 |
    +------------------------------------------------+-------------------------------------------------+
    """

    def build_header(elem):
        # We use a `pf.RawInline` here because setting the `align`
        # attribute on `pf.Div` does not work for some reason.
        header = pf.Plain(pf.RawInline('<div align="center">', 'html'),
                          pf.Strong(*elem.content),
                          pf.RawInline('</div>', 'html'))
        width = float(elem.attributes['width']) if 'width' in elem.attributes else 0
        return header, width

    def build_code(elem, format):
        if (format != 'gfm'):
            return elem
        lang = ' lang="{}"'.format(elem.classes[0]) if elem.classes else ''
        code = html.escape(elem.text)
        return pf.RawBlock('\n\n<pre{lang}>\n{code}\n</pre>'.format(lang=lang, code=code))

    def build_row(elems):
        return pf.TableRow(*[pf.TableCell(elem) for elem in elems])

    if not isinstance(table, pf.Div) or 'tonytable' not in table.classes:
        return None

    rows = []

    kwargs = {}

    headers = []
    widths = []
    examples = []

    header = pf.Null()
    width = 0
    table.content.append(pf.HorizontalRule())
    for elem in table.content:
        if isinstance(elem, pf.Header):
            header, width = build_header(elem)
        elif isinstance(elem, pf.CodeBlock):
            headers.append(header)
            widths.append(width)
            header = pf.Null()
            width = 0

            examples.append(build_code(elem, doc.format))
        elif isinstance(elem, pf.HorizontalRule) and examples:
            if not all(isinstance(header, pf.Null) for header in headers):
                rows.append(build_row(headers))

            if 'width' not in kwargs:
                kwargs['width'] = widths

            rows.append(build_row(examples))

            headers = []
            widths = []
            examples = []
        else:
            pf.debug("[Warning] The following is ignored by a Tony Table:",
                     pf.stringify(elem))

    return pf.Table(*rows, **kwargs)

def codeblock(elem, doc):
    if not isinstance(elem, pf.CodeBlock):
        return None

    is_raw = not elem.classes

    if is_raw:
        elem.classes.append('default')
        elem.attributes['style'] = 'color: inherit'

    if not any(cls in elem.classes for cls in ['cpp', 'default', 'diff']):
        return None

    if escape_char not in elem.text:
        return None

    datadir = doc.get_metadata('datadir')
    syntaxdir = os.path.join(datadir, 'syntax')

    text = pf.convert_text(
        elem,
        input_format='panflute',
        output_format=doc.format,
        extra_args=[
            '--syntax-definition', os.path.join(syntaxdir, 'isocpp.xml')
        ])

    def repl(match_obj):
        match = match_obj.group(1)
        if not match:  # @@
            return match_obj.group(0)
        if match.isspace():  # @  @
            return match
        return pf.convert_text(
            pf.Plain(*pf.convert_text(match)[0].content),
            input_format='panflute',
            output_format=doc.format)

    result = pf.RawBlock(escape_span.sub(repl, text), doc.format)

    return pf.Div(
        pf.RawBlock('{\\renewcommand{\\NormalTok}[1]{#1}', 'latex'),
        result,
        pf.RawBlock('}', 'latex')) if is_raw else result

# https://github.com/jgm/pandoc/issues/5529
def strikeout(elem, doc):
    if not isinstance(elem, pf.Strikeout):
        return None

    elem.walk(protect_code)

if __name__ == '__main__':
    pf.run_filters([divspan, tonytable, codeblock, strikeout], prepare=prepare)
