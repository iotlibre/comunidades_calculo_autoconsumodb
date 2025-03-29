
#!/usr/bin/env python
import configparser
import json
from datetime import datetime
from datetime import timedelta
import time 
import requests
import logging
from logging.handlers import RotatingFileHandler
import mysql.connector

# Para obtener mas detalle: level=logging.DEBUG
# Para comprobar el funcionamiento: level=logging.INFO
logging.basicConfig(
        level=logging.DEBUG,
        handlers=[RotatingFileHandler('./logs/log_autoconsumido.log', maxBytes=10000000, backupCount=4)],
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

'''
regsiter:

{'sidn': 3, 'name': 'jose', 'type': 'datadis', 'emon_key': '6numeros2345245yletrasasdfadsf80',
 'gen_id': 1, 'coef': 1.0, 'feed_con': 102, 'feed_gen': 103, 
 'autoconsumed': 1.1, 'exported': 1.1, 'imported': 1.1, 'sen_last': datetime.datetime(2025, 3, 20, 23, 0)}
'''
def save_register(rr_index_):
    logging.debug('save_register()')

    global config
    global reading_register_
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor(dictionary=True)

    register = reading_register_[rr_index_]
    au = register["autoconsumed"]
    ex = register["exported"]
    im = register["imported"]
    sl = register["sen_last"]
    id = register["sidn"]

    sql = "UPDATE sensors SET autoconsumed=%s, exported=%s, imported=%s, sen_last=%s WHERE sidn=%s"
    val = (au,ex,im,sl,id)

    logging.debug(sql)
    logging.debug(val)

    cursor.execute(sql,val)
    conexion.commit()

    cursor.close()
    conexion.close()
    # logging.debug(resultados)

'''
Cambio de una fecha en formato iso a formato Datetime
iso: '2022-06-02T14:00:00+02:00'

type(isoD) --> <class 'datetime.datetime'>
'''

def iso_to_datetime(iso):
     dateL= iso.split("+")[0].split("T")
     year = int(dateL[0].split("-")[0])
     month = int(dateL[0].split("-")[1])
     day = int(dateL[0].split("-")[2])
     hour = int(dateL[1].split(":")[0])
     minutes = int(dateL[1].split(":")[0])
     isoD = datetime(year, month, day, hour, minutes, 00, 00000)
     logging.debug("isoD :" + str(isoD))
     return isoD


'''datetime

register del reading_register_ :
{'sidn': 3, 'name': 'jose', 'type': 'datadis', 'emon_key': '6numeros2345245yletrasasdfadsf80',
 'gen_id': 1, 'coef': 1.0, 'feed_con': 102, 'feed_gen': 103, 
 'autoconsumed': 1.1, 'exported': 1.1, 'imported': 1.1, 'sen_last': datetime.datetime(2025, 3, 20, 23, 0)}

http://direcciondelservidor.com/input/post?node=francisco&fulljson=
{"autoconsumed":2.785,"exported":2.377,"imported":1.715,"time":"2025-03-24T12:13:00"}
&apikey=6numeros2345245yletrasasdfadsf80
'''
def emoncms_tx(position):

    global reading_register_

    emonServer = parser.get('emoncms_server','emon_ip')

    register_tx = reading_register_[position]
    userKey =  register_tx["emon_key"]
    nodeNameS = register_tx["name"]
    
    autoconsumedS = str(round(register_tx["autoconsumed"],3))
    exportedS = str(round(register_tx["exported"],3))
    importedS = str(round(register_tx["imported"],3))

    # Correcciones horarias
    # DATADIS muestra el consumo de una hora al inicio de la hora
    ener_time_s = (register_tx["sen_last"] - timedelta(hours=1)).isoformat()
    
    urlEmon =  "http://"
    urlEmon += emonServer
    urlEmon += "/input/post?node="
    urlEmon += nodeNameS
    urlEmon += "&fulljson={\"autoconsumed\":"
    urlEmon += autoconsumedS
    urlEmon += ",\"exported\":"
    urlEmon += exportedS
    urlEmon += ",\"imported\":"
    urlEmon += importedS
    urlEmon += ",\"time\":\""
    urlEmon += ener_time_s
    urlEmon += "\"}&apikey="
    urlEmon += userKey
    
    logging.info("----> " + urlEmon)
    response_text = requests.get(urlEmon)
    logging.debug("+++ " + str(response_text))
    time.sleep(0.4)

''' Procesar la lectura antes de enviarla.
data0n:
["2022-05-30T20:00:00+02:00",1.1659999999999968]
data1n:
["2022-05-30T20:00:00+02:00",0.3434343434343434]
register:
'sidn': 1, 'name': 'nombre', 'type': 'datadis', 'emon_key': 'wetjj0a7e7a650wrfy08ewert35wt005', 'gen_id': 1, 'coef': 1.0, 'feed_con': 180, 'feed_gen': 187, 
'autoconsumed': 1.1, 'exported': 1.1, 'imported': 1.1, 'sen_last': datetime.datetime(2025, 3, 20, 23, 0)}
'''
def procesar_lectura(data0n,data1n,position):

    global reading_register_

    logging.debug("++ procesar_lectura()")

    register = reading_register_[position]    
    imporetedEnergy = register["imported"]
    autoconsumedEnergy = register["autoconsumed"]
    exportedEnergy = register["exported"]
    lastTimeD=register["sen_last"]

    logging.debug("register:")
    logging.debug(register)
    
    logging.debug("dataXn:")
    logging.debug(data0n[0]) # "2022-05-30T20:00:00+02:00"
    logging.debug(data1n[0])
    logging.debug(data0n[1]) # 1.1659999999999968
    logging.debug(data1n[1])    
    
    logging.debug("lastTimeD: " + str(lastTimeD)) # <class 'datetime.datetime'>
 
    currentTimeD = iso_to_datetime(data0n[0])
    
    timeOk = 1
    decodedOk = 0
    
    if(lastTimeD >= currentTimeD):
        timeOk = 0
    if(currentTimeD.replace(tzinfo=None) + timedelta(hours=2) >= datetime.now()):
        timeOk = 0

    if(isinstance(data0n[1], float) and isinstance(data1n[1], float)):
        decodedOk = 1
        logging.debug("decodedOk = 1. types ok")
    else:
        logging.debug("decodedOk = 0. types not ok")
        decodedOk = 0

    if(timeOk == 1 and  decodedOk == 1):
        try:
            importedHour= data0n[1]-data1n[1]
            # logging.debug("tipos de las variables :") # <class 'float'>
            # logging.debug(type(importedHour))
            # logging.debug(type(imporetedEnergy))
            # logging.debug(type(autoconsumedEnergy))
            # logging.debug(type(data1n[1]))
            # logging.debug(type(exportedEnergy))
            # logging.debug(type(importedHour))
            # logging.debug(type(data0n[1]))

            if(importedHour >= 0.0):
                imporetedEnergy = imporetedEnergy + importedHour
                autoconsumedEnergy = autoconsumedEnergy +data1n[1]
            else:
                exportedEnergy = exportedEnergy + abs(importedHour)
                autoconsumedEnergy = autoconsumedEnergy + data0n[1]
        except Exception as e:
            logging.debug(f"Error inesperado: {e}")
            decodedOk = 0          
        
    logging.debug("imporetedEnergy: " + str(imporetedEnergy))
    logging.debug("autoconsumedEnergy: " + str(autoconsumedEnergy))
    logging.debug("exportedEnergy: " + str(exportedEnergy))

    if(timeOk == 1 and decodedOk == 1):
        register["imported"] = imporetedEnergy
        register["autoconsumed"] = autoconsumedEnergy
        register["exported"] = exportedEnergy
        register["sen_last"] = currentTimeD

        logging.debug("emoncms_tx: " + str(register))
        emoncms_tx(position)

''' ver reading_register con formato json
cat registers/reading_register.txt | python -m json.tool
'''
def abrir_reading_register():
    global config
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT * FROM sensors"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    # logging.debug(resultados)
    cursor.close()
    conexion.close()

    return resultados

'''comprobar_consulta
comprueba que los formatos son correctos antes de enviarlos a procesar
data_: datos leidos en json(los 2 feedId)
rr_index: indice del registro de cliente (reading_register_)
comprueba que hay un numero de registros mínimo

register del reading_register_  :
'sidn': 1, 'name': 'nombre', 'type': 'datadis', 'emon_key': 'wetjj0a7e7a650wrfy08ewert35wt005', 'gen_id': 1, 'coef': 1.0, 'feed_con': 180, 'feed_gen': 187, 
'autoconsumed': 1.1, 'exported': 1.1, 'imported': 1.1, 'sen_last': datetime.datetime(2025, 3, 20, 23, 0)}
<class 'dict'>
'''
def comprobar_consulta(data_, rr_position):  #reading register position, objeto datetime.datetime 
    logging.debug("++++++ comprobar_consulta()")
    
    consultaOk = 1
    try:
        data0 = data_[0]["data"]
        data1 = data_[1]["data"]
    except:
        logging.warning("Error en el formato de los datos recibidos")
        consultaOk = 0
        
    if(consultaOk == 0):
        consultaOk = 0
    elif((type(data0) != type(list())) or (type(data1) != type(list()))):
        consultaOk = 0;
        logging.warning("Error type list")
    elif ((len(data0) < 4) or (len(data1) < 4)):
        consultaOk = 0;
        logging.warning("Error longitud < 4")
    else:
        consultaOk = 1;
        
    if(consultaOk == 1):
        valid_power_data = {}
        for x in data0:
            try:
                index = data0.index(x)
                logging.debug("++++ Procesado de la posicion: "+ str(index))
                logging.debug(x)
                logging.debug(data1[index])
            except:
                logging.warning("Error en el calculo de los datos")
                consultaOk = 0
            if(consultaOk == 1):
                procesar_lectura(x,data1[index],rr_position)
            
def formato_lectura(text):
    try:
        data = json.loads(text)
    except:
        data = []
    return data

'''
register del reading_register_  :
'sidn': 1, 'name': 'nombre', 'type': 'datadis', 'emon_key': 'wetjj0a7e7a650wrfy08ewert35wt005', 
'gen_id': 1, 'coef': 1.0, 'feed_con': 102, 'feed_gen': 103, 
'autoconsumed': 1.1, 'exported': 1.1, 'imported': 1.1, 'sen_last': datetime.datetime(2025, 3, 20, 23, 0)}
<class 'dict'>

consulta:
---------
http://direcciondelservidor/feed/data.json?ids=101,1102&start=2025-03-21T23:00&end=now
&interval=3600&average=0&timeformat=iso8601&skipmissing=0&limitinterval=0&delta=1,1
&apikey=wetjj0a7e7a650wrfy08ewert35wt005

'''
def consulta_de_consumos(position):
    logging.debug("++++++ consulta_de_consumos()")
    global reading_register_

    emonServer = parser.get('emoncms_server','emon_ip')
    register = reading_register_[position]
    # feedId="45,40"                      # consumo: 45. generacion 40    
    feed_con = register["feed_con"]
    feed_gen = register["feed_gen"]
    emon_key = register["emon_key"]
    startDateQ=""
    # last datetime (registered datetimeformat)
    lastDatetimeD = register["sen_last"]   #tiempo de la última lectura del query anterior
    logging.debug("lastDatetimeD ---> " + str(lastDatetimeD) )
    end_date_d = datetime.now()
    delta= timedelta(days=20)
    
    if(lastDatetimeD.replace(tzinfo=None) + delta <= end_date_d):
        lastDatetimeD = end_date_d - delta # star date datetime(format)
        
    # Se parte de lastDatetimeD
    star_hour_str = str(lastDatetimeD.hour) + ":00" 
    if (lastDatetimeD.hour <= 9):
        star_hour_str = "0" + str(lastDatetimeD.hour) + ":00"
    star_day_str = str(lastDatetimeD.day)
    if (lastDatetimeD.day <= 9):
        star_day_str = "0" + str(lastDatetimeD.day)    
    star_month_str = str(lastDatetimeD.month)
    if (lastDatetimeD.month <= 9):
        star_month_str = "0" + str(lastDatetimeD.month)
    startDateQ = str(lastDatetimeD.year) + "-" + star_month_str + "-" + star_day_str + "T" + star_hour_str

    url = "http://"
    url += emonServer
    url += "/feed/data.json?ids="
    url += str(feed_con)
    url += ","
    url += str(feed_gen)
    url += "&start="
    url += startDateQ
    url += "&end=now&interval=3600&average=0&timeformat=iso8601&skipmissing=0&limitinterval=0&delta=1,1&apikey="
    url += emon_key
       
    logging.info(url)
   
    # Consulta de los consumos
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    return response_text

    
#************************
#** LOGICA DE PROCESO ***
#************************

parser = configparser.ConfigParser()

# comunidad_db, emoncms_server
parser.read('config_sensores.ini')

global config
config = {
    'host' : parser.get('comunidad_db','host'),
    'port' : parser.get('comunidad_db','port'), 
    'user' : parser.get('comunidad_db','user'),
    'password' : parser.get('comunidad_db','password'),
    'database' : parser.get('comunidad_db','database')
}

'''Cada x en reading_register_
-----------------------------
Reading_register es un registro de la base de datos con los datos de cada usuario 
El formato es: Lista de diccionarios
Durante todo el programa se guarda en memoria en reading_registers_[x]
register incluye los datos de la última lectura valida

cada elemento del listado (register) del reading_register_  :
'sidn': 1, 'name': 'nombre', 'type': 'datadis', 'emon_key': 'wetjj0a7e7a650wrfy08ewert35wt005', 
'gen_id': 1, 'coef': 1.0, 'feed_con': 102, 'feed_gen': 103, 
'autoconsumed': 1.1, 'exported': 1.1, 'imported': 1.1, 'sen_last': datetime.datetime(2025, 3, 20, 23, 0)}
<class 'dict'>
'''
global reading_register_
reading_register_ = abrir_reading_register() #<class 'list'>
logging.debug("++++++ reading_register desde la DB:")
logging.debug(str(reading_register_))

for x in reading_register_:
    rr_index = reading_register_.index(x) #reading_register_ index
    logging.debug("++++++ register: ")
    logging.debug(str(x))
    response_txt = consulta_de_consumos(rr_index)

    # logging.debug(response_txt)
    # logging.debug(type(response_txt))# <class 'str'>

    data_red = formato_lectura(response_txt) #devuelve la lectura en json
    
    # data_red: datos leidos en json(con los 2 feedId)
    # rr_index: indice del registro en reading_register_
    comprobar_consulta(data_red,rr_index)
        
    save_register(rr_index) 


