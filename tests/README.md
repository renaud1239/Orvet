Infrastructure de tests
=======================

La commande

    ./exe_tests.sh
    
permet de faire tourner tous les tests (avec comparaison contre les sorties de référence).

Les deux commandes :

    $ ./exe_tests.sh | grep OK | wc -l
    40
    $ ./exe_tests.sh | grep KO | wc -l
    0

permettent de connaitre le nombre de tests passés avec succès et le nombre de tests en échec.
    
La commande

    ./gen_tests.sh
    
permet de regénérer toutes les sorties de référence (auquel cas il faut être sûr de son coup ;-).

Tous les tests doivent passer lors d'un commit et il est vivement encouragé d'en ajouter, particulièrement lors d'un ajout de fonctionalité.
