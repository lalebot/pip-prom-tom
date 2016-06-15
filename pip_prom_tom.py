#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
.______    __  .______          .______   .______        ______   .___  ___.        .___________.  ______   .___  ___.
|   _  \  |  | |   _  \         |   _  \  |   _  \      /  __  \  |   \/   |        |           | /  __  \  |   \/   |
|  |_)  | |  | |  |_)  |  ______|  |_)  | |  |_)  |    |  |  |  | |  \  /  |  ______`---|  |----`|  |  |  | |  \  /  |
|   ___/  |  | |   ___/  |______|   ___/  |      /     |  |  |  | |  |\/|  | |______|   |  |     |  |  |  | |  |\/|  |
|  |      |  | |  |             |  |      |  |\  \----.|  `--'  | |  |  |  |            |  |     |  `--'  | |  |  |  |
| _|      |__| | _|             | _|      | _| `._____| \______/  |__|  |__|            |__|      \______/  |__|  |__|

Descripción: Un pipeline que extrae promotores de tomate de la especie
             Solanum lycopersicum desde la web Solgenomics. Proyecto final
             en el marco de la Especialización en Bioinformática de la
             Universidad Nacional de Rosario.
Autor: Alejandro Damián Pistilli <apistill [arroba] unr.edu.ar>
Sitio del proyecto: https://github.com/lalebot/pip-prom-tom
Hecho en Zavalla, Argentina
'''

import urllib.request
import urllib.parse
import sqlite3 as lite
import time
import os
import threading
import re
import optparse
import logging

import sys
import math


'''
.___  ___.  _______ .__   __.  __    __
|   \/   | |   ____||  \ |  | |  |  |  |
|  \  /  | |  |__   |   \|  | |  |  |  |
|  |\/|  | |   __|  |  . `  | |  |  |  |
|  |  |  | |  |____ |  |\   | |  `--'  |
|__|  |__| |_______||__| \__|  \______/
'''
def menu(proy):
    print()
    print("===================================================================")
    print("Bienvenido al Pip-Prom-Tom - Nombre del proyecto: ", proy)
    print("Un Pipeline para extrae Promotores de Solanum Lycopersicum")
    print("===================================================================")
    print("Menu")
    print(" 1 - Inicializar y cargar configuracion y la lista de promotores")
    print(" 2 - Cargar la base de datos desde la web -SolGenomics-")
    print(" 3 - Crear archivo FASTA con los resultados de la busqueda")
    print(" 4 - Análisis MEME y TOMTOM")
    print(" 9 - PIPELINE")
    print(" 0 - Salir")
    print("===================================================================")
    print()


'''
.______      ___      .______          ___      .___  ___.
|   _  \    /   \     |   _  \        /   \     |   \/   |
|  |_)  |  /  ^  \    |  |_)  |      /  ^  \    |  \  /  |
|   ___/  /  /_\  \   |      /      /  /_\  \   |  |\/|  |
|  |     /  _____  \  |  |\  \----./  _____  \  |  |  |  |
| _|    /__/     \__\ | _| `._____/__/     \__\ |__|  |__|

'''
def parametros():
    try:
        file_param = open('conf.ini', 'r')
    except Exception as e:
        print("Error al abrir el archivo de conf.ini: ", e)
        logging.exception(e)
        exit()
    for linea in file_param.readlines():
        if 'pipeline =' in linea:
            pip_pip = linea.split('= ')[1].rstrip('\n')
        if 'meme-path =' in linea:
            memepath = linea.split('= ')[1].rstrip('\n')
        if 'meme-param =' in linea:
            memeparam = linea.split('= ')[1].rstrip('\n')
        if 'tomtom-path =' in linea:
            tomtompath = linea.split('= ')[1].rstrip('\n')
        if 'tomtom-param =' in linea:
            tomtomparam = linea.split('= ')[1].rstrip('\n')
        if 'tomtom-bd =' in linea:
            tomtombd = linea.split('= ')[1].rstrip('\n')
        if 'threads =' in linea:
            try:
                nro_threads = int(linea.split('= ')[1].rstrip('\n'))
            except Exception as e:
                print("El número de threads es incorrecto, por favor corrija el archivo conf.ini")
                logging.exception(e)
                file_param.close()
                exit()
    file_param.close()
    return(pip_pip,memepath,nro_threads,tomtompath,memeparam,tomtomparam,tomtombd)


'''
 __  .__   __.  __    ______  __       ___       __       __   ________      ___      .______
