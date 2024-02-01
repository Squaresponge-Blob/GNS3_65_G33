from routeurs_config import config_routeur, config_routeur_communities
from gns3fy import Gns3Connector, Project
from Config_routeur_défaut import nom 
from Config_routeur_défaut import * 
from Partie_telnet_classe import *
from fonctions_config import *
from customtkinter import * 
from PIL import Image
#pip install pillow et customtkinter !!!

gns3_server = Gns3Connector(url ="http://localhost:3080")

# Define the lab you want to load and assign the server connector
lab = Project(name=nom, connector=gns3_server)
lab.get()
lab.open()
lab.status

class gui():
    def __init__(self):
        self.app = CTk()
        self.app.geometry ("1700x500")
        self.app.iconbitmap("./interface/gns3.ico")
        self.app.title("Configuration réseau")
        set_appearance_mode("dark")
        set_default_color_theme("./interface/Hades.json") 

        self.widgets(self.app)

    def widgets(self,app):
        #Images des boutons
        self.img = Image.open("./interface/router.png")
        self.img_tel = Image.open("./interface/Putty.png")
        self.img_defaut= Image.open("./interface/defaut.png")

        #Configuration des différents widgets
        self.intro = CTkLabel(master=app, text="Configurer votre réseau avec votre fichier JSON!",font=("Arial",25))
        self.conf_json = CTkLabel(master=app, text="Mettez le chemin d'accès du fichier:",font=("Arial",25))
        self.f = StringVar()
        self.entry_json = CTkEntry(master=app, placeholder_text="Attente de fichier...",width= 300, text_color="black", textvariable=self.f)     
        self.conf_json1 = CTkLabel(master=app, text="Charger votre fichier configuration JSON:",font=("Arial",25))
        self.lancer_conf = CTkButton(master=app, text="Charger JSON",font=("Arial",15),image=CTkImage(dark_image=self.img, light_image=self.img),command=self.Config_JSON_start)
        self.telnet = CTkButton(master=app, text="Lancer Telnet",font=("Arial",15),image=CTkImage(dark_image=self.img_tel, light_image=self.img_tel),command=self.Config_JSON__tel_start)
        self.defaut = CTkButton(master=app, text="Config Défaut",font=("Arial",15),image=CTkImage(dark_image=self.img_defaut, light_image=self.img_defaut),command=self.Config_defaut)

        #tabview1
        self.tabview1 = CTkTabview(master=app, border_width=2)
        self.textbox = {}
        for node in lab.nodes:
            self.tabview1.add(node.name)
            self.tabview1.tab(node.name).grid_columnconfigure(0,weight=10)
            self.tabview1.tab(node.name).grid_columnconfigure(1,weight=0)
            self.tabview1.tab(node.name).grid_rowconfigure(0,weight=10)
            self.tabview1.tab(node.name).grid_rowconfigure(1,weight=0)
            self.textbox[node.name] = CTkTextbox(master=self.tabview1.tab(node.name),font=("romrmu",15))
            self.textbox[node.name].grid(column=0, row=0, sticky=NSEW)
                    
        #frame2
        self.frame2 = CTkFrame(master=app, border_width=2)
        self.tabview2 = CTkTabview(master=self.frame2, border_width=2)
        self.frame2.grid_columnconfigure((0,1),weight=0)
        self.frame2.grid_columnconfigure((2,3),weight=1)
        self.frame2.grid_rowconfigure((0,1,2,3),weight=1)
        self.bouton3 = CTkButton(master=self.frame2, text="Communities",font=("Arial",15),image=CTkImage(dark_image=self.img, light_image=self.img),command=self.BGP_Policies).grid(column=0, row=0,sticky= N, pady = 10, padx= 10)
        self.bouton4 = CTkButton(master=self.frame2, text="Telnet Communities",font=("Arial",15),image=CTkImage(dark_image=self.img_tel, light_image=self.img_tel),command=self.BGP_Tel_Policies).grid(column=1, row=0,sticky= N, pady = 10, padx= 10)
        self.tabview2.grid(column=0, row=1, sticky= NSEW, pady= 10, columnspan=4, rowspan=4)
        lab1 = Project(name="communities", connector=gns3_server)
        lab1.get()
        lab1.open()
        self.textbox1 = {}
        for nodes in lab1.nodes:
            self.tabview2.add(nodes.name)
            self.tabview2.tab(nodes.name).grid_columnconfigure(0,weight=10)
            self.tabview2.tab(nodes.name).grid_columnconfigure(1,weight=0)
            self.tabview2.tab(nodes.name).grid_rowconfigure(0,weight=10)
            self.tabview2.tab(nodes.name).grid_rowconfigure(1,weight=0)
            self.textbox1[nodes.name] = CTkTextbox(master=self.tabview2.tab(nodes.name),font=("romrmu",15))
            self.textbox1[nodes.name].grid(column=0, row=0, sticky=NSEW)

        #On configure la grid
        self.intro.grid(column=0, row=0, sticky= NW, padx=0.5, pady=0.5, columnspan=2)
        self.conf_json.grid(column=0, row=1, sticky= NW, padx=0.5,pady=0.5)
        self.entry_json.grid(column=1, row=1, sticky= NW, pady=0.5,columnspan=2)
        self.conf_json1.grid(column=0, row=2, sticky= NW, padx=0.5, pady=0.5)
        self.lancer_conf.grid(column=1, row=2, sticky= NW, padx=0.5, pady=0.5)
        self.telnet.grid(column=2, row=2, sticky= NW, padx=0.5, pady=0.5)
        self.defaut.grid(column=3, row=2, sticky= NW, padx=0.5, pady=0.5)
        self.tabview1.grid(column=0, row=3, sticky= NSEW, pady= 10, columnspan=5)
        self.frame2.grid(column=5, row=0, sticky= NSEW, pady= 10,rowspan= 4)

        app.grid_columnconfigure((0,1,2), weight=0)
        app.grid_columnconfigure((3,4), weight=2)
        app.grid_columnconfigure(5, weight=3)
        app.grid_rowconfigure((0,1,2), weight=1)
        app.grid_rowconfigure(3, weight=3)

    def BGP_Policies(self):
        routeur = 1
        lab1 = Project(name="communities", connector=gns3_server)
        lab1.get()
        lab1.open()
        config_routeur_communities(lab1)
        for nodes in lab1.nodes:
            
            self.textbox1[nodes.name].delete("0.0", "end")
            chemin = nodes.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
            f = open(chemin,"rt")
            content = f.read()
            self.textbox1[nodes.name].insert("0.0", content)
            routeur += 1
        lab1.close()

    def BGP_Tel_Policies(self):
        lab1 = Project(name="communities", connector=gns3_server)
        lab1.get()
        lab1.open()
        l,d = Config(self.f.get()[1:len(self.f.get())-1],lab1)
        x = GNS3_telnet(l,d)
        x.BGP_Policies()
        for nodes in lab1.nodes:
            self.textbox1[nodes.name].delete("0.0", "end")
            tn = telnetlib.Telnet(nodes.console_host,str(nodes.console))
            time.sleep(0.5)
            res = tn.read_very_eager().decode('utf-8')
    
            self.textbox1[nodes.name].insert("0.0", res)
        

    def Config_JSON_start(self):
        config_routeur(lab)
        routeur = 1
        for node in lab.nodes:
            self.textbox[node.name].delete("0.0", "end")
            chemin = node.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
            f = open(chemin,"rt")
            content = f.read()
            self.textbox[node.name].insert("0.0", content)
            routeur += 1
                
    def Config_JSON__tel_start(self):
        l,d = Config(self.f.get()[1:len(self.f.get())-1],lab)
        x = GNS3_telnet(l,d)
        x.IPv6_LOOP_RIP_OSPF()
        x.BGP()
        for node in lab.nodes:
            self.textbox[node.name].delete("0.0", "end")
            tn = telnetlib.Telnet(node.console_host,str(node.console))
            time.sleep(0.5)
            res = tn.read_very_eager().decode('utf-8')
            
            self.textbox[node.name].insert("0.0", res)
    
    def Config_defaut(self):
        routeur = 1
        for node in lab.nodes: 
            self.textbox[node.name].delete("0.0", "end")

            chemin = node.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
            routeur += 1
            f = open(chemin,"wt")
            f.write(Defaut(node.name))
            f = open(chemin,"r")
            self.textbox[node.name].insert("0.0", f.read())
        
        lab1 = Project(name="communities", connector=gns3_server)
        lab1.get()
        lab1.open()

        for node in lab1.nodes: 
            self.textbox1[node.name].delete("0.0", "end")

            chemin = node.node_directory + "/configs/i"+str(routeur)+"_startup-config.cfg"
            routeur += 1
            f = open(chemin,"wt")
            f.write(Defaut(node.name))
            f = open(chemin,"r")
            self.textbox1[node.name].insert("0.0", f.read())
            
      
#Lance le GUI 
if __name__ == "__main__":
    x = gui()
    x.app.mainloop()




