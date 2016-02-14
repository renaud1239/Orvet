#!/bin/sh

echo "Programme : $1"
echo "Entrée : $2"
echo "Sortie : $3"

python3 ../orvet.py $1 -non-interactif < $2 > tmp.out
diff tmp.out $3

if [ $? = 0 ]
then
    echo "Test OK :-)"
else
    echo "Test KO :-("
fi

rm tmp.out

echo '----------------------------------------'



