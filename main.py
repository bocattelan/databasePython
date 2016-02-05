#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

from functions import *

import psycopg2
import urllib.parse
import urllib.request
import json
import time
import datetime
import sched
from datetime import timedelta
import sys



#INICIO DO CORPO DO PROGRAMA //////////////////////////////////////////////

try:
    #conn = psycopg2.connect("dbname=everydayvis_development user=postgres host=localhost")
    conn = psycopg2.connect("dbname=postgres user=postgres host=localhost password=cattelan")
    cur = conn.cursor()
except:
    print ("I am unable to connect to the database")

#deleteTable('activities',cur)
if not existsTable('activities',cur):
    cur.execute("CREATE TABLE activities (id serial PRIMARY KEY, datetime timestamp,activity int, person_id int, created_at timestamp,updated_at timestamp);")
    print('New table created')

if not existsTable('weathers',cur):
    cur.execute("CREATE TABLE weathers (id serial PRIMARY KEY, date timestamp,max_temperature int, mean_temperature int, min_temperature int, precipitation int, events varchar(255), person_id int,  created_at timestamp,updated_at timestamp);")
    print('New table created')

if not existsTable('locations',cur):
    cur.execute("CREATE TABLE locations (id serial PRIMARY KEY, datetime timestamp,name varchar(255), city varchar(255), country varchar(255), latitude float, longitude float, person_id int,  created_at timestamp,updated_at timestamp);")
    print('New table created')


#code: nil, identity: nil, name: "Cattelan", gender: nil, age: nil, created_at: "2016-01-15 15:33:19", updated_at: "2016-01-15 16:38:18", user_id: 10, jawbone_token: "DudD7GQwFneq_wQM__nChaaNfvpKhnpePZJXREh5iPlscEl9dE...", fitbit_token: "eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0NTUzODQ5OTIsInNjb...", foursquare_token: "XS1HHU2VFRG2ANFGKENLWMKNRUCLIRGLHBILWL1TXMCW3WXF">

#if not existsTable('people',cur):
    #cur.execute("CREATE TABLE people (id serial PRIMARY KEY,code varchar[255], identity varchar[255], name varchar[255], gender varchar[255], age varchar[255], created_at timestamp, updated_at timestamp, user_id int, jawbone_token varchar[255],fitbit_token varchar(255), foursquare_token varchar(255));")
    #print('New table created')

#deleteTable("test",cur)




fitbitMoves("eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0NTUzODQ5OTIsInNjb3BlcyI6InJ3ZWkgcnBybyByaHIgcmxvYyBybnV0IHJzbGUgcnNldCByYWN0IHJzb2MiLCJzdWIiOiIzV1c3NloiLCJhdWQiOiIyMjlaNzciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJpYXQiOjE0NTI4NzM5ODN9.EcIFmeovGBKVD92Xs6zxgkHlYuLAZv06Xv32iDr9QwI"
,'bruno','activities',cur)
horaTeste = datetime.datetime.now() + timedelta(seconds=0)

#chamar as funçõs no laço, dentro do try/exept
horaInicio = datetime.datetime.now()
while True:
    #yesterday = datetime.datetime(2015, 5, 12, 23, 30)
    #linha = str(datetime.datetime.now())+ ';' + weather("porto alegre", True)
    #if(datetime.time == )
    #print (str(datetime.datetime.now().minute) + ' ' + str(horaTeste.minute))
    #if datetime.now().hour == horaTeste.hour:

    #apenas para teste, conta o tempo na tela
    
    #####   
    #print (peopleList[0][0])
    if datetime.datetime.now().date() == horaTeste.date():
        peopleList = getPeopleList(cur)
        for person in peopleList:
            #foursquare("OQLGPMDLAZ25JAZE5VW5DRF0SOOSWLCXQMEED5IZSLBBQN3U",'21', 'locations',cur,conn)
            print(person[3])
            if person[11] != None:
                #foursquare(person[11],person[0], 'locations',cur,conn)
                conn.commit()
                #jawboneMoves('oJu-seHwrstYgtTAQpuUxycYC84VDTuWUUjXiXCc2yhDhJTENkwuyJtiaaIX-06Pitl9KvYhBDiSYPnWZGqRFVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP',1,'activities',cur)
            if person[9] != None:
                #jawboneMoves(person[9],person[0],'activities',cur)
                conn.commit()
            if person[10] != None:
                fitbitMoves(person[10],person[0],'activities',cur)
    #jawboneSleep('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450')
            weather('porto alegre','21','weathers',cur)
            conn.commit()

        horaTeste = datetime.datetime.now() + timedelta(days=1)
    sys.stdout.write('\r' + 'Inicio do programa: ' + str(horaInicio) + ' Tempo atual: ' +str(datetime.datetime.now()))