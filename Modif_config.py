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

def Great_Explosion_Murder_God_Dynamight():
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
    return adresses_routeur
     

def fichier_cfg():
    adresses_routeur = Great_Explosion_Murder_God_Dynamight()
    routeur = 1 
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


def Config_debut(config, nom) :
    config += f"""!
!

!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname {nom}
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
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
"""
    return config

def Config_interface(config,Int,adresse):
    config += f"interface {Int}\n no ip address\n negotiation auto\n ipv6 address {adresse}\n ipv6 enable\n"
    return config

def Int_RIP(config):
    config += " ipv6 rip ripng enable\n!"
    return config

def Int_OSPF(config):
    config += " ipv6 ospf 1 area 0\n !"
    return config 

def Config_Loop(config,Int,adresse):
    config += f"interface {Int}\n no ip address\n ipv6 address {adresse}\n ipv6 enable\n"
    return config
     
def Config_int_passif(config,Int):
    config += f"router ospf 1\n passive-interface {Int}\n!"
    return config 

def Config_BGP(config, AS, id):
    config += f"router bgp {AS}\n bgp router-id {id}\n bgp log-neighbor-changes\n no bgp default ipv4-unicast\n"
    return config
     
def Config_BGP_neighbor(config,adresse,AS):
    config += f" neighbor {adresse} remote-as {AS}\n"
    return config

def Config_iBGP(config,adresse):
    config += f" neighbor {adresse} update-source Loopback0\n"
    return config

def Config_BGP2(config):
    config += f" !\n address-family ipv6\n"
    return config

def Config_BGP_adv(config, network) :
    config += f"  network {network}"
    return config

def Config_BGP_activate(config, adresse):
    config += f"  neighbor {adresse} activate\n"
    return config

def Config_BGP_exit(config):
    config += f" exit-address-family\n!\nip forward-protocol nd\n!\n!\nno ip http server\n no ip http secure-server\n!\n"
    return config

def Config_RIP(config): 
    config += "ipv6 router rip ripng\n redistribute connected\n"
    return config

def Config_OSPF(config,id):
    config += f"ipv6 router ospf 1\n router-id {id}\n"
    return config

def Config_fin(config):
    config += f"!\n!\n!\n!\ncontrol-plane\n!\n!\nline con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline vty 0 4\n login\n!\n!\nend"
    return config

def Ecrire_dans_fichier(config, nom):
    routeur = 1
    for node in lab.nodes: 
        node.get()
        if nom == node.name:
            chemin = node.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
        routeur += 1
    f = open(chemin,"wt")
    f.write(config)

        
           

