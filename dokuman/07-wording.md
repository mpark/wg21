# Wording

Proposed wording is the heart of most WG21 papers, and it is where hand-formatting hurts most. The framework gives you markup for every piece of it: added and removed text in the standard's colors, margin paragraph numbers that can number themselves, notes and examples in the standard's `[ Note: ... end note ]` style, editorial and drafting notes, and grammar productions with preserved indentation. After reading this file you will be able to write a complete wording section, from a one-word change to a whole new subclause with numbered paragraphs, and know how each construct looks in PDF and in HTML.

## Adding and removing text

### Inline additions and removals

A small inline addition to standard wording is a bracketed span with the `.add` class. The added text can itself contain bold, italics, or code:

````markdown
Let's add some [new **text**]{.add}.

a `goto`, [`break`, or `continue`]{.add}.
````

Inline additions render underlined in the addition color: green underline in PDF, and underlined inserted text in HTML.

A small inline removal is a bracketed span with the `.rm` class:

````markdown
Remove some [old *text*]{.rm} now.
````

Inline removals render struck out in the removal color: red strikeout in PDF, and struck-out deleted text in HTML. In PDF, ordinary `*emphasis*` inside a change stays italic while the change itself keeps its underline or strikeout. In HTML, readers can hide inline removals with the page's "Hide deleted text" checkbox, which lets them read the wording as it would look after the change.

### Substitutions

A substitution is one span with the old text in square brackets, the new text in parentheses right after it, and the `.sub` class:

````markdown
Substitute: [old *text*](new **text**){.sub}
````

It is shorthand for `[old text]{.rm}[new text]{.add}` and renders the two parts with no space between them: the old text struck out in the removal color, immediately followed by the new text underlined in the addition color, in both PDF and HTML. The "Hide deleted text" checkbox hides the old half of a substitution too.

Both halves can use Markdown formatting. The new-text half is parsed as full Markdown, so it can contain inline formatting and code, and new text that starts with a dash is not mistaken for a list. The old-text half can hold multi-word phrases with their own formatting:

````markdown
appertains to the [label](_general-label_){.sub}.

The only use of a [label with an _identifier_](_label_){.sub} is

No two [label](*label*){.sub}s in a function
````

In the last line, the plural `s` is glued right after the closing brace and stays outside the change styling. Substitutions, additions, and removals can be mixed freely in one paragraph of quoted wording. Extra classes added to a `.sub` substitution are copied onto both the removed half and the added half. `.sub` substitutions work anywhere in the paper, including inside embedded-Markdown fragments in code.

Because `.sub` joins the halves with no space, write a separate removal and addition with a space between them when you want the old and new phrases visibly apart:

````markdown
[`setstate(ios::failbit)` is called]{.rm} [`format_error` is thrown]{.add}.
````

This shows the struck-out phrase, a space, then the inserted phrase.

### Blocks of added or removed wording

A large block of added wording is a fenced div opened with `::: add` and closed with `:::`, and a large block of removed wording uses `::: rm`. Standard wording is usually quoted as a Markdown blockquote, with `>` on every line, inside the div, and code blocks and formatted *Returns* clauses live inside the quote:

````markdown
::: add
> ```
> template<class... Args>
>   string format(const locale& loc, string_view fmt, const Args&... args);
> ```
>
> *Returns*: `vformat(loc, fmt, make_format_args(args...))`.
:::
````

````markdown
::: rm
> The operand of postfix `--` is decremented analogously to the postfix `++` operator.
:::
````

Block additions render in the addition color and block removals in the removal color. In PDF a whole block is colored green or red but not underlined or struck out, unlike inline changes. In HTML the block takes the addition or removal color from the framework's stylesheet. An `::: add` or `::: rm` div can hold several paragraphs and block quotes. Note that the HTML "Hide deleted text" checkbox does not hide block-level `::: rm` sections, only inline removals and substitutions.

### Quoting an editing instruction with its wording

An editing instruction and its proposed wording can be framed as one block quote by prefixing every line with `>`, with the change div and any code fences inside it also prefixed:

