# JSD-MP Article

## Introduction

The [Typst](https://typst.app/) sources of the JSD-MP article, migrated from the
original Elsevier LaTeX template. Written by
[@1995parham](https://github.com/1995parham) and
[@bahador-bakhshi](https://github.com/Bahador-Bakhshi).

The manuscript is split into `main.typ` (preamble, title, abstract, structure)
and one file per section (`introduction.typ`, `related-works.typ`, `system.typ`,
`formulation.typ`, `solution.typ`, `results.typ`). Shared helpers live in
`lib.typ`; references are in `references.bib`.

## Up and Running

Install [Typst](https://github.com/typst/typst) (e.g. `brew install typst`),
then:

```sh
make            # compiles main.typ -> main.pdf
make watch      # live-recompile on changes
```

or directly:

```sh
typst compile main.typ main.pdf
```