|  | |  \ |  | |  |  /      ||  |     /   \     |  |     |  | |       /     /   \     |   _  \
|  | |   \|  | |  | |   ----'|  |    /  ^  \    |  |     |  | `---/  /     /  ^  \    |  |_)  |
|  | |  . `  | |  | |  |     |  |   /  /_\  \   |  |     |  |    /  /     /  /_\  \   |      /
|  | |  |\   | |  | |  `----.|  |  /  _____  \  |  `----.|  |   /  /----./  _____  \  |  |\  \----.
|__| |__| \__| |__|  \______||__| /__/     \__\ |_______||__|  /________/__/     \__\ | _| `._____|

'''
def inicializar(path_out,filein):
    print("\n==============")
    print("Inicialización")
    print("==============")
    try:
        os.system('sqlite3 '+ path_out + 'promResult.db &')
        con = lite.connect(path_out + 'promResult.db')
        conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
        conn.execute("DROP TABLE IF EXISTS Prom") # Elimnar la Bdd
        conn.execute("CREATE TABLE Prom(id INTEGER DEFAULT 1 PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT UNIQUE NOT NULL, cab_adn TEXT UNIQUE, adn TEXT, cod_sg_bus TEXT, cod_sg_up TEXT)") # Crear las tablas de la bdd
        # id nom cab_adn adn cod_sg_bus cod_sg_up exp
        con.commit() # Confirmar los cambios
    except lite.Error as e:
        print("Error al crear Bdd: \n", e)
        logging.exception(e)
        exit()
    # Abrir el archivo con lista de los promotores
    try:
        file_list_prom = open(filein, 'r')
        list_prom = file_list_prom.read().split('\n')
        file_list_prom.close()
    except Exception as e:
        print("Error al abrir el archivo de entrada, revise el log.\n",e)
        logging.exception(e)
        exit()
    # Cargar la Bdd
    lista_prom = []
    for i in list_prom:
        i = i.strip()
        if i not in lista_prom:
            i = i.strip()
            lista_prom.append(i)
    for i in lista_prom:
        try:
            if re.search('\s*Solyc\w*\s*',i):
                print(i)
                conn.execute("INSERT INTO Prom(id,nom) VALUES(null,?)",[i])
        except lite.Error as e:
            print("Error al cargar la Bdd, revise el log: \n", e)
            logging.exception(e)
            exit()
    # Grabar los cambios en la Bdd
    try:
        con.commit()
        print("\nCódigo de promotores cargados.")
    except lite.Error as e:
        print("Error al grabar en la Base de datos: \n", e)
        logging.warning(e)
    # Cerrar la conexion a la Bdd
    if con:
        conn.close()
        con.close()


'''
 __    __  .______   .______       _______  .______   .______
