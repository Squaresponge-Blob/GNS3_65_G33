import gns3fy
from tabulate import tabulate
import telnetlib
import time 
import json
from ipaddress import IPv6Address, ip_network


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

nb_interconnexion = 0
snb_interconnexion = "1"

# List the names and status of all the nodes in the project
sub_asx = "2001:100:1:1::/64"
sub_asy = "2001:100:2:1::/64"
asx_asy = "2001:100:4:1::/64"

sub_asx = ip_network(sub_asx)
sub_asy = ip_network(sub_asy)
asy_asx = ip_network(asx_asy)

"""for addresse in sub_asx:
    print(addresse)
    if addresse == IPv6Address("2001:100:1::2"):
        break
    time.sleep(1)
"""

lien_parcouru = []
adresses_routeur = {}
num_r = 1
list = []

for node in lab.nodes: #récupère les id de chaque lien 
    node.get()
    for i in range(len(node.links)):
        link = node.links[i]
        if link.link_id not in list: 
            list.append(link.link_id)
            print(list)

for lien in list: #crée un dictionnaire associant les id des liens et leurs masques d'adresse ip respectives 
    adresses_routeur[lien] = "2001:100:1:"+str(num_r)+"::"
    num_r += 1    
print(adresses_routeur)
    
for node in lab.nodes:        
    node.get()#récupère les informations du noeud
    node.start()
    print(node.node_directory) #Important le fichier config a pour chemin node.node_directory + configs
    print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}\n")
    
    tn = telnetlib.Telnet(node.console_host,str(node.console))
    tn.write(bytes("\r",encoding= 'ascii'))
    tn.write(bytes("\r",encoding= 'ascii'))
    tn.write(bytes("\r",encoding= 'ascii'))
    tn.write(bytes("configure terminal\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 unicast-routing\r",encoding= 'ascii'))
    
    for i in range(len(node.links)):
        link = node.links[i]
        #print(link)
        sub = adresses_routeur[link.link_id] + "/64"
        sub = ip_network(sub)
        for k in range (2):#car link.nodes[i] contient le lien dans les deux sens
                    if link.nodes[k]["node_id"] == node.node_id: 
                        interface = link.nodes[k]["label"]["text"]
                        print(interface)
                        print(sub[k]+1)
                    
                        tn.write(bytes("int "+ interface+"\r",encoding= 'ascii'))
                        tn.write(bytes("ipv6 enable\r",encoding= 'ascii'))
                        tn.write(bytes("ipv6 address " + str(sub[k] + 1) +"/64\r",encoding= 'ascii'))
                        time.sleep(1)
                        tn.write(bytes("no shutdown\r",encoding= 'ascii'))
                        tn.write(bytes("exit\r",encoding= 'ascii'))

    tn.write(bytes("end\r",encoding= 'ascii'))
    #res = tn.read_very_eager().decode('utf-8')
    #print(res)

  