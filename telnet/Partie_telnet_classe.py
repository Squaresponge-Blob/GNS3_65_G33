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
        
    def IPv6_LOOP_RIP_OSPF(self):
        for r in self.liste:
            print("le routeur traité est:",r.nom)
            routeur_config = self.dico_routeurs[r.nom]
            tn = telnetlib.Telnet(routeur_config[0],routeur_config[1])
            tn.write(bytes("configure terminal\r",encoding= 'ascii'))
            tn.write(bytes("ipv6 unicast-routing\r",encoding= 'ascii'))
            #Configurer les adresses physiques
            for v in r.voisins :
                Config_adresse(r.nom,v["Adresse"],v["Int"],tn)

                #Configurer les interfaces loopback 
            Config_loopback(r.nom,r.loopback,tn)

                #Le routeur est dans l'AS X
            if r.AS == "1" :
                print("configuration du routeur en RIP")
                RIP(r.nom,tn)
                for v in r.voisins :
                    time.sleep(0.5)
                    RIP_int(r.nom, v["Int"],tn)

                #Le routeur est dans l'AS Y
            if r.AS == "2" :
                print("configuration du routeur en OSPF")
                ID_OSPF(r.nom, r.id,tn)
                for v in r.voisins :
                    time.sleep(0.5)
                    if v["AS"] == r.AS :
                        OSPF(r.nom, v["Int"],tn)
                    else : 
                        OSPF_passif(r.nom, v["Int"],tn)   
                        OSPF(r.nom, v["Int"],tn)
            tn.write(bytes("end\r",encoding= 'ascii'))  
    
    def BGP(self):
        for r in self.liste :
            print("le routeur traité est:",r.nom)
            print("configuration du routeur en BGP")
            routeur_config = self.dico_routeurs[r.nom]

            tn = telnetlib.Telnet(routeur_config[0],routeur_config[1])
            tn.write(bytes("configure terminal\r",encoding= 'ascii'))
            ID_BGP(r.nom,r.id,r.AS,tn)

            for v in r.voisins :
                time.sleep(0.5)
                if len(v["Adresse"])== 18:
                    prefixe = v["Adresse"][:14] +v["Adresse"][15:]
                    print(prefixe)
                else:
                    prefixe = v["Adresse"][:15] +v["Adresse"][16:]
                    print(prefixe)
                eBGP_adv(r.nom, r.AS, prefixe,tn)

                # si routeur de bord : eBGP
                if v["AS"] != r.AS : 
                    eBGP(r.nom,v["Adresse_v"], v["AS"],r.AS,tn)
                    if len(v["Adresse"]) == 18:
                        prefixe = v["Adresse_v"][:14] +v["Adresse_v"][15:]
                        print(prefixe)
                    else:
                        prefixe = v["Adresse_v"][:15] +v["Adresse_v"][16:]
                        print(prefixe)
                    eBGP_adv(r.nom, r.AS, prefixe,tn)

            print("configuration de l'iBGP")
            for t in self.liste : 
                    if t.AS == r.AS and t.nom != r.nom :
                        iBGP(r.nom,t.loopback,r.AS,tn)
            tn.write(bytes("end\r",encoding= 'ascii'))

def Config():
        f = open("network_intent.json","r")
        content = f.read()
        obj=json.loads(content)

        routeurs = obj["Routeurs"]

        l = []
        dico_routeurs = {}

        for r in routeurs :
            r = Routeur(r["Nom"],r["ID"],r["AS"],r["Protocole"],r["Loopback"],r["Voisins"])
            l.append(r)

        for node in lab.nodes:
                node.get()#récupère les informations du noeud
                node.start()
                print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}\n")
                dico_routeurs[node.name] = [node.console_host,str(node.console)]
        return l, dico_routeurs

l,d = Config()
x = GNS3_telnet(l,d)
x.IPv6_LOOP_RIP_OSPF()
x.BGP()                    



