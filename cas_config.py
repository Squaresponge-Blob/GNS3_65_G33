"""
vérifie la position du routeur et lance les configurations nécessaires
"""

from lecture_json import Routeur, liste_routeurs
from Modif_config import *

def find_ad(a, b, liste_routeurs) : 
    """
    trouve l'adresse du routeur a sur l'interface où il est connecté à b
    """
    for r in liste_routeurs :
        if r.nom == b :
            for v in r.voisins :
                if v["Nom"] == a :
                    return v["Adresse"]





for r in liste_routeurs :

    config = ""

    Config_debut(config,r.nom) #fonction qui écrit le début, tjrs pareil sauf pour le hostname r.nom

    #Configurer les interfaces (en fonction du protocole)
    for v in r.voisins :
        Config_interface(config,v["Int",v["Adresse"]]) #activer ipv6, donner une adresse
        if r.AS == "1" :
            Int_RIP(config) # ajoute la ligne pour activer RIP
        if r.AS =="2":
            Int_OSPF(config)
        
        Config_interface(config,"Loopback0", r.loopback)
        if r.AS == "1" :
            Int_RIP(config) # ajoute la ligne pour activer RIP
        if r.AS =="2":
            Int_OSPF(config)

    #OSPF interface passif
    #interface passif
    for v in r.voisins : 
        if v["AS"] != r.AS and r.AS == "2":
            Config_int_passif(config,v["Int"])

    
    #BGP
    
    Config_BGP(config) # bloc commun pour tous les routeurs (en eBGP et iBGP)
    for v in r.voisins :

        adresse_v = find_ad(r.nom, v["Nom"])   
        Config_BGP(config,adresse_v,v["AS"]) # ligne neighbor [adresse_v] remote-as [AS]
        
        #iBGP
        if v["AS"] == r.AS :
            Config_iBGP(config,adresse_v) # ligne neighbor [adresse_v] update-source Loopback0
    
        Config_BGP2(config) #address-family ipv6
        Config_BGP_activate(config,adresse_v) # la partie qui activate


    # configurer les protocoles (lignes à la fin)
    if r.protocole == "RIP" :
        Config_RIP(config,r.id)
    if r.protocole == "OSPF" :
        Config_OSPF(config,r.id)



    Config_fin(config) #trucs à la fin

    Ecrire_dans_fichier(config,r.nom) 


    