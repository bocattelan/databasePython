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


def fitbitMoves(client_secret,client_id,tableName,cur):
    lastDate = getLastDate(tableName,cur)
    if lastDate[0][0] != None:
        if lastDate[0][0].date() < datetime.datetime.now().date(): 
            url = 'https://api.fitbit.com/1/user/229Z77/activities/steps/date/' + str(lastDate[0][0].timestamp()) + '/' +str(datetime.datetime.now().timestamp()) +'/1min.json'
        else:
            return print('Fitbit Moves up to date')
    else:
        url = 'https://api.fitbit.com/1/user/229Z77/activities/steps/date/' + '0' + '/' + str(datetime.datetime.now().date()) +'/1m.json'
    #dois dias
    #url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1441065600&&end_time=1441152000'
    while(1):
    #cidade  =  input("Digite o nome da cidade procurada: ")
    #cidade = cidade.split(' ')

    #if len(cidade) >  2:
    #    url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87'
    #else:
        
        print ("Requisitando acesso aos dados Moves")
        request = urllib.request.Request(url, headers = {"Authorization": "Bearer " + client_secret  })
        response = urllib.request.urlopen(request).getcode()
        if response !=200:
            break
        print("Baixando dados")
        print("Baixados")
        return


def foursquare (client_secret,client_id,tableName,cur,conn):
    #nedel eh 21
    # id  |      datetime       |                             name                              |         city         |    country    |                 latitude                 |                longitude                 | person_id |         created_at         |         updated_at

    #OQLGPMDLAZ25JAZE5VW5DRF0SOOSWLCXQMEED5IZSLBBQN3U
    try:
        url = "https://api.foursquare.com/v2/users/self/checkins?oauth_token=" + client_secret + "&sort=oldestfirst" + "&afterTimestamp=0" + "&v=20140806&m=foursquare"
        request = urllib.request.Request(url)
        encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
        data = (urllib.request.urlopen(request).read().decode(encoding))
        dadosNedel = json.loads(data)
        lastDate = getLastDate(tableName,cur)

        if len(dadosNedel['response']['checkins']["items"]) <=0:
            print("sem dados do foursquare")
            return
    except:
        print("ACCSSES DENIED to foursquare")
        return
    
    for checkin in dadosNedel['response']['checkins']["items"]:
        #print('oi')
        if lastDate[0][0].date() < datetime.datetime.fromtimestamp(checkin['createdAt']).date():
            addFoursquareElement(tableName,[datetime.datetime.fromtimestamp(checkin['createdAt']),checkin['location']['name'],checkin['location']['city'],checkin['location']['country'],checkin['location']['lat'],checkin['location']['lng'],client_id,datetime.datetime.now(), datetime.datetime.now()],cur)
            print('element added')
    lastDateGot = dadosNedel['response']['checkins']["items"][-1]["createdAt"] - 3000

    while(len(dadosNedel['response']['checkins']["items"])!=0 and  lastDate[0][0].date() < datetime.datetime.now().date() ):
        try:
            url = "https://api.foursquare.com/v2/users/self/checkins?oauth_token=" + client_secret + "&sort=oldestfirst" + "&afterTimestamp=" + str(lastDateGot) + "&v=20140806&m=foursquare"
            request = urllib.request.Request(url)
            encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
            data = (urllib.request.urlopen(request).read().decode(encoding))
            dadosNedel = json.loads(data)
            lastDate = getLastDate(tableName,cur)
        except:
            print("ACCSSES DENIED to foursquare")
            break
        for checkin in dadosNedel['response']['checkins']["items"]:
            if lastDate[0][0].date() < datetime.datetime.fromtimestamp(checkin['createdAt']).date():
                try:
                    if 'location' in checkin.keys():
                        print('oi')
                        addFoursquareElement(tableName,[datetime.datetime.fromtimestamp(checkin['createdAt']),checkin['location']['name'],checkin['location']['city'],checkin['location']['country'],checkin['location']['lat'],checkin['location']['lng'],client_id,datetime.datetime.now(), datetime.datetime.now()],cur)
                        print('element added')
                        #conn.commit()
                    elif 'venue' in checkin.keys() and 'name' in checkin['venue'].keys():
                        #print(checkin)
                        #print('\n')
                        print('ola')
                        addFoursquareElement(tableName,[datetime.datetime.fromtimestamp(checkin['createdAt']),checkin['venue']['name'],checkin['venue']['location']['city'],checkin['venue']['location']['country'],checkin['venue']['location']['lat'],checkin['venue']['location']['lng'],client_id,datetime.datetime.now(), datetime.datetime.now()],cur)
                        print('element added')
                    elif 'venue' in checkin.keys():
                        addFoursquareElement(tableName,[datetime.datetime.fromtimestamp(checkin['createdAt']),'',checkin['venue']['location']['city'],checkin['venue']['location']['country'],checkin['venue']['location']['lat'],checkin['venue']['location']['lng'],client_id,datetime.datetime.now(), datetime.datetime.now()],cur)
                        #print(checkin)
                except:
                    try:
                        print(checkin)
                    except:
                        print('ERRO BIZARRO')
                  #  print('\n')
        lastDateGot = dadosNedel['response']['checkins']["items"][-1]["createdAt"] - 3000
    print('Foursquare updated')

