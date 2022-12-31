Idriss BACHI
Célian VALANTIN

## Rapport sur les Échecs:  

Objectifs : L'Objectif du projet est de choisir un sujet au choix et le traiter en utilisant des données publiques Open Data, accessible et non modifiées. Tout cela en utilisant au moins les modules dash et pandas.

Notre sujet : Nous avons décidé de travailler sur les échecs.

Pourquoi les échecs ? : C'est un sujet qui nous parle étant donné que nous aimons y jouer et en recherchant des donnés sur internet, nous nous sommes rendu compte que nous pouvions avoir assez de données pour travailler car la fédération internationale des échecs (FIDE) répertorie plutôt bien les données.



I) La recherche des données : 

Pour faire le projet, nous avons donc cherché des données publique sur internet. Comme dit précédemment, le FIDE nous a beaucoup aidé car elle met à jour chaque mois les données sous forme de fichier XML ou txt. Nous avons donc utilisé les fichiers XML à notre disposition.

De plus pour la seconde partie de notre projet, nous avons voulu utilisé l'API de chess.com. Chess.com est un célébre site ou l'on peut jouer en ligne aux échecs contre des joueurs du monde entier avec tout un système de classement. De plus, de nombreux tournoi y sont organisé avec les meilleurs joueurs du monde. Après quelques recherches, nous avons vu que python propose une bibliothèque (chessdotcom) qui permet de se connecter directement à l'API de chess.com. Nous nous en sommes donc servi pour notre projet



II) Notre projet :

Notre projet est découpé en 2 Grandes partie :
    a) Les données de la FIDE : 
    Cette partie est la plus importante du projet, elle contient un histogramme, une carte, un tableau, deux graphiques circulaires ainsi que 5 champs (Contry, Sex, Title, Date et Name),tous connectés les uns aux autres.
    Lorsqu’on arrive sur la page, tous les champs sont null par défaut et les graphiques représentent donc tous les données du fichier XML récupéré.
    L'histogramme :
    L'histogramme représente la répartition des classement des joueurs par la fédération (A partir de 1000 et jusqu’à plus de 2500). 
    La carte : 
    La carte représente la répartition des joueur selon les pays avec des couleurs différentes selon la densité de joueurs.
    Les deux graphiques circulaire :
    Le premier graphique représente homme / femme et le second graphique représente la répartition des différents titre (en enlevant ceux qui n'en n'ont pas pas sinon le graphique ne serait pas lisible puisqu'il y a assez pas de joueur qui ont un titre par rapport au nombre de joueurs total)
    Le tableau : 
    Le tableau représente les 10 meilleurs joueurs (en terme de classement).

    Il est possible de modifier ces 5 graphiques avec les 5 champs. En effet, les champs sont des options et il est possible d'en remplir un ou plusieurs afin de modifier l’ensemble des graphiques. Par exemple on peut chercher tous les hommes français ou bien on peut rechercher tous les joueurs qui s’appellent 'Magnus'.

    Un point à noter est que si l'on remplit le champs 'Sex', le premier graphique circulaire ne sera plus vraiment utile.

    Cette partie est dynamique car en effet, à chaque fois que l'on éxecute le programme, nous recherchons s'il existe un fichier plus récent sur le site de la FIDE et si tel est le cas, nous le téléchargeons et remplaçons l'ancien fichier.

    b) Les données de chess.com
    La deuxième grande partie de notre projet consiste simplement à pouvoir comparé les statistiques de deux joueurs Chess.com grace à leurs pseudonymes.
    Par exemple On peut comparer Magnus Carlsen (pseudo : MagnusCarlsen) avec Alireza Firouzja (pseudo : Firouzja2003). Par défaut, ce sont nos deux pseudos qui sont mis.
    Cela permet de pouvoir leur nombre de parties joué, (avec nombres de victoires, de défaites et de null et donc leur pourcentage de victoire) donc les trois modes de jeu différents (blitz, rapid et bullet)

    Cette partie est elle aussi dynamique.



III) Les piste d'améliorations :

Nous avons plusieurs améliorations que l'on aurait aimé faire mais nous n’avons pas eu le temps pour les faire.

- Pour le tableau, nous aurions voulu afficher toutes les valeurs sous forme d'entier. Cela fonctionne parfaitement lorsque l'on a pas de valeur 'NaN' dans le tableau, mais des qu'on a une valeur 'NaN', les autres valeurs ne sont pas converti en entier.

- Pour améliorer notre projet, nous pourrions aussi ajouter du CSS afin de faire une interface plus belle



IV) Les problèmes rencontré : 

Comme dans tous les projets, nous avons rencontrés des problèmes plus ou moins important : 

- Ce n'est pas vraiment un problème mais c'est intéressant de noter que on a du filtrer beaucoup de joueur qui sont inscrit à la FIDE mais qui n'ont pas de classement ou leur classement est 0 (souvent car il n'ont pas fait assez de parties). En fait, la classement sont pris en compte seulement à partir de 1000 elo.

- Le CSS en python à été compliqué à mettre en place.


V) La structure du code :

Le code est relativement court et ne comporte pas énormement de partie.
La premiere parite contient plusieurs fonctions qui sont 


VI) Conclusion :

Nous avons donc réalisé le travail demandé en respectant les consignes. Nous aons aimé faire ce projet car même si nous connaissons bien python, il nous a permi de voir une nouvelle facette de ce language.
