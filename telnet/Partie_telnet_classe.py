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
lab = Project(name="projet", connector=gns3_server)
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
                time.sleep
                RIP_int(r.nom,"l0",tn)
                time.sleep(1)
                for v in r.voisins :
                    time.sleep(0.5)
                    RIP_int(r.nom, v["Int"],tn)

                #Le routeur est dans l'AS Y
            if r.AS == "2" :
                print("configuration du routeur en OSPF")
                ID_OSPF(r.nom, r.id,tn)
                OSPF(r.nom,"l0",tn)
                for v in r.voisins :
                    time.sleep(0.5)
                    if v["AS"] == r.AS :
                        OSPF(r.nom, v["Int"],tn)
                    else : 
                        OSPF_passif(r.nom, v["Int"],tn)   
                        OSPF(r.nom, v["Int"],tn)
                    time.sleep(0.5)
                    if v["Metric"] != "1" :
                        OSPF_cost(r.nom, v["Int"], v["Metric"], tn)
            tn.write(bytes("end\r",encoding= 'ascii'))  
    
    def BGP(self):
        l_prefixes_AS_1 = []
        l_prefixes_AS_2 = []
        for r in self.liste :
            print("le routeur traité est:",r.nom)
            print("configuration du routeur en BGP")
            routeur_config = self.dico_routeurs[r.nom]

            tn = telnetlib.Telnet(routeur_config[0],routeur_config[1])
            tn.write(bytes("configure terminal\r",encoding= 'ascii'))
            #time.sleep(0.5)
            ID_BGP(r.nom,r.id,r.AS,tn)

            for v in r.voisins :

                if len(v["Adresse"]) == 18:
                    prefixe_1 = v["Adresse"][:12]+"::/64"         
                else:
                    prefixe_1 = v["Adresse"][:13]+"::/64"
                print(prefixe_1)    
                            
                if v["AS"] == "1":
                    if prefixe_1 not in l_prefixes_AS_1:
                        l_prefixes_AS_1.append(prefixe_1)
                    print(l_prefixes_AS_1)
                
                if v["AS"] == "2":
                    if prefixe_1 not in l_prefixes_AS_2:
                        l_prefixes_AS_2.append(prefixe_1)
                    print(l_prefixes_AS_2)

            
                # si routeur de bord : eBGP
                if v["AS"] != r.AS :
                    for n in r.voisins:
                        if len(n["Adresse"])== 18:
                            adresse = n["Adresse"][:15] 
                            #print(adresse)
                        else:
                            adresse = n["Adresse"][:16] 
                            #print(adresse) 
                        eBGP(r.nom,adresse, n["AS"],r.AS,tn)

                        if len(n["Adresse"]) == 18:
                            if n["Adresse"][9] == '3':
                                prefixe = n["Adresse"][:12]+"::/64"
                                #print(prefixe)
                            else:
                                prefixe = n["Adresse"][:11]+":/64"
                                #print(prefixe)
                        else:
                            if n["Adresse"][9] == '3':
                                prefixe = n["Adresse"][:13]+"::/64"
                                #print(prefixe)
                            else:
                                prefixe = n["Adresse"][:12]+":/64"
                                #print(prefixe)
                        eBGP_adv(r.nom, r.AS, prefixe,tn)

                        if n["AS"]!= r.AS:
                            if len(n["Adresse_v"])== 18:
                                adresse_v = n["Adresse_v"][:15] 
                                #print(adresse_v)
                            else:
                                adresse_v = n["Adresse_v"][:16] 
                                #print(adresse_v) 
                            eBGP(r.nom,adresse_v, n["AS"],r.AS,tn)

            print("configuration de l'iBGP")
            for t in self.liste : 
                    if t.AS == r.AS and t.nom != r.nom :
                        loop = t.loopback[:7]
                        iBGP(r.nom,loop,r.AS,tn)
            tn.write(bytes("end\r",encoding= 'ascii'))
        """
        for r in self.liste:
            print("le routeur traité est:",r.nom)
            print("configuration du routeur en BGP")
            routeur_config = self.dico_routeurs[r.nom]

            tn = telnetlib.Telnet(routeur_config[0],routeur_config[1])
            tn.write(bytes("clear bgp ipv6 unicast *\r",encoding= 'ascii'))
            tn.write(bytes("end\r",encoding= 'ascii'))
        """
        print(l_prefixes_AS_1)
        print(l_prefixes_AS_2)
        for r in self.liste :
            print("le routeur traité est:",r.nom)
            print("configuration du routeur en BGP")
            routeur_config = self.dico_routeurs[r.nom]

            tn = telnetlib.Telnet(routeur_config[0],routeur_config[1])
            tn.write(bytes("configure terminal\r",encoding= 'ascii'))
            for v in r.voisins: 
                if v["AS"] != r.AS :
                    if r.AS == "1": 
                        for ad in l_prefixes_AS_1:
                            eBGP_adv(r.nom, r.AS, ad,tn)
                    else:
                        for ad in l_prefixes_AS_2:
                            eBGP_adv(r.nom, r.AS, ad,tn)
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



