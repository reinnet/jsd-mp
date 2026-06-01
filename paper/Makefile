.PHONY: all watch clean
TYPST ?= typst

all: main.pdf

main.pdf: $(wildcard *.typ) references.bib $(wildcard images/*) $(wildcard plots/*)
	$(TYPST) compile main.typ main.pdf

watch:
	$(TYPST) watch main.typ main.pdf

clean:
	rm -f main.pdf
