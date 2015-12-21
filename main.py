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
    conn = psycopg2.connect("dbname=postgres user=postgres host=localhost password=cattelan")
    cur = conn.cursor()
except:
    print ("I am unable to connect to the database")

#deleteTable('activities',cur)
if not existsTable('activities',cur):
    cur.execute("CREATE TABLE activities (id serial PRIMARY KEY, datetime timestamp,activity int, person_id int, created_at timestamp,updated_at timestamp);")
    print('New table created')


#deleteTable("test",cur)






jawboneMoves('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450',1,'activities',cur)
conn.commit()
#jawboneSleep('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450')
#jawboneHeart('0NIN0D_htj0','aac3f063d18489fc2e3fa3dabbd5c01a120fa450')
#horaTeste = datetime.datetime.now() + timedelta(hours=1)
horaTeste = datetime.datetime.now() + timedelta(minutes=0)

#chamar as funçõs no laço, dentro do try/exept

while True:
    #yesterday = datetime.datetime(2015, 5, 12, 23, 30)
    #linha = str(datetime.datetime.now())+ ';' + weather("porto alegre", True)
    #if(datetime.time == )
    #print (str(datetime.datetime.now().minute) + ' ' + str(horaTeste.minute))
    #if datetime.now().hour == horaTeste.hour:

    #apenas para teste, conta o tempo na tela
    sys.stdout.write('\r' + str(datetime.datetime.now().second))
    #####
    if datetime.datetime.now().minute == horaTeste.minute:
        #try:
        data = weather('porto alegre', True)
        linha = '\nData:' + str(datetime.datetime.utcfromtimestamp(data[0])) + '\nMaior Temperatura: ' + str(data[1]) +'\nTemperatura Média(ATUAL): ' + str(data[2]) + '\nMenor Temperatura: ' + str(data[3]) + '\nPrecipitacao: ' + str(data[4]) + '\nEventos: ' + '\nperson_id(?): ' + '\nCreated At: ' + '\nUpdated At: ' #melhor forma de fazer isso?
        print  (linha)
        #addWeatherElements('test',weather('porto alegre',True))
        
        #horaTeste = datetime.datetime.now() + timedelta(hours=1)
        horaTeste = datetime.datetime.now() + timedelta(minutes=1)
            
            #conn.commit()
        #except:
         #   print ("Fail to connect") 
         #   data = weather('porto alegre', False)
         #   linha = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')+ ';' + data[0] + ';' + data[1] #melhor forma de fazer isso?
         #   print  (linha)
            #addWeatherElements('test',weather('porto alegre',False))
            #horaTeste = datetime.datetime.now() + timedelta(hours=1)
         #   horaTeste = datetime.datetime.now() + timedelta(minutes=1)
            
            #conn.commit()
    #time.sleep(60) #levar em conta o tempo para baixar os dados? (simultaneamente ou um depois do outro?)
   # id  |    date    | max_temperature | mean_temperature | min_temperature | precipitation |          events           | person_id |         created_at         |         updated_at







#print(weather('porto alegre',True))