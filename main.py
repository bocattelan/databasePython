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
    conn = psycopg2.connect("dbname=postgres user=postgres host=localhost")
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

#deleteTable("test",cur)





#foursquare("OQLGPMDLAZ25JAZE5VW5DRF0SOOSWLCXQMEED5IZSLBBQN3U",'21', 'locations',cur,conn)
#jawboneMoves('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450',1,'activities',cur)
#jawboneSleep('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450')
#weather('porto alegre', 1,'weathers',cur)
#conn.commit()
#jawboneHeart('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450')
#horaTeste = datetime.datetime.now() + timedelta(hours=1)
horaTeste = datetime.datetime.now() + timedelta(minutes=0)



while True:
    #yesterday = datetime.datetime(2015, 5, 12, 23, 30)
    #linha = str(datetime.datetime.now())+ ';' + weather("porto alegre", True)
    #if(datetime.time == )
    #print (str(datetime.datetime.now().minute) + ' ' + str(horaTeste.minute))
    #if datetime.now().hour == horaTeste.hour:

    #apenas para teste, conta o tempo na tela
    
    #####
    if datetime.datetime.now().hour == horaTeste.hour:
        foursquare("OQLGPMDLAZ25JAZE5VW5DRF0SOOSWLCXQMEED5IZSLBBQN3U",'21', 'locations',cur,conn)
        jawboneMoves('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450',1,'activities',cur)
#jawboneSleep('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450')
        weather('porto alegre', 1,'weathers',cur)
        conn.commit()
       
        horaTeste = datetime.datetime.now() + timedelta(hours=1)
    sys.stdout.write('\r' + str(datetime.datetime.now().time()))
         