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
    for node in lab.nodes: 
        node.get()
        chemin = node.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
        print(chemin)
        routeur += 1
        f = open(chemin,"wt")
        f.write

x = fichier_cfg()        
        