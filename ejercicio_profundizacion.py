

import json
import requests
import tinymongo as tm
import tinydb

# Bug: https://github.com/schapman1974/tinymongo/issues/58
class TinyMongoClient(tm.TinyMongoClient):
    @property
    def _storage(self):
        return tinydb.storages.JSONStorage

db_name = 'profundizacion'

def clear():
    conn = TinyMongoClient()
    db = conn[db_name]

    db.estudiantes.remove({})

    conn.close()

def fill():
    conn = TinyMongoClient()
    db = conn[db_name]
    
    url = 'https://jsonplaceholder.typicode.com/todos'
    response = requests.get(url)
    data = json.loads(response.text)
    data = response.json()

    db.estudiantes.insert_many(data)
    conn.close()

    '''
    ## title_completed_count(userId)
    Deben crear una función que lea la DB (find) y cuente (count) cuantos usuarios con "userId" han completado sus títulos.
    Para esto sentencia "find" de Mongo deberá tener dos campos condicionales (userId y completed) y utilizar el método count
    para contar los casos favorables.
    '''
def title_completed_count(userId):
    conn = TinyMongoClient()
    db = conn[db_name]
    print(db.estudiantes.find({'userId': userId ,'completed':True}).count())
    
    cursor = db.estudiantes.find()
    data = list(cursor)

    filter_data = [{x['userId'] } for x in data if x.get('completed')is True]
    
    
    data = {}
    for i in filter_data:
        if (i in data) == False:
            data[i] = 0
        data[i] += 1
    users = []
    cursos= []
    for i in data:
        print("El usuario {} realizo {}  cursos".format(i,data[i]))
        
        users.append(i)
        cursos.append(data[i])

    conn.close()
    
if __name__ == "__main__":
  # Borrar DB
  clear()

  # Completar la DB con el JSON request
  fill()

  #Buscar autor
  userId = 5
  title_completed_count(userId)


