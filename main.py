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
        return [dadosTempo['list'][0]['dt'],dadosTempo['list'][0]['main']['temp_max'],dadosTempo['list'][0]['main']['temp'],dadosTempo['list'][0]['main']['temp_min'],'-','-','-','-']#dadosTempo['list'][0]['rain']['3h'] ]
    else:
        return ['-']


#pega os dados de uma pessoa
def jawbone():
    def jauth():
        code = params[:code]
        uri = URI("https://jawbone.com/auth/oauth2/token")
        params = {
          client_id: '0NIN0D_htj0',
          client_secret: 'aac3f063d18489fc2e3fa3dabbd5c01a120fa450',
          grant_type: 'authorization_code',
          scope: 'basic_read extended_read location_read move_read',
          code: code
        }
        uri.query = URI.encode_www_form(params)

    def jrequest():
        uri = URI('https://jawbone.com/nudge/api/v.1.1/users/@me/moves')
        token = params[:oauth_token]
        request = Net.HTTP.Get.new(uri.to_s, {Authorization : "Bearer #{token}"})
        http = Net.HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        response = http.request(request)
        
        body = response.body
        #render layout: false



    params = {
        "response_type=code" : 'code',
          "client_id": '0NIN0D_htj0',
          'scope': 'basic_read extended_read location_read move_read',
          'redirect_uri' : ''
        }
    url = "https://jawbone.com/auth/oauth2/token"
    request = urllib.request.Request(url, headers = params)
    #encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
    #data = (urllib.request.urlopen(request).read().decode(encoding))
    print (request)


    information = []
    #arquivo = open('newToken.txt' , 'w+')
    params = {
          "client_id": '0NIN0D_htj0',
          "client_secret": 'aac3f063d18489fc2e3fa3dabbd5c01a120fa450',
          "grant_type": 'refresh_token',
          "refresh_token": ''
        }
    url = "https://jawbone.com/auth/oauth2/token"
    request = urllib.request.Request(url, headers = params)
    #encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
    #data = (urllib.request.urlopen(request).read().decode(encoding))
    #dadosNedel = json.loads(data)
    print (params["refresh_token"])
    #json.dump(data,arquivo)


    #arquivo = open('nedelJawbone.txt', 'w')
    #de setembro 2015 até outubro 2015
    url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/moves?start_time=1441065600&&end_time=1446336000'
    #dois dias
    #url = 'https://jawbone.com/nudge/api/v.1.1/users/@me/sleeps?start_time=1441065600&&end_time=1441152000'
    while(1):
    #cidade  =  input("Digite o nome da cidade procurada: ")
    #cidade = cidade.split(' ')

    #if len(cidade) >  2:
    #    url = 'http://api.openweathermap.org/data/2.5/find?q=' + cidade[0] + '%20' + cidade[1] +  '&APPID=c202fefe29158aebc3cd656900708e87'
    #else:
        
        
        print ("Requisitando acesso aos dados")
        request = urllib.request.Request(url, headers = {"Authorization": "Bearer oJu-seHwrstYgtTAQpuUxycYC84VDTuWUUjXiXCc2yhDhJTENkwuyJtiaaIX-06Pitl9KvYhBDiSYPnWZGqRFVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP"  })
        response = urllib.request.urlopen(request).getcode()
        if response !=200:
            break
        print("Baixando dados")
        print("Baixados")



        encoding = urllib.request.urlopen(request).info().get_param('charset', 'utf8')
        data = (urllib.request.urlopen(request).read().decode(encoding))
        dadosNedel = json.loads(data)
        information.append(dadosNedel)
        #json.dump(dadosNedel,arquivo)

        for evento in dadosNedel['data']['items']:
            print(evento['date'])
        if 'links' in dadosNedel['data'].keys():
            url = 'https://jawbone.com' + dadosNedel['data']['links']['next']
        else: 
            print(information)
            return information



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






jawbone()
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