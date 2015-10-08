#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Pip-Prom-Tom
Descripción: Un pipeline que extrae promotores de tomate de la especie 
            Solanum lycopersicum desde la web Solgenomics
Autor: Alejandro Damián Pistilli <apistillAAA@unr.edu.ar> (Con el triple 'AAA' eliminado)
Hecho Zavalla, Argentina
'''

import urllib.request
import urllib.parse
import sqlite3 as lite
import time
import os
import threading
import re
import optparse

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
    print("=================================================================")
    print("Bienvenido al Pip-Prom-Tom - Nombre del proyecto: ", proy)
    print("Un Pipeline para extrae Promotores de genes de Tomate.")
    print("=================================================================")
    print("Menu:")
    print(" 1 - Inicializar Proyecto y cargar la lista de promotores")
    print(" 2 - Cargar la Bdd desde -SolGenomics-")
    print(" 3 - Crear archivo FASTA")
    print(" 4 - Análisis MEME y TOMTOM")
    print(" 9 - PIPELINE")
    print(" 0 - Salir")
    print("=================================================================")
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
    except:
        print("Error al abrir el archivo de configuración")
        exit()
    for linea in file_param.readlines():
        # Averiguo si el script debe ejecutarse en modo pipeline o mostrar menú
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
        if 'threads =' in linea:
            try:
                nro_threads = int(linea.split('= ')[1].rstrip('\n'))
            except Exception as e:
                print("El número de threads es incorrecto, por favor corrija el archivo conf.ini")
                print(e)
                file_param.close()
                exit()
    file_param.close()
    return(pip_pip,memepath,nro_threads,tomtompath,memeparam,tomtomparam)


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
        os.system('sqlite3 '+ path_out + 'prom.db &')
        con = lite.connect(path_out + 'prom.db')
        conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
        conn.execute("DROP TABLE IF EXISTS Prom") # Elimnar la Bdd
        conn.execute("CREATE TABLE Prom(id INTEGER DEFAULT 1 PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT UNIQUE NOT NULL, cab_adn TEXT, adn TEXT, cod_sg_bus TEXT, cod_sg_up TEXT)") # Crear las tablas de la bdd
        # id nom cab_adn adn cod_sg_bus cod_sg_up exp
        con.commit() # Confirmar los cambios
    except lite.Error as e:
        print("Error al crear Bdd: ")
        print(e)
        exit()
    # Abrir el archivo con lista de los promotores
    try:
        file_list_prom = open(filein, 'r')
        list_prom = file_list_prom.read()
        file_list_prom.close()
    except:
        print("Error al abrir el archivo de entrada")
    list_prom = list_prom.split('\n')
    # Cargar la Bdd
    for i in list_prom:
        try:
            print(i)
            if ([i] != '\n') or ([i] != '') or ([i] != ' '):
                conn.execute("INSERT INTO Prom(id,nom) VALUES(null,?)",([i]))
        except lite.Error as e:
            print("Error al cargar la Bdd: ", e.args[0])
    # Grabar los cambios en la Bdd
    try:
        con.commit()
        print("\nCódigo de promotores cargados.")
    except lite.Error as e:
        print("Commit error Bdd entrada: ", e.args[0])
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

    for i in range(nro_threads):
        i = threading.Thread(target=up1_bdd, args=(path_out,up,down,gap))
        i.start()
    b = 1
    while b > 0:
        time.sleep(1)
        while True:
            try:
                con = lite.connect(path_out + 'prom.db')
                conn = con.cursor()
                conn.execute("SELECT count(id) FROM Prom WHERE adn is null")
                # id nom cab_adn adn cod_sg_bus cod_sg_up exp
                b = conn.fetchone()[0]
                conn.close()
                con.close()
                break
            except Exception as e:
                print ("Desliz en la carga: ", e.args[0])
                if con:
                    conn.close()
                    con.close()
                time.sleep(0.25)
        # print("Porcentaje de carga: %3.2f Procesados: %4d Faltantes: %4d" % (round((2497-b[0])*100/2497,2),2497-b[0],b[0]))
    print("La carga de la Base de datos se realizó correctamente. :)")


'''
 __    __  .______    __     .______    _______   _______
