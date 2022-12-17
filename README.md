# Systeme-Expert Moteur 0+

Le parser est généré par la bibliothèque PLY, une traduction python des bibliothèques Lex/Yacc. Le code source servant à générer le parser se trouve dans le fichier parser/CustomParser.py

Exécuter le fichier main.py lance le parser afin de pouvoir utiliser le système expert
> python3 main.py

Afficher les règles de grammaire du système
> help()

La base de connaissances peut être remplie à la main ou chargée à partir d'un fichier
> load("chemin_du_fichier")

Déclaration d'un fait
> nom | NON nom (booléen)

> nom = valeur (entier ou chaîne de caractères)

> nom = [valeur1, valeur2, ...] (liste d'entier ou de chaîne de caractères)

Déclaration d'une règle
> nom_règle : premisse1 ET premisse2 ET ... => conclusion1 ET ...

Déclaration de buts ou d'hypothèses
> nom_but : premisse1, premisse2, ...

Les conclusions ont la même forme que les faits et les prémisses, elles, remplacent le '=' par un '=='

Le chaînage avant peut être lancé avec ou sans but en paramètre
> forward(nom_but)

> forward()

Le chaînage arrière se lance avec des hypothèses en paramètre
> backward(hypothèses)

Les buts/hypothèses doivent être ajouté à la base de connaissance au préalable
(voir la commande help() pour leur syntaxe)


### Exemple d'utilisation du système-expert

> load("ressources/medical_case")\
> forward(H1)\
> backward(StressDrugs)

Des connaissances peuvent être ajoutées au cours de l'utilisation du système et peuvent donc influer sur les résultats obtenus
> load("ressources/medical_case")\
> forward(Vitamine)\
> season = Winter\
> forward(Vitamine)
