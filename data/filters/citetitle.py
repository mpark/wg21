#!/usr/bin/env python3

# MPark.WG21
#
# Copyright Michael Park, 2025
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

import panflute as pf

"""
This filter is separate from `wg21.py` because it needs to run before `citeproc`.
`wg21.py` currently needs to run after `citeproc` due to `citation_link` (may be others too).

The mechanism is a bit convoluted, but basically... `wg21.csl` is the CSL definition
that determines how references are handled and rendered. The logic there is to optionally
display the title of the reference if a "locator" is present. I don't currently know of
another way to inject a cite-specific thing into the citation.

So, for example `[@Pxxxx]` is a citation without a locator, whereas `[@Pxxxx{}]` is
a citation with a locator. Note the "{}" suffix. This is sufficient to inject the title.
However, since this syntax is rather unfamiliar and cryptic, we offer `[@Pxxxx]{.title}`
instead. This filter transforms `[@Pxxxx]{.title}` into `[@Pxxxx{}]`.
"""

def citetitle(elem, doc):
    if not (
        isinstance(elem, pf.Span) and
        elem.classes == ['title'] and
        len(elem.content) == 1 and
        isinstance(elem.content[0], pf.Cite)
    ):
        return None

    for citation in elem.content[0].citations:
        citation.suffix.append(pf.Str('{}'))

    return elem

if __name__ == '__main__':
    pf.run_filter(citetitle)
