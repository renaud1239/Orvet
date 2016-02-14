#!/bin/sh

echo "Programme : $1"
echo "Entrée : $2"
echo "Sortie : $3 (générée)"

python3 ../orvet.py $1 -non-interactif < $2 > $3

echo '----------------------------------------'