#pega os dados de uma cidade NO MOMENTO
def weather (cidadeInput, person_id,tableName,cur):
    #  id  |    date    | max_temperature | mean_temperature | min_temperature | precipitation |          events           | person_id |         created_at         |         updated_at
    lastDate = getLastDate(tableName,cur)
    if lastDate[0][0] != None:
        if lastDate[0][0] < datetime.datetime.now().date(): 
            cidade = cidadeInput 
            cidade = cidade.split(' ')
            if len(cidade) >=  2:
                url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87&units=metric'
            else:
                url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '&APPID=c202fefe29158aebc3cd656900708e87&units=metric'
            #print ("Requisitando acesso aos dados")
            request = urllib.request.Request(url)
            encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
            data = (urllib.request.urlopen(request).read().decode(encoding))
            dadosTempo = json.loads(data)
            addWeatherElements('weathers',[datetime.datetime.now(),dadosTempo['list'][0]['main']['temp_max'],dadosTempo['list'][0]['main']['temp'],dadosTempo['list'][0]['main']['temp_min'],dadosTempo['list'][0]['main']['humidity'],dadosTempo['list'][0]['weather'][0]['main'],person_id, datetime.datetime.now(), datetime.datetime.now()], cur)
            print("Weathers updated")
        else:
            return print('Weathers up to date')
    else:
        cidade = cidadeInput 
        cidade = cidade.split(' ')
        if len(cidade) >=  2:
            url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87&units=metric'
        else:
            url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '&APPID=c202fefe29158aebc3cd656900708e87&units=metric'
        #print ("Requisitando acesso aos dados")
        request = urllib.request.Request(url)
        encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
        data = (urllib.request.urlopen(request).read().decode(encoding))
        dadosTempo = json.loads(data)
        addWeatherElements('weathers',[datetime.datetime.now(),dadosTempo['list'][0]['main']['temp_max'],dadosTempo['list'][0]['main']['temp'],dadosTempo['list'][0]['main']['temp_min'],dadosTempo['list'][0]['main']['humidity'],dadosTempo['list'][0]['weather'][0]['main'],person_id, datetime.datetime.now(), datetime.datetime.now()], cur)
        print("Weathers updated")
        #print (dadosTempo)
    #return [dadosTempo['list'][0]['dt'],dadosTempo['list'][0]['main']['temp_max'],dadosTempo['list'][0]['main']['temp'],dadosTempo['list'][0]['main']['temp_min'],'-','-','-','-']#dadosTempo['list'][0]['rain']['3h'] ]
    #return ['-']

#JAWBONE /////////////\\\\\\\\\\\\\\\\\//////////////////\\\\\\\\\\\\\\\\\\\//////////////////
#pega os dados de uma pessoa
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
            urlTicks = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps/' + evento['xid'] + '/ticks'
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
        cur.execute(query + "(date, max_temperature,mean_temperature,min_temperature,precipitation,events,person_id,created_at,updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",elements)

def addMoveElement(tableName,element,cur):
    if existsTable(tableName,cur):
        query = "INSERT INTO " + tableName
        cur.execute(query + "(datetime, activity,person_id,created_at, updated_at) VALUES (%s, %s,%s,%s,%s)",element)

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
    if existsTable(tableName,cur) and tableName == 'activities' or tableName == 'locations':
        cur.execute("SELECT MAX(datetime) FROM " + tableName + ";")
        return cur.fetchall()
    elif existsTable(tableName,cur) and tableName == 'weathers':
        cur.execute("SELECT MAX(date) FROM " + tableName + ";")
        return cur.fetchall()

def getPeopleList(cur):
    if existsTable('people',cur):
        cur.execute("SELECT * FROM people;")
        return cur.fetchall()