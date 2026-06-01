# Build the MDPI LaTeX manuscript. Requires a TeX distribution with latexmk,
# pdflatex and bibtex (the MDPI class lives locally in Definitions/).

MAIN := main

.PHONY: all watch clean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex $(wildcard *.tex) references.bib $(wildcard images/*) $(wildcard plots/*)
	latexmk -pdf -bibtex $(MAIN).tex

watch:
	latexmk -pdf -bibtex -pvc $(MAIN).tex

clean:
	latexmk -C
	rm -f $(MAIN).bbl
