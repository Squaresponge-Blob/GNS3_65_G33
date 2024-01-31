# GNS3



## Intent files

Deux configurations sont disponibles : la configuration à deux AS et 14 routeurs de l’énoncé (*intent.json*) et un configuration supplémentaire pour les communities BGP (*intent_communities.json*).
Pour charger le bon fichier intent, il faut modifier la ligne 15 de *lecture_json.py* avec le nom du fichier json voulu.

Ex : `f = open("intent.json","r")`.



## Drag and drop bot

Pour configurer automatiquement les fichiers startup-config du projet, il faut tout d’abord annoncer le nom du fichier GNS3 sur la ligne 12 de *fonctions_config.py* (ne pas oublier d’avoir chargé l’intent correspondant au projet).
Il suffit ensuite d’exécuter soit *routeurs_config.py*, soit *routeurs_config_communities.py*.

Ex : `lab = gns3fy.Project(name="Projet", connector=gns3_server)`.

Il est aussi possible de revenir au fichier startup-config par défaut en exécutant *Config_routeur_défaut.py* (modifier ligne 8 avec le nom du projet).




## Telnet

La configuration avec telnet s’effectue à l’aide d’une interface graphique. Il faut pour cela installer pillow et customtkinter : `pip install pillow` et `pip install customtkinter` dans un terminal.
Il faut ensuite charger le projet ligne 17 de *Interface_graphique.py* et ligne 16 de *Partie_telnet_classe.py*. Vérifiez que *Config_routeur_défaut.py* est aussi avec le bon projet.
Il reste à exécuter *Interface_graphique.py* et ajouter dans l’interface le chemin du fichier entre guillemets.
