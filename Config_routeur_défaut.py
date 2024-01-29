import gns3fy
from tabulate import tabulate

# Define the server object to establish the connection
gns3_server = gns3fy.Gns3Connector(url ="http://localhost:3080")

# Define the lab you want to load and assign the server connector
lab = gns3fy.Project(name="Projet", connector=gns3_server)

# Retrieve its information and display
lab.get()

# Access the project attributes
print(f"Name: {lab.name} -- Status: {lab.status} -- Is auto_closed?: {lab.auto_close}\n")

# Open the project
lab.open()
lab.status

# Verify the stats
lab.stats

def Defaut(nom):
    config = f"""!
!
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname {nom}
!
ip cef
no ip domain-lookup
no ip icmp rate-limit unreachable
ip tcp synwait 5
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
    return config

routeur = 1
for node in lab.nodes:
    node.get()
    config = Defaut(node.name)
    chemin = node.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
    routeur += 1
    f = open(chemin,"wt")
    f.write(config)