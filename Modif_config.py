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

# Access the project attributes
print(f"Name: {lab.name} -- Status: {lab.status} -- Is auto_closed?: {lab.auto_close}\n")

# Open the project
lab.open()
lab.status

# Verify the stats
lab.stats

def fichier_cfg():
    routeur = 1
    num_r = 1
    list = []
    adresses_routeur = {}

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
        node.get()
        chemin = node.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
        print(chemin)
        routeur += 1
        f = open(chemin,"wt")
        for i in range(len(node.links)):
            link = node.links[i]
            sub = adresses_routeur[link.link_id] + "/64"
            sub = ip_network(sub)
            for k in range (2):#car link.nodes[i] contient le lien dans les deux sens
                        if link.nodes[k]["node_id"] == node.node_id: 
                            interface = link.nodes[k]["label"]["text"]
                            conf = f"""!
!
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname {node.name}
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ipv6 unicast-routing
ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
!
interface {interface}
 no ip address
 negotiation auto
 ipv6 address {str(sub[k] + 1)}/64
 ipv6 enable
 ipv6 rip 1 enable
!                         
no cdp log mismatch duplex
!
line con 0
 exec-timeout 0 0
 logging synchronous
 privilege level 15
 no login
line aux 0
 exec-timeout 0 0
 logging synchronous
 privilege level 15
 no login
!
!
end
"""
                            f.write(conf)                       
                            
                            
                            
                            
                            
x = fichier_cfg()        
        