|  |  |  | |   _  \  |   _  \     |       \ |   _  \  |   _  \
|  |  |  | |  |_)  | |  |_)  |    |  .--.  ||  |_)  | |  |_)  |
|  |  |  | |   ___/  |   ___/     |  |  |  ||   _  <  |   _  <
|  `--'  | |  |      |  |         |  '--'  ||  |_)  | |  |_)  |
 \______/  | _|      | _|         |_______/ |______/  |______/

'''
# Se utiliza la combinación de Bdd (Sqlite3) y Threads para que los hilos trabajen paralelamente y puedan acceder de manera conjunta a la misma base de datos actualizándola hasta estar completa. Además ante cualquier corte del proceso de carga se puede retomar facilmente.
def up_bdd(nro_threads,path_out,up,down,gap):
    print("\n=========================================")
    print("Cargando las secuencias desde SolGenomics")
    print("=========================================")
    print("Cantidad de threads lanzados: ", nro_threads, ", por favor espere.")

    try:
        con = lite.connect(path_out + 'promResult.db')
        conn = con.cursor()
        conn.execute("SELECT count(id) FROM Prom WHERE adn is null")
        tot = conn.fetchone()[0]
        conn.close()
        con.close()
    except Exception as e:
        logging.exception(e)

    for i in range(nro_threads):
        i = threading.Thread(target=up1_bdd, args=(path_out,up,down,gap,tot))
        i.start()
    b = tot
    while b > 0:
        time.sleep(1)
        while True:
            try:
                con = lite.connect(path_out + 'promResult.db')
                conn = con.cursor()
                conn.execute("SELECT count(id) FROM Prom WHERE adn is null")
                # id nom cab_adn adn cod_sg_bus cod_sg_up exp
                b = conn.fetchone()[0]
                conn.close()
                con.close()
                break
            except Exception as e:
                print ("Error en la carga, se reitentará: ", e.args[0])
                if con:
                    conn.close()
                    con.close()
                time.sleep(0.25)
    print("La carga de la base de datos se realizó correctamente. :)")


'''
 __    __  .______    __     .______    _______   _______
|  |  |  | |   _  \  /_ |    |   _  \  |       \ |       \
|  |  |  | |  |_)  |  | |    |  |_)  | |  .--.  ||  .--.  |
|  |  |  | |   ___/   | |    |   _  <  |  |  |  ||  |  |  |
|  `--'  | |  |       | |    |  |_)  | |  '--'  ||  '--'  |
 \______/  | _|       |_|    |______/  |_______/ |_______/
