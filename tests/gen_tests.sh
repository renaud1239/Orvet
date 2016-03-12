#!/bin/sh

echo "ECRASEMENET de tous les tests..."
echo '----------------------------------------'

./gen_test.sh ../exemples/exemple1.orv entrées/exemple1.txt sorties/exemple1.ref

./gen_test.sh ../exemples/exemple2.orv entrées/exemple2.txt sorties/exemple2.ref

./gen_test.sh ../exemples/affectation.orv entrées/affectation.txt sorties/affectation.ref

./gen_test.sh ../exemples/addition.orv entrées/addition.txt sorties/addition.ref

./gen_test.sh ../exemples/addition2.orv entrées/addition2.txt sorties/addition2.ref

./gen_test.sh ../exemples/diveuclid.orv entrées/diveuclid.txt sorties/diveuclid.ref

./gen_test.sh ../exemples/diveuclid.orv entrées/div0.txt sorties/div0.ref

./gen_test.sh ../exemples/min.orv entrées/min.txt sorties/min.ref

./gen_test.sh ../exemples/max.orv entrées/max.txt sorties/max.ref

./gen_test.sh ../exemples/puissance2.orv entrées/puissance2.txt sorties/puissance2.ref

./gen_test.sh ../exemples/boucle.orv entrées/boucle.txt sorties/boucle.ref

./gen_test.sh ../exemples/boucle2.orv entrées/boucle2.txt sorties/boucle2.ref

./gen_test.sh ../exemples/somme.orv entrées/somme.txt sorties/somme.ref

./gen_test.sh ../exemples/somme2.orv entrées/somme.txt sorties/somme2.ref

./gen_test.sh ../exemples/factoriel.orv entrées/factoriel.txt sorties/factoriel.ref

./gen_test.sh ../exemples/bonjour.orv entrées/bonjour.txt sorties/bonjour.ref

./gen_test.sh ../exemples/diveuclid2.orv entrées/diveuclid.txt sorties/diveuclid2.ref

./gen_test.sh ../exemples/booléens.orv entrées/booléens.txt sorties/booléens.ref

./gen_test.sh ../exemples/comp.orv entrées/comp.txt sorties/comp.ref

./gen_test.sh ../exemples/comp.orv entrées/comp-2.txt sorties/comp-2.ref

./gen_test.sh ../exemples/si.orv entrées/comp.txt sorties/si.ref

./gen_test.sh ../exemples/si.orv entrées/comp-2.txt sorties/si-2.ref

./gen_test.sh ../exemples/multiple.orv entrées/multiple.txt sorties/multiple.ref

./gen_test.sh ../exemples/multiple.orv entrées/multiple-2.txt sorties/multiple-2.ref

./gen_test.sh ../exemples/diviseurs.orv entrées/diviseurs.txt sorties/diviseurs.ref

./gen_test.sh ../exemples/diviseurs.orv entrées/diviseurs-2.txt sorties/diviseurs-2.ref

./gen_test.sh ../exemples/premier.orv entrées/diviseurs.txt sorties/premier.ref

./gen_test.sh ../exemples/premier.orv entrées/diviseurs-2.txt sorties/premier-2.ref

./gen_test.sh ../exemples/logique.orv entrées/logique.txt sorties/logique.ref

./gen_test.sh ../exemples/arrêter.orv entrées/diviseurs.txt sorties/arrêter.ref

./gen_test.sh ../exemples/arrêter.orv entrées/diviseurs-2.txt sorties/arrêter-2.ref

./gen_test.sh ../exemples/vérifier.orv entrées/vérifier.txt sorties/vérifier.ref

./gen_test.sh ../exemples/vérifier.orv entrées/vérifier-2.txt sorties/vérifier-2.ref

./gen_test.sh ../exemples/proc.orv entrées/proc.txt sorties/proc.ref

./gen_test.sh ../exemples/proc2.orv entrées/proc.txt sorties/proc2.ref

./gen_test.sh ../exemples/simplifie_frac.orv entrées/simplifie_frac.txt sorties/simplifie_frac.ref

./gen_test.sh ../exemples/famille.orv entrées/famille.txt sorties/famille.ref

./gen_test.sh ../exemples/ératosthène.orv entrées/ératosthène.txt sorties/ératosthène.ref

./gen_test.sh ../exemples/ératosthène.orv entrées/ératosthène-2.txt sorties/ératosthène-2.ref

./gen_test.sh ../exemples/ératosthène2.orv entrées/ératosthène.txt sorties/ératosthène2.ref

./gen_test.sh ../exemples/ératosthène2.orv entrées/ératosthène-2.txt sorties/ératosthène2-2.ref

./gen_test.sh ../exemples/bulles.orv entrées/tri.txt sorties/bulles.ref

./gen_test.sh ../exemples/bulles-rec.orv entrées/tri.txt sorties/bulles-rec.ref

./gen_test.sh ../exemples/tri-facile.orv entrées/tri.txt sorties/tri-facile.ref

./gen_test.sh ../exemples/galettes.orv entrées/galettes.txt sorties/galettes.ref

./gen_test.sh ../exemples/code.orv entrées/code.txt sorties/code.ref

./gen_test.sh ../exemples/code.orv entrées/code-2.txt sorties/code-2.ref

./gen_test.sh ../exemples/code.orv entrées/code-3.txt sorties/code-3.ref

./gen_test.sh ../exemples/fibonacci.orv entrées/fibonacci.txt sorties/fibonacci.ref

./gen_test.sh ../exemples_enfants/division_inf.orv entrées/division_inf.txt sorties/division_inf.ref

./gen_test.sh ../exemples_avancés/euler.orv entrées/euler.txt sorties/euler.ref

./gen_test.sh ../exemples_avancés/fibonacci-rec.orv entrées/fibonacci-rec.txt sorties/fibonacci-rec.ref

./gen_test.sh ../exemples_avancés/fibonacci-rec.orv entrées/fibonacci-rec-2.txt sorties/fibonacci-rec-2.ref

./gen_test.sh ../exemples_avancés/hanoi.orv entrées/hanoi.txt sorties/hanoi.ref

./gen_test.sh ../exemples_avancés/hanoi.orv entrées/hanoi-2.txt sorties/hanoi-2.ref

./gen_test.sh ../exemples_avancés/RC4.orv entrées/RC4.txt sorties/RC4.ref
