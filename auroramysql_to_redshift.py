#!/usr/bin/env python

import boto3
import psycopg2
import pymysql
import csv
import time
import sys
import os
import datetime
from sqlalchemy import create_engine
import pandas as pd
from datetime import date

datetime_object = datetime.datetime.now()

print ("Data Pipeline: Aurora MySQL -> EC2 -> Redshift")
print ("Inicio: ", datetime_object)

'''
PRIMERA PARTE (EXTRACCIÓN):
Se toman los datos de Aurora (tipo MySQL) de las diferentes tablas y se crean archivos CSV,
para ser tratados posteriormente.
'''
def conect_aurora():
    # Parametros de conexión a Aurora MySQL
    dbmysql_opts = {
        'user': 'admin',
        'password': 'ffrb75sol',
        'host': 'fondeadora-instance-1.cfvethvqoo3o.us-east-2.rds.amazonaws.com',
        'database': 'fondeadoradb'
    }

    
    # Conección a Aurora MySQL
    db = pymysql.connect(**dbmysql_opts)
    cur = db.cursor()
    return db, cur

# Función de cone
def aurora_query(db, cur, sql, csv_path): 
    # Intentar realizar la conexión a Aurora 
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        db.close()
    
    # Si hay resultados continúa
    if rows:
        # Variables auxiliares para manipulación de resultados
        result = list()
        column_names = list()
        
        for i in cur.description:
            column_names.append(i[0])
    
        result.append(column_names)
        for row in rows:
            result.append(row)
    
        # Realizar la manipulación en un archivo
        with open(csv_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            for row in result:
                csvwriter.writerow(row)
    else:
        sys.exit("SIN RESULTADOS: {}".format(sql))

# Variables para mandar una búsqueda con la función
db, cur = conect_aurora()
sql = 'SELECT * from rutas'
csv_path = '/home/ubuntu/rutas_file.csv'
aurora_query(db, cur, sql,csv_path)

db, cur = conect_aurora()
sql = 'SELECT * from envios'
csv_path = '/home/ubuntu/envios_file.csv'
aurora_query(db, cur, sql,csv_path)

db, cur = conect_aurora()
sql = 'SELECT * from logistica'
csv_path = '/home/ubuntu/log_file.csv'
aurora_query(db, cur, sql,csv_path)

datetime_object = datetime.datetime.now()
print ("Ingestión Aurora (OK): ", datetime_object)

'''
SEGUNDA PARTE (TRANSFORMACIÓN):
Se crean dos nuevas tablas complementarias a partir de las 3 tablas originales de Aurora DB.
'''
# Lectura de archivos CSV
rutas = pd.read_csv("rutas_file.csv")
envios = pd.read_csv("envios_file.csv")
logis = pd.read_csv("log_file.csv")

# Creación del primer archivo fucionando los envíos con las rutas para añadir entidad federativa
envios_estado = pd.merge(envios, rutas,
                        how='left', left_on=['ciudad_orig', 'ciudad_dest'], right_on=['ciudad_orig', 'ciudad_dest'])
envios_estado = envios_estado.drop(['id_y'], axis = 1)
envios_estado.to_csv('cargo_redshift.csv',encoding='utf-8', index=False)

# Creación del segundo archivo fucionando los envíos con la logistica para añadir entidad federativa
#  y conocer capacidad de carga
rutas_log = pd.merge(rutas, logis,
                        how='left', left_on=['ciudad_orig', 'ciudad_dest'], right_on=['ciudad_orig', 'ciudad_dest'])
rutas_log = rutas_log.drop(['id_y'], axis = 1)
rutas_log.to_csv('rutas_redshift.csv',encoding='utf-8', index=False)

datetime_object = datetime.datetime.now()
print ("Transformación datos (OK): ", datetime_object)

'''
TERCERA PARTE (CARGA):
Las nuevas tablas se envían a Redshift para otros análisis.
'''

#endpoint
conn = create_engine('postgresql://admin:FFrb75%sol@fondeadora.cfqxofvplpaq.us-east-2.redshift.amazonaws.com:5439/dev')

# Envío de la primera tabla a redshift
df = pd.read_csv("cargo_redshift.csv")
df.to_sql('cargo', conn, index=False, if_exists='replace')

# Envío de la primera tabla a redshift
df = pd.read_csv("rutas_redshift.csv")
df.to_sql('rutas', conn, index=False, if_exists='replace')

datetime_object_2 = datetime.datetime.now()

print ("Termino: ", datetime_object)