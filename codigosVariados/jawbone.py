#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.parse
import urllib.request
import json
import csv
from csv import writer
import argparse
import logging
from types import *
import sys
from os import path



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



arquivo = open('newToken.txt' , 'w+')
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
    json.dump(dadosNedel,arquivo)

    for evento in dadosNedel['data']['items']:
        print(evento['date'])

    url = 'https://jawbone.com' + dadosNedel['data']['links']['next']

#text_file = open("logCidadeTempo.json", "w")
#text_file.write(str(dadosTempo))
#text_file.close()
#if(dadosTempo['message'] !=  ''):
#    print  (dadosTempo['message'])
#else:
#    print("Erro, cidade nao encontrada (ou outra pode ser coisa, sou soh um else. Desculpa)")


