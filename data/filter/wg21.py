#!/usr/bin/env python3

"""
"""

import datetime
import html
import json
import os.path
import panflute as pf
import re
import tempfile

escape_char = '@'
escape_span = re.compile('{ec}(.*?){ec}'.format(ec=escape_char))

def prepare(doc):
    date = doc.get_metadata('date')
    if date == 'today':
        doc.metadata['date'] = datetime.date.today().isoformat()

def header(elem, doc):
    if not isinstance(elem, pf.Header):
        return None

    elem.content.append(
        pf.Link(url='#{}'.format(elem.identifier), classes=['self-link']))

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

    def _color(html_color):
        _wrap(pf.RawInline('{{\\color[HTML]{{{}}}'.format(html_color), 'latex'),
              pf.RawInline('}', 'latex'))
        elem.attributes['style'] = 'color: #{}'.format(html_color)

    def _nonnormative(name):
        _wrap(pf.Span(pf.Str('[ '), pf.Emph(pf.Str('{}:'.format(name.title()))), pf.Space),
              pf.Span(pf.Str(' — '), pf.Emph(pf.Str('end {}'.format(name.lower()))), pf.Str(' ]')))

    def _diff(color, latex_tag, html_tag):
        if isinstance(elem, pf.Span):
            def protect_code(elem, doc):
                if isinstance(elem, pf.Code):
                    return pf.Span(pf.RawInline('\\mbox{', 'latex'),
                                   elem,
                                   pf.RawInline('}', 'latex'))
            elem.walk(protect_code)
            _wrap(pf.RawInline('\\{}{{'.format(latex_tag), 'latex'),
                  pf.RawInline('}', 'latex'))
            _wrap(pf.RawInline('<{}>'.format(html_tag), 'html'),
                  pf.RawInline('</{}>'.format(html_tag), 'html'))
        _color(doc.get_metadata(color))

    def pnum():
        num = pf.stringify(elem)

        if '.' in num:
            num = '({})'.format(num)

        if doc.format == 'latex':
            return pf.RawInline('\\pnum{{{}}}'.format(num), 'latex')

        if doc.format == 'html':
            return pf.Span(
                pf.RawInline('<a class="marginalized">{}</a>'.format(num), 'html'),
                classes=['marginalizedparent'])

        return pf.Superscript(pf.Str(num))

    def example(): _nonnormative('example')
    def note():    _nonnormative('note')
    def ednote():
        _wrap(pf.Str("[ Editor's note: "), pf.Str(' ]'))
        _color('0000ff')

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
    Tony Tables: Code blocks are the first-class entities that get added
    to the table. Each code block is pushed onto the current row.
    A horizontal rule (`---`) is used to move to the next row.

    In the first row, the last header (if any) leading upto the i'th
    code block is the header for the i'th column of the table.

    The last block quote (if any) is used as the caption.

    # Example

    ::: tonytable

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

    if not isinstance(table, pf.Div) or 'tonytable' not in table.classes:
        return None

    rows = []
    kwargs = {}

    headers = []
    widths = []
    examples = []

    header = pf.Null()
    width = 0

    first_row = True
    table.content.append(pf.HorizontalRule())

    warning = '[Warning] The following {} is in a Tony Table is ignored:'

    for elem in table.content:
        if isinstance(elem, pf.Header):
            if not isinstance(header, pf.Null):
                pf.debug(warning.format('header'), pf.stringify(header))

            if first_row:
                header = pf.Plain(*elem.content)
                width = float(elem.attributes['width']) if 'width' in elem.attributes else 0
            else:
                pf.debug(warning.format('header'), pf.stringify(elem))
        elif isinstance(elem, pf.BlockQuote):
            if 'caption' in kwargs:
                pf.debug(warning.format('caption'), pf.stringify(*kwargs['caption']))

            kwargs['caption'] = elem.content[0].content.list
        elif isinstance(elem, pf.CodeBlock):
            if first_row:
                headers.append(header)
                widths.append(width)

                header = pf.Null()
                width = 0

            examples.append(elem)
        elif isinstance(elem, pf.HorizontalRule) and examples:
            first_row = False

            rows.append(pf.TableRow(*[pf.TableCell(example) for example in examples]))
            examples = []
        else:
            pf.debug(warning.format('element'), type(elem), pf.stringify(elem))

    if not all(isinstance(header, pf.Null) for header in headers):
        kwargs['header'] = pf.TableRow(*[pf.TableCell(header) for header in headers])

    kwargs['width'] = widths

    return pf.Table(*rows, **kwargs)

def codeblock(elem, doc):
    if not isinstance(elem, pf.CodeBlock):
        return None

    if not elem.classes:
        elem.classes.append('default')

    result = elem

    if any(cls in elem.classes for cls in ['cpp', 'default', 'diff']) and escape_char in elem.text:
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

            if doc.format == 'latex':
                # Undo `escapeLaTeX` from https://github.com/jgm/skylighting
                match = match.replace('\\textbackslash{}', '\\') \
                             .replace('\\{', '{') \
                             .replace('\\}', '}')

            plain = pf.Plain(*pf.convert_text(match)[0].content)
            return pf.convert_text(
                plain.walk(divspan, doc),
                input_format='panflute',
                output_format=doc.format)

        result = pf.RawBlock(escape_span.sub(repl, text), doc.format)

    if 'diff' not in elem.classes:
        return result

    # For HTML, this is handled via CSS in `data/template/wg21.html`.
    command = '\\renewcommand{{\\{}}}[1]{{\\textcolor[HTML]{{{}}}{{#1}}}}'
    return pf.Div(
        pf.RawBlock('{', 'latex'),
        pf.RawBlock(command.format('NormalTok', doc.get_metadata('uccolor')), 'latex'),
        pf.RawBlock(command.format('VariableTok', doc.get_metadata('addcolor')), 'latex'),
        pf.RawBlock(command.format('StringTok', doc.get_metadata('rmcolor')), 'latex'),
        result,
        pf.RawBlock('}', 'latex'))

def table(elem, doc):
    if not isinstance(elem, pf.Table):
        return None

    def header(elem, doc):
        if not isinstance(elem, pf.Plain):
            return None

        return pf.Div(
            pf.Plain(pf.RawInline('\\centering', 'latex'),
                     pf.Strong(*elem.content)),
            attributes={'style': 'text-align:center'})

    if elem.header is not None:
        elem.header.walk(header)

def bibliography(elem, doc):
    if not isinstance(elem, pf.Div) or elem.identifier != 'bibliography':
        return None

    def references(elem, doc):
        if isinstance(elem, pf.Div) and elem.identifier == 'refs':
            nonlocal refs
            refs = elem

    refs = pf.Div()
    elem.walk(references)
    if refs.content:
        # This should just be `return None`, but the HTML output
        # for headers seem to break with `<h1>` inside a `<div>`.
        elem.parent.content.extend(elem.content)

    return []

if __name__ == '__main__':
    pf.run_filters(
        [
            bibliography,
            divspan,
            tonytable,
            # after `tonytable` because...
            codeblock,  # this can produce raw html/latex but `tonytable` expects codeblocks.
            header,     # this doesn't apply to the "headers" in tony table.
            table       # this also applies to tables generated by `tonytable`.
        ],
        prepare=prepare)
