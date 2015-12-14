#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#



import psycopg2
import urllib.parse
import urllib.request
import json
import time
import datetime
import sched
from datetime import timedelta
import sys

#pega os dados de uma cidade
def weather (cidadeInput, internetConnection):
    cidade = cidadeInput 
    cidade = cidade.split(' ')
    if internetConnection:
        if len(cidade) >=  2:
            url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87&units=metric'
        else:
            url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '&APPID=c202fefe29158aebc3cd656900708e87&units=metric'
        #print ("Requisitando acesso aos dados")
        request = urllib.request.Request(url)
        encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
        data = (urllib.request.urlopen(request).read().decode(encoding))
        dadosTempo = json.loads(data)
        print (dadosTempo)
        return [dadosTempo['list'][0]['dt'],dadosTempo['list'][0]['main']['temp_max'],dadosTempo['list'][0]['main']['temp'],dadosTempo['list'][0]['main']['temp_min']]
    else:
        return ['-']


#SQL /////////////////////////////////////////////////////////////////////////////////////////////
#dado um nome de tabela retorna verdadeiro se existe
def existsTable(tableName):
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('test',))
    return cur.fetchone()[0]

def printTable(tableName,cur):
    if existsTable(tableName):
        cur.execute("SELECT * FROM " + tableName)
        cur.fetchone()
        for row in cur:
            print(row)
#dado um nome de tabela e um json ele salva na tabela
def addWeatherElements(tableName,elements):
    if existsTable(tableName):
        query = "INSERT INTO " + tableName
        cur.execute(query + "(cidade, temperatura) VALUES (%s, %s)",elements)

def deleteTable(tableName):
    if existsTable(tableName):
        cur.execute("DROP TABLE " + tableName + " ;")
        print("Table '"+ tableName +"' deleted")



#INICIO DO CORPO DO PROGRAMA //////////////////////////////////////////////

try:
    conn = psycopg2.connect("dbname=postgres user=postgres host=localhost password=cattelan")
    cur = conn.cursor()
except:
    print ("I am unable to connect to the database")

if not existsTable('test'):
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, cidade varchar, temperatura float);")
    print('New table created')


#deleteTable("test")







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
        linha = '\nData:' + str(datetime.datetime.utcfromtimestamp(data[0])) + '\nMaior Temperatura: ' + str(data[1]) +'\nTemperatura Média(ATUAL): ' + str(data[2]) + '\nMenor Temperatura: ' + str(data[3]) + '\nPrecipitacao'#melhor forma de fazer isso?
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