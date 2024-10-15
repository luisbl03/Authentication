import json

file = json.loads(open('prueba.json').read()) #devuleve una lista de diccionarios

print(file[0]["nombre"]) #primero accedemos al usuario y despues al parametro a buscar

file.append({"nombre": "Juan", "edad": 25, "ciudad": "Madrid"}) #añadimos un nuevo usuario
print(file)

#guardar en el archivo
with open('prueba.json', 'w') as f:
    json.dump(file, f) #guardamos la lista de diccionarios en el archivo