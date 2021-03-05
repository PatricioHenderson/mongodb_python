#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import json

import tinymongo as tm
import tinydb

# Bug: https://github.com/schapman1974/tinymongo/issues/58
class TinyMongoClient(tm.TinyMongoClient):
    @property
    def _storage(self):
        return tinydb.storages.JSONStorage

db_name = 'secundaria'


def clear():
    conn = TinyMongoClient()
    db = conn[db_name]

    # Eliminar todos los documentos que existan en la coleccion estudiante
    db.estudiante.remove({})

    # Cerrar la conexión con la base de datos
    conn.close()


def fill():
    print('Completemos esta tablita!')
    # Llenar la coleccion "estudiante" con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto completado por mongo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> nombre de su tutor

    # Se debe utilizar la sentencia insert_one o insert_many.
    
    conn = TinyMongoClient()
    db = conn[db_name]

    estudiante1 = {'name' : 'Armani', 'age' : 33 , 'grade' : 1 , 'tutor': 'Barovero'}
    estudiante2 = {'name' : 'Montiel', 'age' : 24 , 'grade' : 2 , 'tutor': 'Mercado'}
    estudiante3 = {'name' : 'Diaz', 'age' : 27 , 'grade' : 3 , 'tutor': 'Maidana'}
    estudiante4 = {'name' : 'Pionla', 'age' : 38 , 'grade' : 4 , 'tutor': 'Funes Mori'}

    estudiantes = (estudiante1, estudiante2, estudiante3, estudiante4)

    for i in estudiantes:
        db.estudiante.insert_one(i)

    conn.close()

def show():
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Utilizar la sentencia find para imprimir en pantalla
    # todos los documentos de la DB
    # Queda a su criterio serializar o no el JSON "dumps"
    #  para imprimirlo en un formato más "agradable"

    conn = TinyMongoClient()
    db = conn[db_name]
    
    cursor = db.estudiante.find()
    data = list(cursor)
    json_string = json.dumps(data,indent=4)
    print(json_string)

    for i in cursor:
        print(i)

    conn.close()


def find_by_grade(grade):
    print('Operación búsqueda!')
    # Utilizar la sentencia find para imprimir en pantalla
    # aquellos estudiantes que se encuentra en en año "grade"

    # De la lista de esos estudiantes debe imprimir
    # en pantalla unicamente los siguiente campos por cada uno:
    # id / name / age

    conn = TinyMongoClient()
    db = conn[db_name]

    cursor = db.estudiante.find({'grade' : grade})
    data = list(cursor)
    
    
    filtrado = [{'name': x['name'],'age':x['age'],'_id':x['_id']} for x in data]
    
    print(filtrado)
    
    
    
    conn.close()


def insert(student):
    print('Nuevos ingresos!')
    # Utilizar la sentencia insert_one para ingresar nuevos estudiantes
    # a la secundaria

    # El parámetro student deberá ser un JSON el cual se inserta en la db

    conn = TinyMongoClient()
    db = conn[db_name]

    db.estudiante.insert_one(student)

    data = db.estudiante.find()

    for i in data:
        print(i)


    conn.close()


def count(grade):
    print('Contar estudiantes')
    # Utilizar la sentencia find + count para contar
    # cuantos estudiantes pertenecen el grado "grade"

    conn = TinyMongoClient()
    db = conn[db_name]

    print(db.estudiante.find({'grade' : grade}).count())

    conn.close()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    # Borrar la db
    clear()

    fill()
    show()

    grade = 3
    find_by_grade(grade)

    student = {'name' : 'Casco', 'age' : 33 , 'grade' : 5 , 'tutor': 'Vangioni'}
    insert(student)

    count(grade)
