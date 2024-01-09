import json

f = open("test.json","r")
content = f.read()
obj=json.loads(content)

routeurs = obj["Routeurs"]

for r in routeurs :
    print(r["Nom"])



    




