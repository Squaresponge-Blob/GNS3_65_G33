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

f = open("network_intent.json","r")
content = f.read()
obj=json.loads(content)

routeurs = obj["Routeurs"]

liste_routeurs = []
for r in routeurs :
    r = Routeur(r["Nom"],r["ID"],r["AS"],r["Protocole"],r["Loopback"],r["Voisins"])
    liste_routeurs.append(r)

# Verify the stats
lab.stats

class GNS3_telnet:
    def __init__(self, nom, id, AS, protocole, loopback, voisins) :
        self.nom = nom
        self.id = id
        self.AS = AS
        self.protocole = protocole
        self.loopback = loopback
        self.voisins = voisins
    
    def IPv6(self, liste): 
        for node in lab.nodes: #récupère les id de chaque lien 
            node.get()
            for r in (len(liste)):
                if r.nom == node.name:
                    for ip in r.voisins:
                        Config_adresse(node.name,ip["Adresse"],ip["Int"])
    
    def RIP_OSPF(self, liste):
        for r in liste:
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
    
    def BGP(self, liste):
        for r in liste :
            ID_BGP(r.nom,r.id,r.AS)
            
            for v in r.voisins :
                # si routeur de bord : eBGP
                if v["AS"] != r.AS : 
                    eBGP(r.nom,v["Adresse_v"], v["AS"])
            
            for t in liste_routeurs : 
                    if t.AS == r.AS and t.nom != r.nom :
                        iBGP(r.nom,t.loopback,r.AS)
            

    def Config(self):
        f = open("network_intent.json","r")
        content = f.read()
        obj=json.loads(content)

        routeurs = obj["Routeurs"]

        self.liste_routeurs = []
        for r in routeurs :
            r = Routeur(r["Nom"],r["ID"],r["AS"],r["Protocole"],r["Loopback"],r["Voisins"])
            self.liste_routeurs.append(r)
        return self.liste_routeurs