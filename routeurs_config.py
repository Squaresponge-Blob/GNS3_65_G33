"""
vérifie la position du routeur et lance les configurations nécessaires
"""

from lecture_json import Routeur, liste_routeurs
from fonctions_config import *

liste_AS ={}
liste_AS["1"] = []
liste_AS["2"] = []
for r in liste_routeurs :
    liste_AS[r.AS].append(r)

for r in liste_routeurs :

    config = ""

    config = Config_debut(config,r.nom) #fonction qui écrit le début, tjrs pareil sauf pour le hostname r.nom

    #Configurer les interfaces (en fonction du protocole)
    for v in r.voisins :
        config = Config_interface(config,v["Int"],v["Adresse"]) #activer ipv6, donner une adresse
        if r.protocole == "RIP" :
            config = Int_RIP(config) # ajoute la ligne pour activer RIP
        if r.protocole =="OSPF":
            config = Int_OSPF(config)
        
    config = Config_Loop(config,"Loopback0", r.loopback)
    if r.protocole == "RIP" :
        config = Int_RIP(config) # ajoute la ligne pour activer RIP
    if r.protocole =="OSPF":
        config = Int_OSPF(config)
    if r.voisins["Metric"] != 1 :
        config = Int_OSPF_cost(config)

    #OSPF interface passif
    #interface passif
    if routeurBord(r) and r.protocole == "OSPF" : 
        config = Config_int_passif(config,v["Int"])

    
    #BGP    
    config = Config_BGP(config, r.AS, r.id) # bloc commun pour tous les routeurs (en eBGP et iBGP)
    
    for r2 in liste_AS[r.AS] :
        if r2.nom != r.nom :
            config = Config_BGP_neighbor(config,r2.loopback[:7],r2.AS)
            config = Config_iBGP(config, r2.loopback[:7])
    if routeurBord(r) :
        for v in r.voisins : 
            if v["AS"] != r.AS :
                adresse_v = find_ad(r.nom, v["Nom"],liste_routeurs)
                config = Config_BGP_neighbor(config,adresse_v[:15],v["AS"]) # ligne neighbor [adresse_v] remote-as [AS]
    

    config = Config_BGP2(config) #address-family ipv6

    #Network advertisement pour routeurs de bords 
    if routeurBord(r) : 
        for i in range (1,11) :
            network = "2001:100:"+r.AS+":"+str(i)+"::/64"
            config = Config_BGP_adv(config,network)
        for v in r.voisins :
            if v["AS"]!=r.AS :
                network = v["Adresse"][:14]+"/64"
                config = Config_BGP_adv(config,network)

    for r2 in liste_AS[r.AS] :
        if r2.nom != r.nom :
            config = Config_BGP_activate(config, r2.loopback[:7])
    if routeurBord(r) :
        for v in r.voisins : 
            if v["AS"] != r.AS :
                adresse_v = find_ad(r.nom, v["Nom"],liste_routeurs)
                config = Config_BGP_activate(config,adresse_v[:15]) # ligne neighbor [adresse_v] remote-as [AS]
    
    config = Config_BGP_exit(config)

    # configurer les protocoles (lignes à la fin)
    if r.protocole == "RIP" :
        config = Config_RIP(config)
    if r.protocole == "OSPF" :
        config = Config_OSPF(config,r.id)



    config = Config_fin(config) #trucs à la fin

    print(f"***Config de {r.nom} en cours d'écriture***")

    Ecrire_dans_fichier(config,r.nom) 
    print(f"***Config de {r.nom} faite***")