'''
def up1_bdd(path_out,up,down,gap,tot):
    # Consultar la bdd y traer sólo los datos que tengan el adn vacío
    while True:
        try:
            con = lite.connect(path_out + 'promResult.db')
            conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
            conn.execute("SELECT nom FROM Prom WHERE adn is null ORDER BY random() LIMIT 10")
            i = conn.fetchone()
            conn.close()
            con.close()
            break
        except Exception as e:
            print("Error al traer la lista de nombres desde la base de datos: \n", e)
            logging.exception(e)
            if con:
                conn.close()
                con.close()
            time.sleep(0.5)
    # Para cada una de las consultas que tengan ADN vacio
    while i != None:
        contents = "" # cab_fasta y fasta
        op = 0 # cod_sg_up
        cod = 0 # cod_sg_bus
        opener = urllib.request.FancyURLopener({})
        fasta=[]
        # E1
        try:
            # response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
            contents = opener.open("http://solgenomics.net/search/quick?term=" + i[0] + "&x=51&y=8").read().decode(encoding='UTF-8')
            if re.search('/feature/([0-9]{8})/details',contents):
                codigo = re.search('/feature/([0-9]{8})/details',contents)
                cod = codigo.group(1)
            else:
                cod = 0
        except Exception as e:
            print ("E1 - Se ha producido un problema al acceder a la web. \n", e)
            print ("Código de promotor: ", i[0])
        # E2
        try:
            if cod != 0:
                contents = opener.open("http://solgenomics.net/feature/" + cod + "/details").read().decode(encoding='UTF-8')
            if re.search('([0-9]+):([0-9]+)..([0-9]+)">1000 bp upstream',contents):
            # Solyc01g098790 (+) Solyc04g082720 (-)
            # print seq.reverse_complement()
                if (up > 0):
                    opcion = re.search('([0-9]+):([0-9]+)..([0-9]+)">1000 bp upstream',contents)
                    dest_ud = int(opcion.group(3)) + up - 1
                    dest_gap = int(opcion.group(3)) - gap
                    op = str(opcion.group(1)) + ":" + str(dest_ud) + ".." + str(dest_gap)
                elif (down > 0):
                    opcion = re.search('([0-9]+):([0-9]+)..([0-9]+)">1000 bp downstream',contents)
                    dest_ud = int(opcion.group(3)) + down - 1 + gap
                    op = str(opcion.group(1)) + ":" + str(dest_ud) + ".." + str(opcion.group(3))
            else:
                op = 0
        except Exception as e:
            print ("E2 - Se ha producido un problema al acceder a la web.\n", e)
            print ("Código de promotor: ", i[0])
        # E3 FASTA
        try:
            if op != 0:
                contents = opener.open("http://solgenomics.net/api/v1/sequence/download/multi?format=fasta&s=" + op).read().decode(encoding='UTF-8')
                fasta = contents.split('\n',1)
            else:
                print ("E3 - Error al obtener la opción para descargar el fasta de: ", i[0])
        except Exception as e:
            print ("E3 - Se ha producido un problema al acceder a la web.\n", e)
            print ("Código de promotor: ", i[0])
        # Grabar en la Bdd
        if cod != 0 and op != 0 and len(fasta) != 0:
            while True:
                try:
                    con = lite.connect(path_out + 'promResult.db')
                    conn = con.cursor()
                    conn.execute("UPDATE Prom SET cab_adn=?,adn=?,cod_sg_bus=?,cod_sg_up=? WHERE nom = ? ",(fasta[0],fasta[1],cod,op,i[0]))
                    con.commit()
                    conn.execute("SELECT nom FROM Prom WHERE adn is null ORDER BY random() LIMIT 20")
                    i=conn.fetchone()
                    conn.execute("SELECT count(id) FROM Prom WHERE adn is null")
                    b = conn.fetchone()[0]
                    if (b > 0):
                        print("Promotores que faltan cargar: ",b)
                    conn.close()
                    con.close()
                    break
                except Exception as e:
                    print ("%s %s" % (e.args[0],threading.currentThread().getName()))
                    if con:
                        conn.close()
                        con.close()
        else:
            print("Cod, o op o fasta estan vacíos")


'''
 _______    ___           _______.___________.    ___
