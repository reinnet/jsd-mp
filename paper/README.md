# JSD-MP Article

## Introduction

The LaTeX sources of the JSD-MP article, formatted for **MDPI _Future
Internet_** using MDPI's official class in [`Definitions/`](Definitions/).
Written by [@1995parham](https://github.com/1995parham) and
[@bahador-bakhshi](https://github.com/Bahador-Bakhshi).

The manuscript is split into `main.tex` (preamble, title, abstract, frontmatter,
section includes, conclusion, appendix) and one file per section:
`introduction.tex`, `related-works.tex`, `system.tex`, `formulation.tex`,
`solution.tex`, `results.tex`, and `appendix.tex` (the revenue tables).
References are in `references.bib`.

## Up and Running

You need a TeX distribution (TeX Live or MacTeX) with `latexmk`, `pdflatex` and
`bibtex`. The MDPI class and its assets are vendored under `Definitions/`, so no
extra install is required.

```sh
make            # latexmk -> main.pdf
make watch      # live-recompile on changes
make clean
```

or directly:

```sh
latexmk -pdf -bibtex main.tex
```

## Notes on the MDPI template

- The document class line is
  `\documentclass[futureinternet,article,submit,pdftex,moreauthors]{Definitions/mdpi}`.
  On acceptance, the editorial office changes `submit` to `accept`.
- The `Definitions/` folder here is a working copy of the MDPI class. **Before
  final submission, refresh it from the latest official template** at
  <https://www.mdpi.com/authors/latex> (the class is updated periodically).
- Figures live in `images/` and `plots/`; the bibliography uses the MDPI BibTeX
  style shipped with the class.
