---
title: "Wording Tests"
document: D0000R1
date: 2026-01-01
audience:
  - Library Evolution
author:
  - name: Test Author
    email: <test@example.com>
toc: true
toc-depth: 2
---

# Wording Blocks

## [intro.compliance.general]{.sref} {-}

::: wording
#. The set of _diagnosable rules_ consists of all syntactic and semantic rules
   in this document except for those rules containing an explicit notation that
   "no diagnostic is required" or which are described as resulting in "undefined behavior".

#. Although this document states only requirements on C++ implementations, those
   requirements are often easier to understand if they are phrased as requirements
   on programs, parts of programs, or execution of programs. Such requirements have
   the following meaning:

   - If a program contains no violations of the rules in [lex]{- .sref} through
     [exec]{- .sref} as well as those specified in [depr]{- .sref}, a conforming
     implementation shall accept and correctly execute that program, except when
     the implementation's limitations are exceeded.
   - If a program contains a violation of a rule for which no diagnostic is required,
     this document places no requirement on implementations with respect to that program.
   - Otherwise, if a program contains
     - a violation of any diagnosable rule,
     - a preprocessing translation unit with a `#warning` preprocessing directive
       ([cpp.error]{- .sref}),
     - an occurrence of a construct described in this document as "conditionally-supported",
       when the implementation does not support that construct, or
     - a contract assertion ([basic.contract.eval]{- .sref}) evaluated with
       a checking semantic in a manifestly constant-evaluated context
       ([expr.const.defns]{- .sref}) resulting in a contract violation,

     a conforming implementation shall issue at least one diagnostic message.

   [During template argument deduction and substitution, certain constructs that
   in other contexts require a diagnostic are treated differently;
   see [temp.deduct]{- .sref}.]{.note}

#. For classes and class templates, the library Clauses specify partial definitions.
   Private members are not specified, but each implementation shall supply them to complete
   the definitions according to the description in the library Clauses.
:::

## [cpp.error]{.sref} {-}

::: wording
#. A preprocessing directive of the form

   > ```cpp
   > # error $pp-tokens~opt~$ $new-line$
   > ```

   renders the program ill-formed. A preprocessing directive of the form

   > ```cpp
   > # warning $pp-tokens~opt~$ $new-line$
   > ```

   requires the implementation to produce at least one diagnostic message for
   the preprocessing translation unit ([intro.compliance.general]{- .sref}).

#. _Recommended practice_: Any diagnostic message caused by either of these directives should include the specified sequence of preprocessing tokens.
:::
