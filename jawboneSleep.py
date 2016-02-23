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
import calendar
import sched
from datetime import timedelta
import sys



#JAWBONE /////////////\\\\\\\\\\\\\\\\\//////////////////\\\\\\\\\\\\\\\\\\\//////////////////
#pega os dados de uma pessoa


def jawboneSleep(token,person_id,tableName,cur):

    lastDate = getLastDate(tableName,cur)
    try:
        if lastDate[0][0].date() < datetime.datetime.now().date(): 
            url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=' + str(lastDate[0][0].timestamp()) + '&&end_time=' + str(datetime.datetime.now().timestamp())
        else:
            return print('Jawbone Sleeps up to date')
    except:
        url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1383289200'
        #url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1383289200'
        print (url)
    
    while(1):

        
        print ("Requisitando acesso aos dados Sleeps")
        print(token)
        request = urllib.request.Request(url, headers = {"Authorization": "Bearer " + token  })
        response = urllib.request.urlopen(request).getcode()
        if response !=200:
            break
        print("Baixando dados")
        print("Baixados")



        encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
        data = (urllib.request.urlopen(request).read().decode(encoding))
        dadosNedel = json.loads(data)
        
        #json.dump(dadosNedel,arquivo)

        for evento in dadosNedel['data']['items']:
            print(evento['date'])
            urlTicks = 'https://jawbone.com/nudge/api/v.1.1/sleeps/' + evento['xid'] + '/ticks'
            requestTicks = urllib.request.Request(urlTicks, headers = {"Authorization": "Bearer " + token  })
            responseTicks = urllib.request.urlopen(requestTicks).getcode()
            if response !=200:
                break
            encodingTicks = urllib.request.urlopen(requestTicks).info().get_param('charset', 'utf8')
            dataTicks = (urllib.request.urlopen(requestTicks).read().decode(encodingTicks))
            dadosNedelDetalhes = json.loads(dataTicks)
            #aqui o information vai ter todos os ticks de um "move"
            #information.append(dadosNedelDetalhes)
            #print(dadosNedelDetalhes['data']['items'])
            #for i in dadosNedelDetalhes['data']['items']:
                #print(i['steps'])

            #passosIntervalo = 0
            #tempoIntervalo = datetime.datetime.utcfromtimestamp(dadosNedelDetalhes['data']['items'][0]['time_completed'])
            for evento in dadosNedelDetalhes['data']['items']:
                addSleepElement(tableName,[datetime.datetime.utcfromtimestamp(evento['time']),evento['depth'],person_id,datetime.datetime.now(),datetime.datetime.now()],cur)

        if 'links' in dadosNedel['data'].keys():
            url = 'https://jawbone.com' + dadosNedel['data']['links']['next']
            #print('continuando')
        else: 
            #print(information)
            #printTable(tableName,cur)
            print('Jawbone Moves updated')
            return

def jawboneHeart(client_id,client_secret):

    params = {
        "response_type=code" : 'code',
          "client_id": client_id,
          'scope': 'basic_read extended_read location_read move_read',
          'redirect_uri' : ''
        }
    url = "https://jawbone.com/auth/oauth2/token"
    request = urllib.request.Request(url, headers = params)
    #encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
    #data = (urllib.request.urlopen(request).read().decode(encoding))


    information = []
    #arquivo = open('newToken.txt' , 'w+')
    params = {
          "client_id": client_id,
          "client_secret": client_secret,
          "grant_type": 'refresh_token',
          "refresh_token": ''
        }
    url = "https://jawbone.com/auth/oauth2/token"
    request = urllib.request.Request(url, headers = params)

    url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/heartrates?start_time=1441065600&&end_time=1446336000'
    while(1):

        
        print ("Requisitando acesso aos dados Heart Rate")
        request = urllib.request.Request(url, headers = {"Authorization": "Bearer oJu-seHwrstYgtTAQpuUxycYC84VDTuWUUjXiXCc2yhDhJTENkwuyJtiaaIX-06Pitl9KvYhBDiSYPnWZGqRFVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP"  })
        response = urllib.request.urlopen(request).getcode()
        if response !=200:
            break
        print("Baixando dados")
        print("Baixados")



        encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
        data = (urllib.request.urlopen(request).read().decode(encoding))
        dadosNedel = json.loads(data)
        
        #json.dump(dadosNedel,arquivo)

        for evento in dadosNedel['data']['items']:
            print(evento['date'])
            #aqui o information vai ter todos os ticks de um "move"
            information.append(dadosNedel)

        if 'links' in dadosNedel['data'].keys():
            url = 'https://jawbone.com' + dadosNedel['data']['links']['next']
        else: 
            #print(information)
            return information


