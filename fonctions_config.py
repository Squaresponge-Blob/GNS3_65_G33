import gns3fy
from tabulate import tabulate
import telnetlib
import time 
import json
from ipaddress import IPv6Address, ip_network

# Define the server object to establish the connection
gns3_server = gns3fy.Gns3Connector(url ="http://localhost:3080")

# Define the lab you want to load and assign the server connector
lab = gns3fy.Project(name="Projet", connector=gns3_server)
# Retrieve its information and display
lab.get()
lab.open()
lab.status
lab.stats


def find_ad(a, b, liste_routeurs) : 
    """
    trouve l'adresse du routeur a sur l'interface où il est connecté à b
    """
    for r in liste_routeurs :
        if r.nom == b :
            for v in r.voisins :
                if v["Nom"] == a :
                    return v["Adresse"]


def routeurBord(r) :
    for v in r.voisins : 
        if v["AS"] != r.AS :
            return True
    return False




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
    config += " ipv6 rip ripng enable\n!\n"
    return config

def Int_OSPF(config):
    config += " ipv6 ospf 1 area 0\n !\n"
    return config 

def Int_OSPF_cost(config, cost):
    config += f" ipv6 ospf cost {cost}\n"
    return config

def Config_Loop(config,Int,adresse):
    config += f"interface {Int}\n no ip address\n ipv6 address {adresse}\n ipv6 enable\n"
    return config
     
def Config_int_passif(config,Int):
    config += f"router ospf 1\n passive-interface {Int}\n!\n"
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
    config += f" !\n address-family ipv4\n exit-address-family\n !\n address-family ipv6\n"
    return config

def Config_BGP_adv(config, network) :
    config += f"  network {network}\n"
    return config

def Config_BGP_activate(config, adresse):
    config += f"  neighbor {adresse} activate\n"
    return config

def Neighbor_community(config,adresse,status):
    config += f"  neighbor {adresse} send-community\n neighbor {adresse} route-map tag-{status} in\n"
    return config

def Neighbor_filter(config,adresse) :
    config += f"  neighbor {adresse} route-map filter out\n"
    return config

def Config_BGP_exit(config):
    config += f" exit-address-family\n!\nip forward-protocol nd\n!\n"
    return config

def Config_community_start(config) :
    config +=f"ip bgp-community new-format\n"
    return config

def Create_community(config,status,value) :
    config += f"ip community-list standard {status} permit {value}\n"
    return config

def Config_community_exit(config):
    config += "!\nno ip http server\n no ip http secure-server\n!\n"
    return config

def Config_RIP(config): 
    config += "ipv6 router rip ripng\n redistribute connected\n"
    return config

def Config_OSPF(config,id):
    config += f"ipv6 router ospf 1\n router-id {id}\n"
    return config

def Route_map_tag(config,name,loc_pref) :
    config +=f"route-map {name} permit 10\n set local-preference {loc_pref}\n set community 1:{loc_pref}\n!\n"
    return config

def Route_map_filter(config):
    config +=f"route-map filter permit 10\n match community client\n!\n"
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


           

