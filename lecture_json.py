import json

class Routeur : 
    def __init__(self, nom, id, AS, protocole, loopback, voisins) :
        self.nom = nom
        self.id = id
        self.AS = AS
        self.protocole = protocole
        self.loopback = loopback
        self.voisins = voisins
    def __str__(self) :
        return f"{self.nom} d'ID : {self.id} appartient à l'AS {self.AS}"


f = open("intent_communities.json","r")
content = f.read()
obj=json.loads(content)

routeurs = obj["Routeurs"]

liste_routeurs = []
for r in routeurs :
    r = Routeur(r["Nom"],r["ID"],r["AS"],r["Protocole"],r["Loopback"],r["Voisins"])
    liste_routeurs.append(r)





    
        

    




