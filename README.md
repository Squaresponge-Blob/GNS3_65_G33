GNS3

Intent files
Deux configurations sont disponibles�: la configuration � deux AS et 14 routeurs de l��nonc� (intent.json) et un configuration suppl�mentaire pour les communities BGP (intent_communities.json).
Pour charger le bon fichier intent, il faut modifier la ligne 15 de lecture_json.py avec le nom du fichier json voulu.


Drag and drop bot
Pour configurer automatiquement les fichiers startup-config du projet, il faut tout d�abord annoncer le nom du fichier GNS3 sur la ligne 12 de fonctions_config.py (ne pas oublier d�avoir charg� l�intent correspondant au projet).
Il suffit ensuite d�ex�cuter soit routeurs_config.py ou routeurs_config_communities.py.

Il est aussi possible de revenir au fichier startup-config par d�faut en ex�cutant Config_routeur_d�faut.py (modifier ligne 8 avec le nom du projet).


Telnet
La configuration avec telnet s�effectue � l�aide d�une interface graphique. Il faut pour cela installer pillow et customtkinter�: pip install pillow et pip install customtkinter dans un terminal.
Il faut ensuite charger le projet ligne 17 de Interface_graphique.py et ligne 16 de Partie_telnet_classe.py. V�rifiez que Config_routeur_d�faut.py est aussi avec le bon projet.
Il reste � ex�cuter Interface_graphique.py. Il faut ajouter dans l�interface le chemin du fichier entre guillemets.