#SQL /////////////////////////////////////////////////////////////////////////////////////////////
#dado um nome de tabela retorna verdadeiro se existe
def existsTable(tableName,cur):
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (tableName,))
    return cur.fetchone()[0]

def printTable(tableName,cur):
    if existsTable(tableName,cur):
        cur.execute("SELECT * FROM " + tableName)
        cur.fetchone()
        for row in cur:
            print(row)
#dado um nome de tabela e um json ele salva na tabela
def addWeatherElements(tableName,elements,cur):
    if existsTable(tableName,cur):
        query = "INSERT INTO " + tableName
        cur.execute(query + "(date, max_temperature,mean_temperature,min_temperature,precipitation,events,person_id,created_at,updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",elements)

def addMoveElement(tableName,element,cur):
    if existsTable(tableName,cur):
        query = "INSERT INTO " + tableName
        cur.execute(query + "(datetime, activity,person_id,created_at, updated_at) VALUES (%s, %s,%s,%s,%s)",element)

def addSleepElement(tableName,element,cur):
    if existsTable(tableName,cur):
        query = "INSERT INTO " + tableName
        cur.execute(query + "(datetime, depth,person_id,created_at, updated_at) VALUES (%s, %s,%s,%s,%s)",element)


def addFoursquareElement(tableName,element,cur):
    if existsTable(tableName,cur):
        query = "INSERT INTO " + tableName
        cur.execute(query + "(datetime, name,city,country,latitude,longitude,person_id,created_at,updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",element)
 # id  |      datetime       |                             name                              |         city         |    country    |                 latitude                 |                longitude                 | person_id |         created_at         |         updated_at


def deleteTable(tableName,cur):
    if existsTable(tableName,cur):
        cur.execute("DROP TABLE " + tableName + " ;")
        print("Table '"+ tableName +"' deleted")

def getLastDate(tableName,cur):
    if existsTable(tableName,cur) and tableName == 'activities' or tableName == 'locations' or tableName == 'sleeps':
        cur.execute("SELECT MAX(datetime) FROM " + tableName + ";")
        return cur.fetchall()
    elif existsTable(tableName,cur) and tableName == 'weathers':
        cur.execute("SELECT MAX(date) FROM " + tableName + ";")
        return cur.fetchall()

def getPeopleList(cur):
    if existsTable('people',cur):
        cur.execute("SELECT * FROM people;")
        return cur.fetchall()



#////////////////\\\\\\\\\\\\\\\\\\\MAIN///////////////////\\\\\\\\\\\\\\\\\\\\\\\\
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

if not existsTable('sleeps',cur):
    cur.execute("CREATE TABLE sleeps (id serial PRIMARY KEY, datetime timestamp,depth int, person_id int, created_at timestamp,updated_at timestamp);")
    print('New table created')

