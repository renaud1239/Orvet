
ORVET V0
========

Orvet est un langage de programmation entièrement en français que j'ai développé pour faciliter l'apprentissage des rudiments de l'algorithmique et de la programmation par des enfants, à commencer par les miens... Orvet a été pensé pour écrire avec eux des programmes qu’ils puissent facilement comprendre, relire et faire tourner puis pour qu’ils arrivent peu à peu à en écrire eux-mêmes. 

Dans sa première version qui commence à être assez complète, Orvet permet de manipuler des nombres entiers (sans limitation de taille) ainsi que des booléens. Il est doté de structures de boucle et d'exécution conditionnelle et il supporte les procédures. Il supporte aussi les dictionnaires et, qui peut le plus peut le moins, les tableaux. Enfin, il est depuis peu doté d'extensions temporisées, pour un premier contact avec le temps réel dans les programmes. Toutes ses instructions ne font qu'une et une seule chose élémentaire (en ce sens il ressemble un peu à un super-assembleur). Tout est explicite.

Orvet est facile à utiliser pour programmer (et accessoirement facile à parser et à interpréter).

L'interpréteur est un script Python3 (orvet.py). Il y a ce qu'il faut dans la distribution (orvet.xml) pour intégrer le support du langage depuis notepad++ (coloration syntaxique et lancement de l'interpréteur, voir la section "Installer et utiliser Orvet" du guide.

Le plus simple pour commencer : jeter un coup d'oeil à Guide_Orvet-V0.pdf (pour les pressés, se référer à la section "Démarrage rapide").

Bon, voilà tout de même de quoi faire tourner le "Hello world!" et un autre programme élémentaire (ça suffira à démarrer les trop pressés pour ne serait-ce qu'ouvrir le guide ;-) :

    $ python3 orvet.py exemples/bonjour.orv
    Orvet version 0.1
    Chargement du programme
    4 lignes chargées
    Démarrage de l'exécution
    
    Bonjour monde !
    
    Fin de l'exécution
    
    Appuyer sur Entrée pour fermer...
    
    $ python3 orvet.py exemples/premier.orv
    Orvet version 0.1
    Chargement du programme
    42 lignes chargées
    Démarrage de l'exécution
    
    Valeur de l'entier x ? 23
    23 est un nombre premier
    
    Fin de l'exécution
    
    Appuyer sur Entrée pour fermer...
    $

Orvet est distribué sous licence GPL, si vous l'utilisez je serai très heureux de le savoir. Si vous trouvez des bugs ou avez des idées d'améliorations, je serai aussi très heureux de le savoir (et de corriger les bugs en question). Si vous écrivez des programmes sympas, je serai (encore) très heureux de le savoir et de les inclure dans les exemples fournis (aujourd'hui il y a principalement des exemples élémentaires).

Chaque version d'Orvet aura une devise. Puisqu'elle ne supporte que les nombres entiers, celle de la version 0 est une citation bien connue de L. Kronecker : "Dieu a créé les nombres entiers, le reste est l'œuvre de l'homme.".

Un certain nombre d'extensions sont prévues (cf. sect. "Extensions futures" du PDF) dans un futur proche. La V0 est néanmoins parfaitement opérationnelle pour écrire des "vrais" programmes (et, par ailleurs, Turing-complète).

Si vous souhaitez contribuer, contacter moi !

Voici également le lien vers le [site officiel d'Orvet](http://sirdeyre.free.fr/orvet/orvet.htm) !

Bonne programmation !

![Logo Orvet bariolé](déco/orvet-bariolé.png)