|  |  |  | |   _  \  /_ |    |   _  \  |       \ |       \
|  |  |  | |  |_)  |  | |    |  |_)  | |  .--.  ||  .--.  |
|  |  |  | |   ___/   | |    |   _  <  |  |  |  ||  |  |  |
|  `--'  | |  |       | |    |  |_)  | |  '--'  ||  '--'  |
 \______/  | _|       |_|    |______/  |_______/ |_______/
'''
def up1_bdd(path_out,up,down,gap):
    # Consultar la bdd y traer sólo los datos que tengan el adn vacío
    while True:
        try:
            con = lite.connect(path_out + 'prom.db')
            conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
            conn.execute("SELECT nom FROM Prom WHERE adn is null ORDER BY random() LIMIT 10")
            i=conn.fetchone()
            conn.close()
            con.close()
            break
        except Exception as e:
            print("Error al traer la lista de nom desde la Bdd", e.args[0])
            if con:
                conn.close()
                con.close()
            time.sleep(0.5) # Esperar para volver a intentar acceder a la bdd
    # Para cada una de las consultas que tengan ADN vacio
    while i != None:
        contents = "" # cab_fasta y fasta
        op = 0 # cod_sg_up
        cod = 0 # cod_sg_bus
        opener = urllib.request.FancyURLopener({})
        fasta=[]
        # E1 buscar el cod
        try:
            # response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
            contents = opener.open("http://solgenomics.net/search/quick?term=" + i[0] + "&x=51&y=8").read().decode(encoding='UTF-8')
            if re.search('/feature/([0-9]{8})/details',contents):
                codigo = re.search('/feature/([0-9]{8})/details',contents)
                cod = codigo.group(1)
            else:
                cod = 0
        except Exception as probl:
            print ("E1 - Se ha producido un problema al acceder a la web")
            print (i[0])
            print (probl)
        # E2
        try:
            if cod != 0:
                contents = opener.open("http://solgenomics.net/feature/" + cod + "/details").read().decode(encoding='UTF-8')
            if re.search('([0-9]+):([0-9]+)..([0-9]+)">1000 bp upstream',contents):
            # Ver el tema de las hebras positivas y negativas para luego hacer el reverso complementario
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
        except Exception as probl:
            print ("E2 - Se ha producido un problema al acceder a la web")
            print (i[0])
            print (probl)
        # E3 FASTA
        try:
            if op != 0:
                contents = opener.open("http://solgenomics.net/api/v1/sequence/download/multi?format=fasta&s=" + op).read().decode(encoding='UTF-8')
                fasta = contents.split('\n',1)
            else:
                print ("E3 - Error al obtener la opción para descargar el fasta de: ", i[0])
        except Exception as probl:
            print ("E3 - Se ha producido un problema al acceder a la web")
            print (i[0])
            print (probl)
        # Grabar en la Bdd
        if cod != 0 and op != 0 and len(fasta) != 0:
            while True:
                try:
                    con = lite.connect(path_out + 'prom.db')
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
            print("Cod, o op o fasta estan vacios")


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
        con = lite.connect(path_out + 'prom.db')
        conn = con.cursor()
        conn.execute("SELECT * FROM Prom WHERE adn not null")
    except Exception as e:
        print("Error", e.args[0])
    file_fas = open(path_out + proy_name +'.fasta', 'w')
    for i in conn:
        try:
            file_fas.write(i[2]+"\n"+i[3])
        except Exception as probl:
            print("Error guardar el fasta")
            print(probl)
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
def meme(meme_path, tomtom_path, path_out, memeparam, tomtomparam):
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
            path_db = path_out + "motif_databases/JASPAR/JASPAR_CORE_2014_plants.meme"
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
                except Exception as probl:
                    print ("TT - Se ha producido un problema al descargar la bdd de promotores")
                    print (probl)
            try:
                bashCom = tomtom_path + " -oc " + path_tomtom_out + " " + tomtomparam + " " + path_meme_file + " " + path_db
                os.system(bashCom)
            except Exception as e:
                print("Error al analizar el TOMTOM")
                print(i[0])
                print(e[0])
        else:
            print("Error en el análisis TOMTOM: No se encuentra el archivo MEME de entrada.")


# PLANT CARE
def plantcare(path_out, proy_name):
    print("\n==================")
    print("Análisis PlantCare")
    print("==================")
    try:
        con = lite.connect(path_out + 'prom.db')
        conn = con.cursor()
        conn.execute("SELECT * FROM Prom WHERE adn not null")
    except Exception as e:
        print("Error Bdd", e.args[0])
    for i in conn:
        try:
            # file_fas.write(i[2]+"\n"+i[3])
            bashCom = "python2 plantcare.py" 
            os.system(bashCom)
        except Exception as probl:
            print("Error guardar el fasta")
            print(probl)
            break
    if con:
        conn.close()
        con.close()

'''
.______    __  .______    _______  __       __  .__   __.  _______
|   _  \  |  | |   _  \  |   ____||  |     |  | |  \ |  | |   ____|
|  |_)  | |  | |  |_)  | |  |__   |  |     |  | |   \|  | |  |__
|   ___/  |  | |   ___/  |   __|  |  |     |  | |  . `  | |   __|
|  |      |  | |  |      |  |____ |  `----.|  | |  |\   | |  |____
| _|      |__| | _|      |_______||_______||__| |__| \__| |_______|
                                                                   '''
def pipe(path_out,filein,proy_name,conf1,conf2,conf3,conf4,conf5):
    print("========")
    print("Pipeline")
    print("========")
    inicializar(path_out,filein)
    up_bdd(conf2,path_out)
    crear_fas(path_out,proy_name)
    meme(conf1,conf3,path_out,conf4,conf5)
    print("\n¡Pipeline completo! Revise los resultados.\n")
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

    parser = optparse.OptionParser()
    parser.add_option('-i', '--in', dest="filein", metavar="FILE",help='Archivo de entrada',default=None)
    parser.add_option('-o', '--out', dest="dirout", help='Proyecto de salida (default="proy")', default="proy")
    parser.add_option('-p', '--pip', dest="pipe",help='Modo pipeline (default=0)', default=0)
    parser.add_option('-u', '--up', dest="up",help='Cantidad bp upstream (default=0)', default=0)
    parser.add_option('-d', '--down', dest="down",help='Cantidad bp downstream (default=0)', default=0)
    parser.add_option('-g', '--gap', dest="gap",help='Gap de bp upstream o downstream (default=0)', default=0)
    (options, args) = parser.parse_args()

    # revisar los parse
    if not (((int(options.up) >= 0) and (int(options.down) == 0)) or ((int(options.up) == 0) and (int(options.down) >= 0))) or (int(options.up) == int(options.down) == 0):
        print('Error: Verificar los parámetros de upstream "-u" y/o downstream "-o"')
        exit()
    print(options.filein)
    if (options.filein == None):
        print('Error: Ingrese el nombre del archivo de entrada con el parámetro "-i"')
        exit()

    conf = parametros()

    if os.path.exists(options.filein):
        path_out = os.getcwd()+ "/" + options.dirout + "_out/"
        proy_name = options.dirout
        if os.path.exists(path_out):
            while True:
                opcionMenu = input("El proyecto ya existe ¿Desea continuar con el mismo? (s/n): ")
                if opcionMenu == "s":
                    break
                elif opcionMenu == "n":
                    nuevoproy = input("Ingrese el nombre del nuevo proyecto: ")
                    path_out = os.getcwd()+ "/" + nuevoproy + "_out/"
                    proy_name = nuevoproy
                    os.makedirs(path_out)
                    break
        else:
            os.makedirs(path_out)

        if (conf[0] == "true") or (options.pipe == 1):
            pipe(path_out,options.filein,proy_name,conf[1],conf[2],conf[3],conf[4],conf[5])
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
                meme(conf[1],conf[3],path_out,conf[4],conf[5])
            #elif opcionMenu == "5":
            #    meme(conf[1],conf[3],path_out,conf[4],conf[5])
            elif opcionMenu == "9":
                pipe(path_out,options.filein,proy_name,conf[1],conf[2],conf[3],conf[4],conf[5])
            ###################################################################################################
            #elif opcionMenu == "--":

            else:
                print("Opcion incorrecta. Intente de nuevo.")
    else:
        print("No se encuentra el archivo de entrada.")
