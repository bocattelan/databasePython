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
        return [dadosTempo['list'][0]['dt'],dadosTempo['list'][0]['main']['temp_max'],dadosTempo['list'][0]['main']['temp'],dadosTempo['list'][0]['main']['temp_min'],'-','-','-','-']#dadosTempo['list'][0]['rain']['3h'] ]
    else:
        return ['-']

#JAWBONE /////////////\\\\\\\\\\\\\\\\\//////////////////\\\\\\\\\\\\\\\\\\\//////////////////
#pega os dados de uma pessoa
def jawboneMoves(client_id,client_secret,person_id,tableName,cur):

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
    #encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
    #data = (urllib.request.urlopen(request).read().decode(encoding))
    #dadosNedel = json.loads(data)
    #print (params["refresh_token"])
    #json.dump(data,arquivo)


    #arquivo = open('nedelJawbone.txt', 'w')
    #de setembro 2015 até outubro 2015
    lastDate = getLastDate(tableName,cur)
    if lastDate[0][0] < datetime.datetime.now(): 
        url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/moves?start_time=' + str(lastDate[0][0].timestamp()) + '&&end_time=' + str(datetime.datetime.now().timestamp())
    else:
        return print('up to date')
    #dois dias
    #url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1441065600&&end_time=1441152000'
    while(1):
    #cidade  =  input("Digite o nome da cidade procurada: ")
    #cidade = cidade.split(' ')

    #if len(cidade) >  2:
    #    url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87'
    #else:
        
        
        print ("Requisitando acesso aos dados Moves")
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
            urlTicks = 'https://jawbone.com/nudge/api/v.1.1/moves/' + evento['xid'] + '/ticks'
            requestTicks = urllib.request.Request(urlTicks, headers = {"Authorization": "Bearer oJu-seHwrstYgtTAQpuUxycYC84VDTuWUUjXiXCc2yhDhJTENkwuyJtiaaIX-06Pitl9KvYhBDiSYPnWZGqRFVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP"  })
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
            printTable(tableName,cur)
            return information





def jawboneSleep(client_id,client_secret):

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
    #encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
    #data = (urllib.request.urlopen(request).read().decode(encoding))
    #dadosNedel = json.loads(data)
    #print (params["refresh_token"])
    #json.dump(data,arquivo)


    #arquivo = open('nedelJawbone.txt', 'w')
    #de setembro 2015 até outubro 2015
    url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1441065600&&end_time=1446336000'
    #dois dias
    #url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1441065600&&end_time=1441152000'
    while(1):
    #cidade  =  input("Digite o nome da cidade procurada: ")
    #cidade = cidade.split(' ')

    #if len(cidade) >  2:
    #    url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87'
    #else:
        
        
        print ("Requisitando acesso aos dados Sleep")
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
            urlTicks = 'https://jawbone.com/nudge/api/v.1.1/users/@me/moves/' + evento['xid'] + '/ticks'
            request = urllib.request.Request(url, headers = {"Authorization": "Bearer oJu-seHwrstYgtTAQpuUxycYC84VDTuWUUjXiXCc2yhDhJTENkwuyJtiaaIX-06Pitl9KvYhBDiSYPnWZGqRFVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP"  })
            response = urllib.request.urlopen(request).getcode()
            encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
            data = (urllib.request.urlopen(request).read().decode(encoding))
            dadosNedel = json.loads(data)
            #aqui o information vai ter todos os ticks de um "move"
            information.append(dadosNedel)

        if 'links' in dadosNedel['data'].keys():
            url = 'https://jawbone.com' + dadosNedel['data']['links']['next']
        else: 
            #print(information)
            return information

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
    #encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
    #data = (urllib.request.urlopen(request).read().decode(encoding))
    #dadosNedel = json.loads(data)
    #print (params["refresh_token"])
    #json.dump(data,arquivo)


    #arquivo = open('nedelJawbone.txt', 'w')
    #de setembro 2015 até outubro 2015
    url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/heartrates?start_time=1441065600&&end_time=1446336000'
    #dois dias
    #url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1441065600&&end_time=1441152000'
    while(1):
    #cidade  =  input("Digite o nome da cidade procurada: ")
    #cidade = cidade.split(' ')

    #if len(cidade) >  2:
    #    url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87'
    #else:
        
        
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
        cur.execute(query + "(cidade, temperatura) VALUES (%s, %s)",elements)

def addMoveElement(tableName,element,cur):
    if existsTable(tableName,cur):
        query = "INSERT INTO " + tableName
        cur.execute(query + "(datetime, activity,person_id,created_at, updated_at) VALUES (%s, %s,%s,%s,%s)",element)

def deleteTable(tableName,cur):
    if existsTable(tableName,cur):
        cur.execute("DROP TABLE " + tableName + " ;")
        print("Table '"+ tableName +"' deleted")

def getLastDate(tableName,cur):
    if existsTable(tableName,cur):
        cur.execute("SELECT MAX(datetime) FROM " + tableName + ";")
        return cur.fetchall()
