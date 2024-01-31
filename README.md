# GNS3



## Intent files

Deux configurations sont disponibles : la configuration à deux AS et 14 routeurs de l’énoncé (*intent.json*) et une configuration supplémentaire pour les communities BGP (*intent_communities.json*).
Pour charger le bon fichier intent, il faut modifier la ligne 15 de *lecture_json.py* avec le nom du fichier json voulu.

Exemple avec chargement de *intent.py* : `f = open("intent.json","r")`.



## Drag and drop bot

Pour configurer automatiquement les fichiers startup-config du projet, il faut entrer dans le terminal le nom du fichier GNS3 (ne pas oublier d’avoir chargé l’intent correspondant au projet dans *lecture_json.py*).
Il suffit ensuite de décommenter soit *config_routeur()*, soit *config_routeur_communities()* dans *main.py* et d’exécuter *main.py*.

Il est aussi possible de revenir au fichier startup-config par défaut en exécutant *Config_routeur_défaut.py*.

Exemple avec un fichier GNS3 nommé *Projet*, pour la configuration à 14 routeurs : `config_routeur()` et `#config_routeur_communities()` dans le *main.py*, puis `Nom du projet GNS3 : Projet` dans le terminal.

## Telnet

La configuration avec telnet s’effectue à l’aide d’une interface graphique. Il faut donc tout d'abord installer les librairies pillow et customtkinter : `pip install pillow` et `pip install customtkinter` dans un terminal.

Il suffit ensuite de lancer le fichier *Interface_graphique.py* et d'entrer dans le terminal le nom du fichier GNS3.

Exemple avec un fichier GNS3 nommé *Projet* : `Nom du projet GNS3 : Projet`.

**Important : Telnet fonctionnne uniquement pour la configuration à 14 routeurs (*intent.json*).**