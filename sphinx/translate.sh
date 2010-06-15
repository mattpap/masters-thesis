#!/bin/bash

ARG=$1
INPUT="$ARG.tex"

sed -i -e "1,/\\\hypertarget{--doc-src\/introduction}{}/ d" $INPUT
sed -i -e "/\\\hypertarget{--doc-src\/glossary}{}/,$ d" $INPUT

sed -i -e "s/⋅/*/g" $INPUT
sed -i -e "s/⎠/\//g" $INPUT
sed -i -e "s/⎡/[/g" $INPUT
sed -i -e "s/⎢/[/g" $INPUT
sed -i -e "s/⎣/[/g" $INPUT
sed -i -e "s/⎤/]/g" $INPUT
sed -i -e "s/⎥/]/g" $INPUT
sed -i -e "s/⎦/]/g" $INPUT
sed -i -e "s/⎧/ /g" $INPUT
sed -i -e "s/⎨/\\{/g" $INPUT
sed -i -e "s/⎩/ /g" $INPUT
sed -i -e "s/⎫/ /g" $INPUT
sed -i -e "s/⎬/\\}/g" $INPUT
sed -i -e "s/⎭/ /g" $INPUT
sed -i -e "s/⎚/ /g" $INPUT
sed -i -e "s/⎛/\//g" $INPUT
sed -i -e "s/⎜/|/g" $INPUT
sed -i -e "s/⎝/@textbackslash[]/g" $INPUT
sed -i -e "s/⎞/@textbackslash[]/g" $INPUT
sed -i -e "s/⎟/|/g" $INPUT
sed -i -e "s/─/-/g" $INPUT
sed -i -e "s/╱/\//g" $INPUT
sed -i -e "s/╲/@textbackslash[]/g" $INPUT
sed -i -e "s/₀/0/g" $INPUT
sed -i -e "s/₁/1/g" $INPUT
sed -i -e "s/₂/2/g" $INPUT
sed -i -e "s/₃/3/g" $INPUT
sed -i -e "s/₄/4/g" $INPUT
sed -i -e "s/₅/5/g" $INPUT
sed -i -e "s/₆/6/g" $INPUT
sed -i -e "s/₇/7/g" $INPUT
sed -i -e "s/₈/8/g" $INPUT
sed -i -e "s/₉/9/g" $INPUT

sed -i -e "/resetcurrentobjects/d" $INPUT
sed -i -e "/begin{thebibliography}/,/end{thebibliography}/ d" $INPUT

sed -i -e "s/hyperlink{[^}]\+}{{\[}\([^{]\+\){]}}/cite{\1}/g" $INPUT

sed -i -e "/end{Verbatim}$/{N; s/$/\\\noindent/}" $INPUT

../../fixrefs.py $INPUT
cp $INPUT ../../../latex/content.tex
cp *.pdf ../../../latex/

