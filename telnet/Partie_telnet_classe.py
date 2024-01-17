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
        for node in lab.nodes: #récupère les id de chaque lien 
            node.get()
            for r in (len(liste)):
                if r.nom == node.name:
                    if r.AS == 1: 
                        RIP(node.name)
                        for int_rip in r.voisins:
                            RIP_int(node.name, int_rip["Int"])
                    else:
                        ID_OSPF(node.name,r.id)
                        for int_ospf in r.voisins:
                            OSPF(node.name, int_ospf["Int"])
            

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