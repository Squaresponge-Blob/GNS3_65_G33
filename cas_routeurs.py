"""
vérifie la position du routeur et lance les configurations nécessaires
"""

from test_lecture_json import Routeur, liste_routeurs
from fonctions import *


for r in liste_routeurs :
    #Configurer les adresses physiques
    for v in r.voisins :
        Config_adresse(r.nom,v["Adresse"],v["Int"])

    #Configurer les interfaces loopback 
    Config_loopback(r.nom,r.loopback)

    #Le routeur est dans l'AS X
    if r.AS == "1" :
        RIP(r.nom)
        for v in r.voisins :
            RIP_int(r.nom, v["Int"])

    #Le routeur est dans l'AS Y
    if r.AS == "2" :
        ID_OSPF(r.nom, r.id)
        for v in r.voisins :
            if v["AS"] == r.AS :
                OSPF(r.nom, v["Int"])
            else : 
                OSPF_passif(r.nom, v["Int"])   
                OSPF(r.nom, v["Int"])  


#Routeur de bord => eBGP   
#iBGP sur int loopback
for r in liste_routeurs :
    ID_BGP(r.nom,r.id,r.AS)
    
    for v in r.voisins :

        # si routeur de bord : eBGP
        if v["AS"] != r.AS : 
            eBGP(r.nom,v["Adresse_v"], v["AS"])
    
    for t in liste_routeurs : 
            if t.AS == r.AS and t.nom != r.nom :
                iBGP(r.nom,t.loopback,r.AS)
