#/usr/bin/ect python3
import gns3fy 
from tabulate import tabulate
import telnetlib
import time 
import json


# Define the server object to establish the connection
gns3_server = gns3fy.Gns3Connector(url ="http://localhost:3080")

# Define the lab you want to load and assign the server connector
lab = gns3fy.Project(name="TEST", connector=gns3_server)

print(
        tabulate(
            gns3_server.projects_summary(is_print=False),
            headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
        )
    )

# Retrieve its information and display
lab.get()
print(lab)


# Access the project attributes
print(f"Name: {lab.name} -- Status: {lab.status} -- Is auto_closed?: {lab.auto_close}\n")

# Open the project
lab.open()
lab.status

# Verify the stats
lab.stats
#nb_as = int(input("Combien d'AS désirez-vous?"))
#while type(nb_as) != int or nb_as < 0 :
#   nb_as = int(input("Erreur mettez un entier, combien d'AS désirez-vous?"))

nb_routeur = 0
snb_routeur = "1"

# List the names and status of all the nodes in the project
for node in lab.nodes:
    int = 1
    print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}\n")
    entete = "2001:100:1:"
    fin = "::"
    node.get()#récupère les informations du noeud

    tn = telnetlib.Telnet(node.console_host,str(node.console))

    tn.write(bytes("configure terminal\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 unicast-routing\r",encoding= 'ascii'))
    for i in range(len(node.links)):
        adresse = entete + snb_routeur + fin 
        link = node.links[i]
        print(link.nodes[i])
        print(len(link.nodes[i]))
        for k in range (len(link.nodes[i])-2):#-2 car link.nodes[i] contient le lien dans les deux sens 
            if link.nodes[k]["node_id"] == node.node_id:
                interface = link.nodes[k]["label"]["text"]
                print(interface)
                tn.write(bytes("int "+interface+"\r",encoding= 'ascii'))
                tn.write(bytes("ipv6 enable\r",encoding= 'ascii'))
                tn.write(bytes("ipv6 address " + adresse + str(int) +"/64\r",encoding= 'ascii'))
                tn.write(bytes("no shutdown\r",encoding= 'ascii'))
                tn.write(bytes("exit\r",encoding= 'ascii'))
                int += 1
                nb_routeur += 1
    snb_routeur = str(nb_routeur)
    tn.write(bytes("end\r",encoding= 'ascii'))