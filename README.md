>Algo_avancee and Machine Learning INFO4 2024 **ISPM**
# QUICKSILVER 🤖
## Membre du groupe :

  * ZAFIARISON **Koloina** Emile, IGGLIA 4, n°10, +261 32 68 902 87
  * RASAMOELINA **Toky** Sandratra Miharimamy, IGGLIA 4 , 07
  * RANDRIANOELINA **Liantsoa** Harimisa IGGLIA4, n°15
  * RASOLONJATOVO Zo **Heriniaina**, IGGLIA 4, n°24
  * RANDIMBINIRINA RAKOTOMANANA **Yusha** Andry Ny Aina, IGGLIA 4, N 45
---
# Outils ⚒️
  * Langage python : pygame 🎮
  * Algorithme pathfinding : A*
---
# Description
 > Pour jouer dans le jeu "puzzle", l'utilisateur doit choisir sur la fenetre principale entre les options "1.Jouer 3x3", "2.Jouer 4x4", et puis entrer la valeur de k correspondant a la valeur de nombre de deplacement de tuile pour faire le "swap". Apres avoir presser sur le bouton "Entree" du clavier, il va choisir soit le mode manuel ou le mode automatique; avec le mode manuel, c'est l'utilisateur qui deplace les tuiles pour essayer de gagner. Mais avec le mode automatique, c'est l'ordinateur qui fait les deplacements pour arranger les tuiles dans la bonne ordre. Lorsque les tuiles du puzzle sont bien ranges, la partie est terminée.         

### Différence de complexité entre 3x3 et 4x4

La différence principale entre une résolution 3x3 réussie et une résolution 4x4 non réussie provient probablement de la **complexité accrue** du puzzle plus grand.

#### Problèmes potentiels pour 4x4 avec k=0 :

* Le calcul heuristique pourrait devenir *moins efficace* avec plus de tuiles
* La génération de l'état d'objectif peut ne pas gérer correctement le 4x4  
* L'espace de recherche augmente de façon **exponentielle** avec la taille du puzzle

# Attributions
  * _Koloina et Heriniaina_: implementation de l'algorithme A* permettant l'automatisation des deplacements par l'ordinateur
  * _Yusha, Liantsoa et Toky_ :  implementation puzzle et creation d'interface graphique avec pygame, et implementation de l'algorithme pour que l'utilisateur joue au jeu  
