# JSD-MP Article

## Introduction

The latex files of JSD-MP article in Elsevier template. Article is written by [@1995parham](https://github.com/1995parham) and [@bahador-bakhshi](https://github.com/Bahador-Bakhshi).
Source code is available on [overleaf](https://overleaf.com/).

## Up and Running

1. Install the required packages.

```sh
sudo tlmgr install elsarticle
sudo tlmgr install multirow
sudo tlmgr install algorithmicx algorithms
sudo tlmgr install soul
```

2. Compile and Run :roket:

```sh
## with Makefile
make
## with latexmk
latexmk main.tex
```