|   ____|  /   \         /       |           |   /   \
|  |__    /  ^  \       |   (----`---|  |----`  /  ^  \
|   __|  /  /_\  \       \   \       |  |      /  /_\  \
|  |    /  _____  \  .----)   |      |  |     /  _____  \
|__|   /__/     \__\ |_______/       |__|    /__/     \__\
'''
def crear_fas(path_out, proy_name):
    print("\n=====================")
    print("Creando archivo fasta")
    print("=====================")
    try:
        con = lite.connect(path_out + 'promResult.db')
        conn = con.cursor()
        conn.execute("SELECT * FROM Prom WHERE adn not null")
    except Exception as e:
        print("Error al conectarse a la Bdd. \n", e)
        logging.exception(e)
    file_fas = open(path_out + proy_name +'.fasta', 'w')
    for i in conn:
        try:
            file_fas.write(i[2]+"\n"+i[3])
        except Exception as e:
            print("Error guardar el archivo FASTA.\n", e)
            logging.exception(e)
            break
    file_fas.close()
    if con:
        conn.close()
        con.close()


'''
.___  ___.  _______ .___  ___.  _______
|   \/   | |   ____||   \/   | |   ____|
|  \  /  | |  |__   |  \  /  | |  |__
|  |\/|  | |   __|  |  |\/|  | |   __|
|  |  |  | |  |____ |  |  |  | |  |____
|__|  |__| |_______||__|  |__| |_______|
                                        '''
def meme(meme_path, tomtom_path, path_out, memeparam, tomtomparam, tomtombd):
    print("\n=================")
    print("Análisis con MEME")
    print("=================")
    if not (os.path.isfile(meme_path) or os.path.isfile(tomtom_path)):
        print("El path del programa MEME y/o TOMTOM es incorrecto, por favor corrija el archivo conf.ini y vuelva a ejecutar el script.\n")
        input("Presiona Enter para continuar...")
    else:
        path_fasta = path_out + proy_name +'.fasta'
        if (os.path.isfile(path_fasta)):
            os.system('export LD_LIBRARY_PATH:=$PATH:/usr/lib/openmpi/lib/') # libreria que puede traer problema con el MEME
            path_meme_out = path_out + 'meme_out/'
            try:
                meme_bash = meme_path + ' ' + path_fasta + " " + memeparam + " " + path_meme_out + "/"
                os.system(meme_bash)
            except Exception as e:
                print("Error al analizar con MEME")
                print(e)
        else:
            print("Error en el análisis de MEME: No se encuentra el archivo fasta de resultados.")

        print("\n===================")
        print("Análisis con TOMTOM")
        print("===================")
        path_meme_file = path_meme_out + "meme.txt"
        if (os.path.isfile(path_meme_file)):
            path_tomtom_out = path_out + 'tomtom_out/'
            path_dbb_out = path_out + 'tmp/'
            if not os.path.exists(path_dbb_out):
                os.makedirs(path_dbb_out)
            path_db = path_out + tomtombd
            # Descargo la Base de datos Jaspar Plants
            if not (os.path.isfile(path_db)):
                contents = ""
                opener = urllib.request.FancyURLopener({})
                try:
                    contents = opener.open("http://meme-suite.org/meme-software/index.html").read().decode(encoding='UTF-8')
                    if re.search('Databases/motifs/motif_databases.([.0-9]+).tgz',contents):
                        codigo = re.search('Databases/motifs/motif_databases.([.0-9]+).tgz',contents)
                        print ("Versión de la Bdd: ", codigo.group(1))
                    else:
                        print ("No se pudo descargar la bdd de promotores.")
                    bashCom = "wget http://meme-suite.org/meme-software/Databases/motifs/motif_databases." + codigo.group(1) + ".tgz -P " + path_dbb_out + " -c -np"
                    os.system(bashCom)
                    bashCom = " tar -xvzf " + path_dbb_out + "motif_databases." + codigo.group(1) + ".tgz" + " -C " + path_out + " > /dev/null 2>&1"
                    os.system(bashCom)
                except Exception as e:
                    print ("Se ha producido un problema al descargar la base de datos Jaspar. \n", e)
            bashCom = tomtom_path + " -oc " + path_tomtom_out + " " + tomtomparam + " " + path_meme_file + " " + path_db
            try:
                os.system(bashCom)
            except Exception as e:
                print("Error al analizar el TOMTOM. \n", e)
                logging.exception(e)
        else:
            print("Error en el análisis TOMTOM: No se encuentra el archivo MEME de entrada.")


'''
.______    __  .______    _______  __       __  .__   __.  _______
|   _  \  |  | |   _  \  |   ____||  |     |  | |  \ |  | |   ____|
|  |_)  | |  | |  |_)  | |  |__   |  |     |  | |   \|  | |  |__
|   ___/  |  | |   ___/  |   __|  |  |     |  | |  . `  | |   __|
|  |      |  | |  |      |  |____ |  `----.|  | |  |\   | |  |____
| _|      |__| | _|      |_______||_______||__| |__| \__| |_______|
                                                                   '''
def pipe(path_out,filein,proy_name,conf1,conf2,conf3,conf4,conf5,conf6,up,down,gap):
    print("========")
    print("Pipeline")
    print("========")
    inicializar(path_out,filein)
    up_bdd(conf2,path_out,up,down,gap)
    crear_fas(path_out,proy_name)
    meme(conf1,conf3,path_out,conf4,conf5,conf6)
    print("\n¡Pipeline completo! Revise los resultados en la carpeta de salida.\n")
    exit()


'''
.___  ___.      ___       __  .__   __.
|   \/   |     /   \     |  | |  \ |  |
|  \  /  |    /  ^  \    |  | |   \|  |
|  |\/|  |   /  /_\  \   |  | |  . `  |
|  |  |  |  /  _____  \  |  | |  |\   |
|__|  |__| /__/     \__\ |__| |__| \__|
                                        '''
if __name__ == '__main__':

    logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)

    parser = optparse.OptionParser()
    parser.add_option('-i', '--in', dest="filein", metavar="FILE",help='Archivo de entrada',default=None)
    parser.add_option('-o', '--out', dest="dirout", help='Proyecto de salida (default="proy")', default="proy")
    parser.add_option('-p', '--pip', dest="pipe",help='Modo pipeline (default=0)', default=0)
    parser.add_option('-u', '--up', dest="up",help='Cantidad bp upstream (default=0)', default=0)
    parser.add_option('-d', '--down', dest="down",help='Cantidad bp downstream (default=0)', default=0)
    parser.add_option('-g', '--gap', dest="gap",help='Gap de bp upstream o downstream (default=0)', default=0)
    (options, args) = parser.parse_args()

    # Revisar los parámetros ingresados por la terminal
    if not (((int(options.up) >= 0) and (int(options.down) == 0)) or ((int(options.up) == 0) and (int(options.down) >= 0))) or (int(options.up) == int(options.down) == 0):
        print('Error: Verificar los parámetros de upstream "-u" y/o downstream "-o"')
        logging.exception('Error: Verificar los parámetros de upstream "-u" y/o downstream "-o"')
        exit()
    if (options.filein == None):
        print('Error: Ingrese el nombre del archivo de entrada con el parámetro "-i"')
        logging.exception('Error: Ingrese el nombre del archivo de entrada con el parámetro "-i"')
        exit()
    if not os.path.exists(options.filein):
        print("No se encuentra el archivo de entrada.")
        logging.exception("No se encuentra el archivo de entrada.")
        exit()

    # Cargo el archivo conf.ini y lo verifico
    conf = parametros()

    path_out = os.getcwd()+ "/" + options.dirout + "_out/"
    proy_name = options.dirout
    if os.path.exists(path_out):
        while True:
            opcionMenu = input("El proyecto ya existe ¿Desea continuar con el mismo? (S/N): ")
            if opcionMenu.upper() == "S":
                break
            elif opcionMenu.upper() == "N":
                nuevoproy = input("Ingrese el nombre del nuevo proyecto: ")
                path_out = os.getcwd()+ "/" + nuevoproy + "_out/"
                proy_name = nuevoproy
                os.makedirs(path_out)
                break
    else:
        os.makedirs(path_out)

    if (conf[0] == "true") or (int(options.pipe) == 1):
        pipe(path_out,options.filein,proy_name,conf[1],conf[2],conf[3],conf[4],conf[5],conf[6],int(options.up),int(options.down),int(options.gap))
        exit()

    while True:
        menu(proy_name)
        opcionMenu = input("Ingrese una opción: ")
        if opcionMenu == "0":
            exit()
        elif opcionMenu == "1":
            inicializar(path_out,options.filein)
        elif opcionMenu == "2":
            up_bdd(conf[2],path_out,int(options.up),int(options.down),int(options.gap))
        elif opcionMenu == "3":
            crear_fas(path_out,proy_name)
        elif opcionMenu == "4":
            meme(conf[1],conf[3],path_out,conf[4],conf[5],conf[6])
        elif opcionMenu == "9":
            pipe(path_out,options.filein,proy_name,conf[1],conf[2],conf[3],conf[4],conf[5],conf[6],int(options.up),int(options.down),int(options.gap))
            exit()
        else:
            print("Opcion incorrecta. Intente de nuevo.")
