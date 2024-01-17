from gns3fy import Gns3Connector, Project,Node
#from Modif_config import routeurBord
from tabulate import tabulate
from fonctions_tn import *
import telnetlib
import time 
import json
from lecture_json import Routeur
from ipaddress import IPv6Address, ip_network


# Define the server object to establish the connection
gns3_server = Gns3Connector(url ="http://localhost:3080")

# Define the lab you want to load and assign the server connector
lab = Project(name="Projet", connector=gns3_server)
lab.get()

print(
        tabulate(
            gns3_server.projects_summary(is_print=False),
            headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
        )
    )

# Access the project attributes
print(f"Name: {lab.name} -- Status: {lab.status} -- Is auto_closed?: {lab.auto_close}\n")

# Open the project
lab.open()
lab.status

# Verify the stats
lab.stats

class GNS3_telnet:
    def __init__(self, liste, dico_routeurs) :
        self.liste = liste
        self.dico_routeurs = dico_routeurs
        
    def IPv6_LOOP_RIP_OSPF(self, liste, dico_routeurs):
        for r in liste:
            routeur_config = dico_routeurs[r.nom]
            tn = telnetlib.Telnet(routeur_config[0],routeur_config[1])
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
    
    def BGP(self, liste, dico_routeurs):
        routeur_config = dico_routeurs[r.nom]
        tn = telnetlib.Telnet(routeur_config[0],routeur_config[1])
        for r in liste :

            ID_BGP(r.nom,r.id,r.AS)
            
            for v in r.voisins :
                # si routeur de bord : eBGP
                if v["AS"] != r.AS : 
                    eBGP(r.nom,v["Adresse_v"], v["AS"])
            
            for t in liste : 
                    if t.AS == r.AS and t.nom != r.nom :
                        iBGP(r.nom,t.loopback,r.AS)

def Config():
        f = open("network_intent.json","r")
        content = f.read()
        obj=json.loads(content)

        routeurs = obj["Routeurs"]

        l = []

        for r in routeurs :
            r = Routeur(r["Nom"],r["ID"],r["AS"],r["Protocole"],r["Loopback"],r["Voisins"])
            l.append(r)
        return l


liste_routeurs = Config()
dico_routeurs_gns3 = {}
for node in lab.nodes:
        node.get()#récupère les informations du noeud
        node.start()
        print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}\n")
        dico_routeurs_gns3[node.name] = [node.console_host,str(node.console)]
GNS3_telnet(liste_routeurs,dico_routeurs_gns3)                    



