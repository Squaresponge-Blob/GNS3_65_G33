from gns3fy import Gns3Connector, Project,Node
#from Modif_config import routeurBord
from tabulate import tabulate
import telnetlib
import time 
import json
from drag_and_drop.lecture_json import Routeur
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
    def __init__(self, nom, id, AS, protocole, loopback, voisins, masque):
        self.nom = nom
        self.id = id
        self.AS = AS
        self.protocole = protocole
        self.loopback = loopback
        self.voisins = voisins
        self.masque = masque 
    
    def IPv6(self, nom, AS): 
        self.adresses_routeur = {}
        num_r = 1
        self.AS_1 = []
        self.AS_2 = []
        self.bord = []
        for node in lab.nodes: #récupère les id de chaque lien 
            node.get()
            for i in range(len(node.links)):
                link = node.links[i]
                if link.link_id not in list: 
                    self.list.append(link.link_id)
                    print(self.list)

        for lien in list: #crée un dictionnaire associant les id des liens et leurs masques d'adresse ip respectives 
            self.adresses_routeur[lien] = "2001:100:1:"+str(num_r)+"::"
            num_r += 1    
        
