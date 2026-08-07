# Separator compression paper

Compile from this directory with:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript's theorem sources are the immutable Cycle 7--11 artifacts at
the project root. The paper does not claim an exact solution of the
three-dimensional Ising model.