````markdown
> Modify section [format.functions]{.sref}:
>
> ::: add
> ```
> template<class... Args>
>   string format(const locale& loc, string_view fmt, const Args&... args);
> ```
> :::
````

The whole thing renders as one indented quotation, with the instruction first and the added declaration in the addition color below it. `[format.functions]{.sref}` is an explicit stable name, which links to that section of the working draft and spells out its number and title; [Explicit stable names](09-stable-names-and-citations.md#explicit-stable-names) covers it.

### Changes inside tables

Inline change markup works inside grid-table cells, and a cell's text with its deletion and addition spans can wrap across several table source rows:

````markdown
+-----------+--------------------------------------------------------------------+
| Specifier | Replacement                                                        |
+===========+====================================================================+
| `%a`      | The locale's abbreviated weekday name. If the value does not       |
|           | contain a valid weekday, [`setstate(ios::failbit)` is called]{.rm} |
|           | [`format_error` is thrown]{.add}.                                  |
+-----------+--------------------------------------------------------------------+
````

The three source rows form one cell, which shows the red struck-out phrase followed by the green inserted phrase, in both PDF and HTML.

### Code inside changes

Code inside a change is shown in the change's style rather than with C++ colors, so the change reads as one uniform color:

- A code block inside an `::: add` block takes the addition color and has syntax highlighting switched off.
- Inline code inside an `::: add` block also loses C++ highlighting so the addition color shows through.
- Inline code inside an inline addition, such as `` [`break`, or `continue`]{.add} ``, is shown in the addition style without C++ highlighting.
- Inline code inside an inline deletion in the middle of a sentence, such as `` [in a `goto` statement]{.rm} ``, is shown struck out without C++ highlighting.

The same switch to plain style happens for code inside editorial and drafting notes, described later in this file.

When an element has more than one of `.add`, `.rm`, and `.mark`, only the first one listed takes effect.

### Wording conventions

The usual conventions of the standard's text are plain Markdown emphasis. Grammar terms in proposed wording are italicized with underscores, for example `_attribute-specifier-seq_` and `_labeled-statement_`. Library element descriptions such as `_Returns:_` and `_Recommended practice_:` are written in italics. Defined terms are italicized with underscore emphasis, for example `_potentially evaluated_`. All of these print in italics in both PDF and HTML.

## The wording block

Wrapping proposed wording in a `::: wording` fenced div turns on automatic numbering of paragraphs, examples, and notes inside it:

````markdown
::: wording
[#]{.pnum} The first paragraph of the new wording.

[#]{.pnum} The second paragraph of the new wording.
:::
````

The two paragraphs are numbered 1 and 2 in the margin. A `::: wording` block adds no visible frame in PDF; its paragraphs just show their numbers. The paragraph number markup, `[#]{.pnum}`, is explained in the next section.

Automatic numbering resets at every new `::: wording` div, so each section of wording starts a fresh paragraph count at 1, along with fresh counters for notes and examples.

Change blocks nest inside a wording block. An `::: add` block nested inside a wording block colors its text as an addition, and an `::: rm` block nested inside it colors its text as a removal, while the numbered items inside either still take paragraph numbers.

All of the automatic features in the rest of this file (the `#` paragraph numbers, list-based paragraphs, and numbered notes and examples) require a surrounding `::: wording` div. A `#` in a paragraph number outside `::: wording` prints this warning, and the `#` is not replaced with a number:

````text
[WARNING] mpark/wg21: automatic paragraph number <num> ignored outside of ::: wording
````

## Paragraph numbers

### Writing paragraph numbers by hand

A paragraph number in front of a wording paragraph is a bracketed span with the `.pnum` class:

````markdown
[1]{.pnum} In this subclause, "before" and "after" refer to the "happens before"
relation.

[2]{.pnum} The *lifetime* of an object or reference is a runtime property of
the object or reference.
````

In PDF, paragraph numbers print in the left margin in small raised type, the way the C++ working draft shows them. In HTML, a paragraph number sits in the left margin as a self-link, and the paragraph a reader links to is highlighted.

Sub-paragraphs, the bulleted items under a paragraph, get a dotted number span at the start of each bullet:

````markdown
[2]{.pnum} The lifetime of an object of type `T` begins when:

  - [2.1]{.pnum} storage with the proper alignment and size for type `T` is obtained, and
  - [2.2]{.pnum} its initialization (if any) is complete.
````

A paragraph number with a dot, such as `[2.1]{.pnum}`, is shown in parentheses as "(2.1)", matching the standard's style for sub-paragraphs. In HTML, the numbers of list items sit further out in the margin than paragraph numbers.

When you insert a new paragraph whose final number is not yet known, use `x` as a placeholder number, typically inside an `::: add` block, while the next existing paragraph keeps its real number:

````markdown
::: add
[x]{.pnum} Some new paragraph here
:::

[6]{.pnum} A program may end the lifetime of an object of class type without
invoking the destructor.
````

The new paragraph shows `x` in the margin and its text in the addition color, and the existing paragraph keeps its 6. In PDF the `x` label is in the addition color too; in HTML it keeps the usual link color of margin numbers.

The `.pnum` class works only on inline spans such as `[1]{.pnum}`, not on `:::` divs. Paragraph numbers written by hand like this work anywhere in the paper.

### Links to numbered paragraphs

In HTML, every margin paragraph number doubles as a link anchor that is unique across the whole paper, so readers can link directly to any numbered paragraph. The anchors are counted document-wide, independent of the displayed numbers, so two paragraphs that both show "1" in different wording blocks still have different anchors. When a reader follows a link to a numbered paragraph, the paragraph's content is highlighted, not just its margin number. PDF has no equivalent.

### Automatic numbers inside wording

Inside a `::: wording` div, writing `#` in a paragraph number lets the framework fill the number in. An explicit number pins that paragraph, and following `#` paragraphs continue from it. `[#.#]{.pnum}` numbers sub-paragraphs under the current paragraph:

````markdown
::: wording
[#]{.pnum} Automatically starts at 1.

[5]{.pnum} Existing paragraph pinned at 5.

[#]{.pnum} Automatically continues to 6.

- [#.#]{.pnum} Automatically starts a nested numbering at (6.1).

::: add
- [#.#]{.pnum} Automatically continues a nested numbering at (6.2).

[x]{.pnum} Added paragraph that does not affect the next automatic number.
:::

[#]{.pnum} Automatically continues to 7.
:::
````

Each paragraph's text states the number it gets. The first `[#]` is 1. `[5]` pins the counter, so the next `[#]` is 6. `[#.#]` gives (6.1), and keeps counting to (6.2) even when the next sub-paragraph sits inside an `::: add` block. `[x]{.pnum}` inside a `::: wording` div inserts a new paragraph without disturbing the automatic count, so the next `[#]{.pnum}` paragraph gets the number it would have had anyway; the margin shows `x`.

### Multi-level numbers

Multi-level numbers follow a few rules. In forms such as `[#.#]{.pnum}` or `[2.#]{.pnum}`, a `#` in a parent position reuses the current parent number, and only the last `#` advances. When there is no current parent number, a `#` in a parent position starts at 1, so the first `[#.#]{.pnum}` in a wording block becomes (1.1). Changing a paragraph number at one level restarts the levels below it, so after `[3.2]{.pnum}`, writing `[4]{.pnum}` and then `[#.#]{.pnum}` gives (4.1).

Here is a block that exercises those rules. Again, each paragraph's text states its result:

````markdown
::: wording
[2]{.pnum} Explicitly pins the paragraph number to 2.

[2.1]{.pnum} Explicitly pins the nested count at (2.1).

[#.#]{.pnum} Automatically continues to (2.2).

[#]{.pnum} Automatically continues to 3.

[#.#]{.pnum} Automatically starts the nested count at (3.1).

[2.#]{.pnum} Resets the nested count to (2.1).
:::
````

`[N.M]{.pnum}`, such as `[2.1]{.pnum}`, pins a nested sub-paragraph number on an ordinary paragraph inside wording. `[N.#]{.pnum}` pins the parent while the child stays automatic. When the pinned parent differs from the current one, the nested count restarts, so `[2.#]{.pnum}` right after (3.1) gives (2.1) even though (2.1) and (2.2) appeared earlier in the block.

Deeper numbers work the same way. `[N.M.K]{.pnum}`, such as `[4.2.5]{.pnum}`, pins a paragraph to a three-level number, and after a deep pin, `[#.#]{.pnum}` advances the second level:

````markdown
::: wording
[4.2.5]{.pnum} Explicitly pins a deeper numeric path, (4.2.5).

[#.#]{.pnum} Returns to the numeric nested count at (4.3).
:::
````

### Literal labels

Any non-numeric placeholder such as `x`, in any position of a paragraph number, is printed verbatim; `[2.x]{.pnum}` shows (2.x). The literal labels leave the numeric count untouched, with one twist: a `#` in the same position right after a literal advances the number instead of reusing it.

````markdown
::: wording
[2]{.pnum} Explicitly pins the paragraph number to 2.

[x]{.pnum} Shows x.

[x.#]{.pnum} Automatically starts the nested count at (x.1).

[x.#]{.pnum} Automatically continues to (x.2).

[x]{.pnum} Shows x, and resets its own nested count.

[x.#]{.pnum} Automatically restarts at (x.1).

[#.#]{.pnum} Returns to the numeric path at (3.1).

[#.x.#]{.pnum} Starts a literal nested path at (3.x.1).

[#.x.#]{.pnum} Continues the literal nested path at (3.x.2).

[#.#]{.pnum} Returns to the numeric nested count at (3.2).
:::
````

`[x.#]{.pnum}` numbers sub-paragraphs automatically under a literal label, and repeating the literal label `[x]{.pnum}` restarts its own nested count. After the literal-labeled paragraphs, `[#.#]{.pnum}` returns to the numeric count; here the last numeric parent was 2, so the `#` after the literal advances it to 3 and gives (3.1). `[#.x.#]{.pnum}` inserts a literal segment in the middle of an automatic number path, and after that literal path, `[#.#]{.pnum}` picks up the ordinary numeric sub-count where it left off, at (3.2).

Under a pinned parent, `[#.x.#]{.pnum}` starts its own literal nested path, independent of any literal path in an earlier block. After `[4.2.5]{.pnum}` in a new wording block, two `[#.x.#]{.pnum}` paragraphs give (4.x.1) and (4.x.2), and a following `[#.#]{.pnum}` still gives (4.3).

## List-based paragraphs

Wording paragraphs can also be written as an ordered Markdown list inside `::: wording`, using `#.` as the list marker to get automatic paragraph numbers. This list-based paragraph mode is marked experimental. It saves typing a `.pnum` span on every paragraph and makes sub-paragraphs fall out of ordinary nested lists.

### Automatic numbers from list markers

````markdown
::: wording
#. In this subclause, "before" and "after" refer to the "happens before" relation.
#. The *lifetime* of an object or reference is a runtime property of the object
   or reference.
:::
````

In list-based mode the list itself disappears from the output: the items render as ordinary paragraphs with margin numbers 1 and 2, not as a numbered list, in both PDF and HTML.

List-based paragraph numbering keeps one counter running across separate lists in the same wording block, and through nested divs (such as `::: add` and `::: rm`) and block quotes inside it. For example, items numbered 6 and 7 inside an `::: rm` block are followed by paragraph 8 after it.

List-based numbering counts only list items, not paragraphs numbered with manual `[#]{.pnum}` spans. So when a `#.` list follows manually numbered paragraphs, start it with an explicit number such as `4.` to avoid restarting at 1. This behavior is inferred from the framework's code rather than shown in a test.

### Pinning a number

A numeric list marker such as `6.` pins the paragraph number, but only when it opens a new list. It opens a new list when the block before it at that level is not a period-style ordered item, for example a `[...]` paragraph, a bullet list, an `x)` item, or the start of a div:

````markdown
::: wording
#. The *lifetime* of an object or reference is a runtime property of the object
   or reference.

[...]

6. A program may end the lifetime of an object of class type without invoking
   the destructor, by reusing or releasing the storage as described above.
:::
````

The `[...]` elision paragraph ends the first list, so `6.` opens a new one and the paragraph is numbered 6.

A numeric marker that directly follows `#.` or `N.` items, even across a blank line, continues the same Markdown list. Its number is discarded and it takes the next count:

````markdown
::: wording
#. First paragraph, numbered 1.
#. Second paragraph, numbered 2.
#. Third paragraph, numbered 3.
#. Fourth paragraph, numbered 4.

17. This marker continues the list above, so it is numbered 5, not 17.
:::
````

The `17.` here is ignored and the paragraph renders as 5. If you meant to pin it, put something that ends the list before it, such as a `[...]` paragraph.

### Sub-paragraphs from nested lists

Sub-paragraphs under a list-based paragraph are written as a nested bullet list, and they are numbered automatically as sub-paragraphs of their parent:

````markdown
::: wording
#. In this subclause, "before" and "after" refer to the "happens before" relation.
#. The *lifetime* of an object or reference is a runtime property of the object
   or reference. [...]

   - storage with the proper alignment and size for type `T` is obtained, and
   - its initialization (if any) is complete, [...]

   4. if `T` is a class type, the destructor call starts, or
   - the storage which the object occupies is released, or is reused by an
     object that is not nested within *o*.
:::
````

The bullets under paragraph 2 are numbered (2.1) and (2.2). A numbered marker inside a nested list partially pins the sub-paragraph number by combining with the parent's number, so `4.` under paragraph 2 gives (2.4), and later bullets keep counting from there, so the last bullet is (2.5). The marker's own number is not shown as a list label; only the margin number appears. Here `4.` follows a bullet list, so it opens a new list and the pin is honored.

A few more nesting rules:

- A `-` bullet list or a list with numeric markers such as `4.` nested inside a numbered wording item gives sub-paragraph numbers like (2.1) and (2.2), and deeper ones like (2.1.1). Nested lists with numeric markers render as bullet lists showing those numbers.
- Bullet and numeric markers can be mixed at the same nesting level, and a `-` bullet after a pinned `5.` under paragraph 2 continues the count from the pin, giving (2.6).
- An indented `-` bullet under a sub-paragraph gives a third level of numbering, such as (2.6.1). In HTML each level's numbers sit further into the margin.
- A numeric marker at the third level, such as `9.` after a `[...]` elision, skips ahead to (2.6.9).
- The `x)` marker in a nested list gives a literal, non-counting label such as (2.6.x), and repeated `x)` items all get the same label.

In PDF and HTML, nested sub-paragraphs render as bullet lists with long-dash bullets, each item showing its margin number.

### Inserting paragraphs with x. and x)

`x.` and `x)` markers never advance the paragraph count, which makes them the list-based way to insert new wording without renumbering. The `x.` marker inserts a new list-based paragraph, usually inside an `::: add` block, so you do not have to shift the numbers of the surrounding paragraphs by hand:

````markdown
::: wording
[...]

::: add
x. Some new paragraph here
:::

6. A program may end the lifetime of an object of class type without invoking
   the destructor, by reusing or releasing the storage as described above.
:::
````

The new paragraph is labeled `x`, with its text in the addition color, and the existing paragraph keeps its 6.

The `x)` marker at the top level works the same way: the paragraph is labeled `x` and the automatic count does not advance. Labeling added paragraphs with `x)` inside an `::: add` block keeps new text from renumbering the existing paragraphs. Sub-bullets under an `x)` paragraph are numbered automatically, as in (x.1), and an `x)` item nested under an `x)` paragraph gets the fully literal label (x.x):

````markdown
::: wording
#. An existing paragraph, numbered 1.

::: add
x) First added paragraph.
   - Nested bullet within an `x)`, numbered (x.1).
   x) Nested `x)` within an `x)`, labeled (x.x).
x) Second added paragraph.
:::

#. The next existing paragraph, numbered 2.
:::
````

Both added paragraphs are labeled `x` and consume no numbers, so the paragraph after the `::: add` block continues the count at 2.

The framework's changelog also lists "suppressed numbering" for paragraphs inside `::: wording` without spelling out its syntax; the documented ways to label a paragraph without consuming a number are the `x` forms (`[x]{.pnum}`, `x.`, and `x)`).

### Continuation paragraphs, elisions, and nested blocks

- An unnumbered continuation paragraph belongs to a numbered item when it is indented under that item. It renders as a plain paragraph with no margin number.
- Unnumbered text that continues a sub-paragraph after its nested list stays inside that sub-paragraph when indented under the bullet.
- A `[...]` elision paragraph inside a list item stays unnumbered and renders with a real ellipsis.

To put block content such as a code block inside a list-based paragraph, leave a blank line after the paragraph text and indent the block to line up with the first non-space character after the list marker:

````markdown
::: wording
#. Some paragraph

   ```
   code
   ```
#. The next paragraph.
:::
````

The code block belongs to paragraph 1, and the next `#.` still continues the count, to 2. A bullet list can be nested directly under a list-based paragraph without the blank line, as long as it is indented to line up with the paragraph text:

````markdown
#. Some paragraph
   - Nested bullet list
````

### Lists that stay lists

Inside wording, some list forms stay ordinary lists and get no paragraph numbers: a nested `#.` list, a top-level `-` bullet list, and any other ordered style such as `a.`, `i.`, or `A.`. Use those when the standard's text itself contains a list.

## Code changes

A change to code can be shown as a ```` ```diff ```` fenced block, with `-` for removed lines, `+` for added lines, and a leading space for unchanged lines:

````markdown
```diff
  template <size_t I, class T1, class T2>
-   constexpr typename tuple_element<I, pair<T1, T2>>::type&
+   constexpr tuple_element_t<I, pair<T1, T2>>&
      get(pair<T1, T2>&) noexcept;
```
````

In a `diff` block, removed lines render red, added lines green, and unchanged lines gray, and `$unspecified$` placeholders still become italic on every kind of line, because `diff` is one of the classes that get embedded Markdown by default. In PDF, unchanged text is drawn in the `uccolor`, added text in the `addcolor`, and removed text in the `rmcolor`, and that recoloring applies only to that block; HTML takes the same coloring from the framework stylesheet. The HTML "No syntax highlighting" checkbox leaves `diff` blocks alone, so the diff colors stay.

The `diff` class also works on inline code, as in `` `...`{.diff} ``, with the same coloring.

For changes to a few tokens rather than whole lines, embedded Markdown with `.add` and `.rm` spans marks the exact tokens that change:

````markdown
```
  constexpr @[typename]{.rm}@ tuple_element@[_t]{.add}@<I, pair<T1, T2>>@[::type]{.rm}@&
```
````

[Wording changes inside code](06-code.md#wording-changes-inside-code) covers this style in full. For inline edits like this, leave the language off the fence so syntax highlighting does not compete with the add and remove colors.

## Examples

A short inline example is a bracketed span with the `.example` class:

````markdown
[`T x = T(T(T()));` value-initializes `x`.]{.example}
````

A longer example, including code blocks, is a fenced `::: example` div:

````markdown
::: example
A simple example of a class definition is

```cpp
struct tnode {
  char tword[20];
  int count;
  tnode* left;
  tnode* right;
};
```
:::
````

Examples render in the standard's style as `[ Example 1: ... end example ]`, with the label and "end example" in italics and a long dash before "end example", in both PDF and HTML. An example with no number, such as one outside wording without `num=` or one marked unnumbered, shows just "Example:".

### Numbering examples

Inside `::: wording`, examples are numbered automatically, both the `::: example` divs and the span form. The counter restarts at 1 in each wording block, and it is separate from the counter for notes.

`num=` gives an example an explicit number, and inside wording the following examples count up from the pinned number:

````markdown
::: wording
[`T x = T(T(T()));` value-initializes `x`.]{.example}

::: {.example num=5}
```cpp
auto a = do { do_return 1; };           // OK, deduces int
auto b = do -> long { do_return 1; };   // OK, explicit type is long
```
:::
:::
````

The first example is "Example 1" and the second is "Example 5"; a third example after it would be "Example 6".

Adding the class `-` or `.unnumbered` to an example inside wording keeps it out of automatic numbering, so it shows no number, for example `::: {.example .unnumbered}`.

In HTML, the number of an example is a clickable link to it, anchored at your own id if you give one (as in `::: {#my-example .example}`), otherwise at an automatic id like `example-1`, numbered across the whole paper. In PDF the number is plain text.

Examples and notes can take a change class too, as in `::: {.example .add}`, which shows the whole example as added.

## Notes

A short inline note is a bracketed span with the `.note` class:

````markdown
[Padding bits have unspecified value, but cannot cause traps.]{.note}
````

A longer note, including code blocks, is a fenced `::: note` div:

````markdown
::: note
An expression of type "*cv1* `T`" can initialize an object of type "*cv2* `T`"
independently of the cv-qualifiers *cv1* and *cv2*.

```cpp
int a;
const int b = a;
int c = b;
```
:::
````

A note renders in the standard's style as `[ Note: ... end note ]`, with "Note:" and "end note" in italics, a long dash before "end note", and the note text in the normal body color, in both PDF and HTML. Inline code and other inline formatting inside a note span render inside the note.

An example can sit inside a note by nesting an `::: example` div within a `::: note` div:

````markdown
::: note
The declaration of a class name takes effect immediately after the *identifier*
is seen in the class definition.

::: example
```cpp
class A * A;
```
:::
:::
````

### Numbering notes

Notes follow the same numbering rules as examples. Inside `::: wording`, notes (the `::: note` divs and the span form) are numbered automatically, with a counter separate from the examples' counter that restarts at 1 in each wording block, so a note reads "Note 1:". A numbered note does not get a paragraph number of its own.

````markdown
::: wording
[Padding bits have unspecified value, but cannot cause traps.]{.note}

::: {.note num=3}
This note is pinned at 3, and the next note in this block is 4.
:::
:::
````

`num=` pins a note's number, as in `::: {.note num=3}`, and the following notes count up from it. Adding `-` or `.unnumbered` keeps a note out of the numbering. In HTML the number links to the note, anchored at your own id (as in `::: {#my-note .note}`) or at an automatic id like `note-3`.

When an element has more than one of `.example`, `.note`, `.ednote`, and `.draftnote`, only the first one listed applies.

## Editorial notes

Two more kinds of note speak to the committee rather than becoming part of the standard. Neither is ever numbered, and both can be used anywhere, including inside `::: wording`.

### Editor's notes

A short editorial note, such as flagging a drive-by fix, is a bracketed span with the `.ednote` class:

````markdown
[This is a drive-by fix.]{.ednote}
````

A longer editorial note, for example one explaining wording conventions to the reader, is a fenced `::: ednote` div:

````markdown
::: ednote
Throughout the wording, we say that a reflection (an object of type `std::meta::info`)
represents some source construct, while splicing that reflection designates that source
construct.
:::
````

Both forms render as `[ Editor's note: ... ]`, with no closing "end note" text. They are colored blue in PDF; in HTML the editorial and drafting note color is blue in the light theme and a lighter blue in the dark theme.

### Drafting notes

A short drafting note is a bracketed span with the `.draftnote` class, and an optional `audience` attribute names who it is addressed to:

````markdown
[An `audience` attribute addresses a specific audience]{.draftnote audience="the reader"}
````

A drafting note renders in blue as `[ Drafting note: ... ]`, or as `[ Drafting note for the reader: ... ]` when `audience="the reader"` is set. A drafting note span that wraps across several source lines rejoins into one paragraph, and a blank line between two drafting note spans keeps them as separate paragraphs.

A longer drafting note is a fenced `::: draftnote` div. To address a block drafting note to an audience, use the braced attribute form of the div opener:

````markdown
::: draftnote
We don't think we have to change anything here, based on how paragraphs 1 and 3
are already worded.
:::

::: {.draftnote audience=CWG}
Please check this against the current working draft.
:::
````

The first renders as `[ Drafting note: ... ]` and the second as `[ Drafting note for CWG: ... ]`, both colored blue in PDF and in the note color in HTML.

### What editorial notes ignore

Editorial and drafting notes ignore `.add`, `.rm`, or `.mark` placed on the same element, while examples and notes can be combined with them. Code inside `.ednote` or `.draftnote` divs and spans, like code inside `.add` and `.rm`, is switched to plain unhighlighted style so it matches the colored region around it, and it takes on the note's color.

## Grammar

Grammar productions are written as Pandoc line blocks, each line starting with `|`, inside a `>` blockquote, so the leading indentation of alternatives is preserved:

````markdown
> | _selection-statement:_
> |     `if constexpr`_~opt~_ `(` _init-statement~opt~_ _condition_ `)` _statement_
> |     `if constexpr`_~opt~_ `(` _init-statement~opt~_ _condition_ `)` _statement_ `else` _statement_
> |     `switch (` _init-statement~opt~_ _condition_ `)` _statement_
````

Grammar is typeset the way the standard does it, in both PDF and HTML: nonterminals in italics, terminals in code, and the "opt" marker as a subscript. The production renders as an indented quotation with the alternatives indented under the production name. Adding spaces after the `|` in a line indents that alternative under the production name, and the indentation is preserved in the output.

### The pieces of a production

- Nonterminals, including a production name with its trailing colon, are marked by wrapping them in underscores, as in `_selection-statement:_` and `_condition_`.
- Terminals (keywords and punctuation) in backtick inline code are highlighted as C++ automatically, with no language tag.
- A keyword and its following punctuation can share one code span when they form a single terminal sequence, as in `` `switch (` ``, and each token is still highlighted separately.
- An optional nonterminal puts a `~opt~` subscript inside its italic markup, as in `_init-statement~opt~_`.
- An optional terminal takes an italic subscript written directly after its code span with no space, as in `` `if constexpr`_~opt~_ ``.
- The alternate nesting `~_opt_~`, as in `` `constexpr`~_opt_~ ``, gives the same optional marker with the markup order reversed.

### Longer grammar blocks

One long grammar alternative can span several source lines by continuing on quoted lines that do not start with `|`; those lines are joined into a single output line. Several grammar productions can share one quoted block when separated by an empty `>` line; each becomes its own group. A production with many single-token alternatives is written as one italic nonterminal per `|` line, giving a vertical choice list:

````markdown
> | _inspect-case-seq:_
> |     _inspect-case_
> |     _inspect-case-seq_ _inspect-case_
>
> | _inspect-pattern:_
> |     _wildcard-pattern_
> |     _identifier-pattern_
> |     _expression-pattern_
````

The two productions print as separate groups inside one quotation, and the alternatives of `inspect-pattern` stack vertically.

### Changing grammar

A new alternative for an existing grammar production is marked with an inline `.add` span, which may span several indented line-block lines:

````markdown
> | _selection-statement:_
> |     `switch (` _init-statement~opt~_ _condition_ `)` _statement_
> |     [`inspect` `constexpr`~_opt_~ `(` _init-statement~opt~_ _condition_ `)` `{`
>            _inspect-case-seq_
>        `}`]{.add}
````

The new alternative is joined onto one output line and shown underlined in the addition color, green in PDF.

Whole new grammar productions are added by wrapping their line blocks in an `::: add` div placed inside the blockquote:

````markdown
> ::: add
> | _inspect-case-seq:_
> |     _inspect-case_
> |     _inspect-case-seq_ _inspect-case_
>
> | _inspect-guard:_
> |     `if (` _expression_ `)`
> :::
````

These productions are colored as additions but not underlined. In both forms, terminals inside a grammar addition are shown in the addition color instead of C++ syntax colors, so the inserted wording reads as one uniform change.

### Grammar as a code block

A grammar production can also be shown as an indented, syntax-highlighted block by putting a fenced `cpp` code block inside a blockquote within a numbered paragraph:

````markdown
::: wording
#. A preprocessing directive of the form

   > ```cpp
   > # error $pp-tokens~opt~$ $new-line$
   > ```

   renders the program ill-formed.
:::
````

The directive prints as a highlighted C++ block, with `# error` colored as a preprocessor token and `pp-tokens` and `new-line` in italics, followed by the rest of paragraph 1.

Previous: [Code](06-code.md) | Next: [Comparison tables](08-comparison-tables.md)

*2026-09-25 - claude-opus-5.5*