def jawboneMoves(token,person_id,tableName,cur):



    #encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
    #data = (urllib.request.urlopen(request).read().decode(encoding))
    #dadosNedel = json.loads(data)
    #print (params["refresh_token"])
    #json.dump(data,arquivo)


    #arquivo = open('nedelJawbone.txt', 'w')
    #de setembro 2015 até outubro 2015
    lastDate = getLastDate(tableName,cur)
    if lastDate[0][0] != None:
        if lastDate[0][0].date() < datetime.datetime.now().date(): 
            url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/moves?start_time=' + str(lastDate[0][0].timestamp()) + '&&end_time=' + str(datetime.datetime.now().timestamp())
        else:
            return print('Jawbone Moves up to date')
    else:
        url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/moves?start_time=' + '0' + '&&end_time=' + str(datetime.datetime.now().timestamp())
    #dois dias
    #url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1441065600&&end_time=1441152000'
    while(1):
    #cidade  =  input("Digite o nome da cidade procurada: ")
    #cidade = cidade.split(' ')

    #if len(cidade) >  2:
    #    url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87'
    #else:
        
        
        print ("Requisitando acesso aos dados Moves")
        request = urllib.request.Request(url, headers = {"Authorization": "Bearer " + token  })
        response = urllib.request.urlopen(request).getcode()
        if response !=200:
            break
        print("Baixando dados")
        print("Baixados")



        encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
        data = (urllib.request.urlopen(request).read().decode(encoding))
        dadosNedel = json.loads(data)
        
        #json.dump(dadosNedel,arquivo)

        for evento in dadosNedel['data']['items']:
            print(evento['date'])
            urlTicks = 'https://jawbone.com/nudge/api/v.1.1/moves/' + evento['xid'] + '/ticks'
            requestTicks = urllib.request.Request(urlTicks, headers = {"Authorization": "Bearer " + token  })
            responseTicks = urllib.request.urlopen(requestTicks).getcode()
            if response !=200:
                break
            encodingTicks = urllib.request.urlopen(requestTicks).info().get_param('charset', 'utf8')
            dataTicks = (urllib.request.urlopen(requestTicks).read().decode(encodingTicks))
            dadosNedelDetalhes = json.loads(dataTicks)
            #aqui o information vai ter todos os ticks de um "move"
            #information.append(dadosNedelDetalhes)
            #print(dadosNedelDetalhes['data']['items'])
            #for i in dadosNedelDetalhes['data']['items']:
                #print(i['steps'])

            passosIntervalo = 0
            tempoIntervalo = datetime.datetime.utcfromtimestamp(dadosNedelDetalhes['data']['items'][0]['time_completed'])
            for evento in dadosNedelDetalhes['data']['items']:
                    if datetime.datetime.utcfromtimestamp(evento['time_completed']) > tempoIntervalo:
                        addMoveElement(tableName,[tempoIntervalo,passosIntervalo,person_id,datetime.datetime.now(),datetime.datetime.now()],cur)
                        tempoIntervalo = datetime.datetime.utcfromtimestamp(evento['time_completed']) + timedelta(minutes=10)
                        #print (passosIntervalo)
                        passosIntervalo = 0
                        #salvar coisas aqui no BD

                    #if 'steps' in dadosNedelDetalhes['data']['items'][j].keys():
                    passosIntervalo = passosIntervalo + evento['steps']
                    #print(str(passosIntervalo) + ' ' +str(datetime.datetime.utcfromtimestamp(evento['time_completed'] )))
                    #print(dadosNedelDetalhes['data']['items'][j].keys())
                    #print(dadosNedelDetalhes['data']['items'][j])

        if 'links' in dadosNedel['data'].keys():
            url = 'https://jawbone.com' + dadosNedel['data']['links']['next']
            #print('continuando')
        else: 
            #print(information)
            #printTable(tableName,cur)
            print('Jawbone Moves updated')
            return

#jawboneMoves("oJu-seHwrstYgtTAQpuUx6aNfvpKhnpePZJXREh5iPkOwO__AqDaI_kdShCqzO0sitl9KvYhBDiSYPnWZGqRFVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP",6,"activities",cur)

jawboneSleep("oJu-seHwrstYgtTAQpuUx6aNfvpKhnpePZJXREh5iPkOwO__AqDaI_kdShCqzO0sitl9KvYhBDiSYPnWZGqRFVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP",6,"sleeps",cur)
conn.commit()
