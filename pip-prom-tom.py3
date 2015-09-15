#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Simple Pipeline que extrae Promotores de genes de Tomate - Pip-Prom-Tom
Author: Alejandro Damián Pistilli <apistillAAA@unr.edu.ar> (Con el triple 'AAA' eliminado)
Implementado para acceder a la bdd de la especie de tomate: xxxxxx
Hecho in Argentina.
'''

import urllib.request
import urllib.parse
import sqlite3 as lite
import os
import threading
import re

'''
.___  ___.  _______ .__   __.  __    __
|   \/   | |   ____||  \ |  | |  |  |  |
|  \  /  | |  |__   |   \|  | |  |  |  |
|  |\/|  | |   __|  |  . `  | |  |  |  |
|  |  |  | |  |____ |  |\   | |  `--'  |
|__|  |__| |_______||__| \__|  \______/
'''
def menu():
	print()
	print("=================================================================")
	print("Bienvenido al Pip-Prom-Tom")
	print("Un Simple Pipeline que extrae Promotores de genes de Tomate.")
	print("=================================================================")
	print("Menu:")
	print(" 1 - Inicializar la Base de datos y cargar la lista de promotores")
	print(" 2 - Cargar la Bdd desde -SolGenomics-")
	print(" 3 - Crear archivo FASTA")
	print(" 4 - Análisis MEME y TOMTOM")
	print(" 9 - PIPELINE")
	print(" 0 - Salir")
	print("=================================================================")

'''
param
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
		if 'tomtom-path =' in linea:
			tomtompath = linea.split('= ')[1].rstrip('\n')
		if 'threads =' in linea:
			nro_threads = int(linea.split('= ')[1].rstrip('\n'))
	file_param.close()
	return(pip_pip,memepath,nro_threads,tomtompath)


'''
 __  .__   __.  __    ______  __       ___       __       __   ________      ___      .______
|  | |  \ |  | |  |  /      ||  |     /   \     |  |     |  | |       /     /   \     |   _  \
|  | |   \|  | |  | |  ,----'|  |    /  ^  \    |  |     |  | `---/  /     /  ^  \    |  |_)  |
|  | |  . `  | |  | |  |     |  |   /  /_\  \   |  |     |  |    /  /     /  /_\  \   |      /
|  | |  |\   | |  | |  `----.|  |  /  _____  \  |  `----.|  |   /  /----./  _____  \  |  |\  \----.
|__| |__| \__| |__|  \______||__| /__/     \__\ |_______||__|  /________/__/     \__\ | _| `._____|

'''
def inicializar():
	print("==============")
	print("Inicialización")
	print("==============")
	# Agregar verificación si sale todo bien
	# Agregar el borrado de prom.db, .tmp, meme_out, o meter todo dentro de una carpeta con el nombre del trabajo
	try:
		os.system('sqlite3 prom.db &')
		con = lite.connect('prom.db')
		conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
		conn.execute("DROP TABLE IF EXISTS Prom") # Elimnar la Bdd
		conn.execute("CREATE TABLE Prom(id INTEGER DEFAULT 1 PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT UNIQUE NOT NULL, cab_adn TEXT, adn TEXT, cod_sg_bus TEXT, cod_sg_up TEXT)") # Crear las tablas de la bdd
		# id nom cab_adn adn cod_sg_bus cod_sg_up exp
		con.commit() # Confirmar los cambios
	except lite.Error as e:
		print("Error borrar la tabla y crear Bdd: ", e.args[0])
	# Abrir el archivo con lista de los promotores
	try:
		file_list_prom = open('exa_prom.txt', 'r')
		list_prom = file_list_prom.read()
		file_list_prom.close()
	except:
		print("Error al abrir el archivo: exa_prom.txt")
	list_prom = list_prom.split('\n')
	print(len(list_prom))
	# Cargar la Bdd
	for i in list_prom:
		try:
			print(i)
			if ([i] != '\n') or ([i] != ''):
				conn.execute("INSERT INTO Prom(id,nom) VALUES(null,?)",([i]))
		except lite.Error as e:
			print("Error al cargar la Bdd: ", e.args[0])
	# Grabar los cambios en la Bdd
	try:
		con.commit()
		print("Bdd entrada cargada.")
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
def up_bdd(nro_threads):
	print("=========================================")
	print("Cargando las secuencias desde SolGenomics")
	print("=========================================")
	print("Cantidad de threads lanzados: ", nro_threads)
	for i in range(nro_threads):
		i = threading.Thread(target=up1_bdd)
		i.start()
	b = 1
	while b > 0:
		time.sleep(3)
		while True:
			try:
				con = lite.connect('prom.db')
				conn = con.cursor()
				conn.execute("SELECT count(id) FROM Prom WHERE adn is null")
				# id nom cab_adn adn cod_sg_bus cod_sg_up exp
				b = conn.fetchone()[0]
				print("Promotores que faltan cargar: ",b)
				conn.close()
				con.close()
				break
			except Exception as e:
				print ("Desliz en la carga: ", e.args[0])
				if con:
					conn.close()
					con.close()
				time.sleep(0.25)
		#print("Porcentaje de carga: %3.2f Procesados: %4d Faltantes: %4d" % (round((2497-b[0])*100/2497,2),2497-b[0],b[0]))
	time.sleep(5)
	print("La carga de la Base de datos se realizó correctamente. :)")


'''
 __    __  .______    __     .______    _______   _______
|  |  |  | |   _  \  /_ |    |   _  \  |       \ |       \
|  |  |  | |  |_)  |  | |    |  |_)  | |  .--.  ||  .--.  |
|  |  |  | |   ___/   | |    |   _  <  |  |  |  ||  |  |  |
|  `--'  | |  |       | |    |  |_)  | |  '--'  ||  '--'  |
 \______/  | _|       |_|    |______/  |_______/ |_______/
'''
def up1_bdd():
	# Consultar la bdd y traer sólo los datos que tengan el adn vacío
	while True:
		try:
			con = lite.connect('prom.db')
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
		cod = 0 # cod_sg_bus8
		opener = urllib.request.FancyURLopener({})
		fasta=[]
		# PRIMERA ETAPA buscar el cod
		try:
			# response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
			contents = opener.open("http://solgenomics.net/search/quick?term="+i[0]+"&x=51&y=8").read().decode(encoding='UTF-8')
			# contents = opener.open("http://solgenomics.net/search/quick?term=Solyc01g080620&x=51&y=8").read().decode(encoding='UTF-8')
			if re.search('/feature/([0-9]{8})/details',contents):
				codigo = re.search('/feature/([0-9]{8})/details',contents)
				cod = codigo.group(1)
			else:
				cod = 0
		except Exception as probl:
			print ("E1 - Se ha producido un problema al acceder a la web")
			print (i[0])
			print (probl)
		# Segunda etapa 1000 upstream
		try:
			if cod != 0:
				contents = opener.open("http://solgenomics.net/feature/" + cod + "/details").read().decode(encoding='UTF-8')
			if re.search('([0-9]+:[0-9]+..[0-9]+)">1000 bp upstream',contents):
				opcion = re.search('([0-9]+:[0-9]+..[0-9]+)">1000 bp upstream',contents)
				op = opcion.group(1)
			else:
				op = 0
		except Exception as probl:
			print ("E2 - Se ha producido un problema al acceder a la web")
			print (i[0])
			print (probl)
		# Tercera etapa bajo el FASTA
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
					con = lite.connect('prom.db')
					conn = con.cursor()
					conn.execute("UPDATE Prom SET cab_adn=?,adn=?,cod_sg_bus=?,cod_sg_up=? WHERE nom = ? ",(fasta[0],fasta[1],cod,op,i[0]))
					con.commit()
					conn.execute("SELECT nom FROM Prom WHERE adn is null ORDER BY random() LIMIT 30")
					i=conn.fetchone()
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
  ______ .______       _______     ___      .______          _______    ___           _______.___________.    ___      
 /      ||   _  \     |   ____|   /   \     |   _  \        |   ____|  /   \         /       |           |   /   \     
|  ,----'|  |_)  |    |  |__     /  ^  \    |  |_)  |       |  |__    /  ^  \       |   (----`---|  |----`  /  ^  \    
|  |     |      /     |   __|   /  /_\  \   |      /        |   __|  /  /_\  \       \   \       |  |      /  /_\  \   
|  `----.|  |\  \----.|  |____ /  _____  \  |  |\  \----.   |  |    /  _____  \  .----)   |      |  |     /  _____  \  
 \______|| _| `._____||_______/__/     \__\ | _| `._____|   |__|   /__/     \__\ |_______/       |__|    /__/     \__\ 
                                                                                                                       
'''
def crear_fas():
	print("Generando archivos fasta...")
	try:
		con = lite.connect('prom.db')
		conn = con.cursor()
		conn.execute("SELECT * FROM Prom WHERE adn not null")
	except Exception as e:
		print("Error: SELECT DISTINCT fam FROM Prom", e.args[0])
	file_fam = open('prom_res.fasta', 'w')
	for i in conn:
		try:
			file_fam.write(i[2]+"\n"+i[3])
		except Exception as probl:
			print("Error guardar en familia")
			print(probl)
			break
	file_fam.close()
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
def meme(meme_path, tomtom_path):
	# bc="export PATH=$PATH:" + os.getcwd() + "/meme/bin; "
	# bc=("export PATH=$PATH:$HOME/meme/bin;") # para que se ubique el meme
	print("=================")
	print("Análisis con MEME")
	print("=================")
	os.system('export LD_LIBRARY_PATH:=$PATH:/usr/lib/openmpi/lib/') # libreria que puede traer problema con el MEME descargado de AUR
	path_meme_out = os.getcwd() + '/meme_out/'
	if not os.path.exists(path_meme_out):
		os.makedirs(path_meme_out)
	try:
		path_fasta = os.getcwd() + "/prom_res.fasta"
		# dna -mod oops -w 8 -minw 6 -maxw 8 -nmotifs 5 -psp dna4_8.psp -revcomp -maxsize 1000000000000 -o
		# bashCom = bc + 'meme ' + path + " -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc "+ path_meme_out + f + "/"
		meme_bash = meme_path + ' ' + path_fasta + " -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc " + path_meme_out + "/"
		os.system(meme_bash)
	except Exception as e:
		print("Error al analizar con MEME")
		print(e)
	print("===================")
	print("Análisis con TOMTOM")
	print("===================")
	# bc=("export PATH=$PATH:$HOME/meme/bin;")
	path_tomtom_out = os.getcwd() + '/tomtom_out/'
	if not os.path.exists(path_tomtom_out):
		os.makedirs(path_tomtom_out)
	contents = "" 
	opener = urllib.request.FancyURLopener({})
	try:
		contents = opener.open("http://meme-suite.org/meme-software/index.html").read().decode(encoding='UTF-8')
		if re.search('Databases/motifs/motif_databases.([.0-9]+).tgz',contents):
			codigo = re.search('Databases/motifs/motif_databases.([.0-9]+).tgz',contents)
			print ("Versión de la Bdd: ", codigo.group(1))
		else:
			print ("No se pudo descargar la bdd de motivos.")
	except Exception as probl:
		print ("TT - Se ha producido un problema al descargar la bdd de motivos")
		print (probl)
	path_dbb_out = os.getcwd() + '/.tmp/'
	if not os.path.exists(path_dbb_out):
		os.makedirs(path_dbb_out)
	bashCom = "wget http://meme-suite.org/meme-software/Databases/motifs/motif_databases." + codigo.group(1) + ".tgz -P " + path_dbb_out + " -c -np"
	os.system(bashCom)
	bashCom = " tar -xvzf " + path_dbb_out + "motif_databases." + codigo.group(1) + ".tgz"
	os.system(bashCom)

	path_db = os.getcwd() + "/motif_databases/JASPAR/JASPAR_CORE_2014_plants.meme"
	try:
		path_meme_file = path_meme_out + "meme.txt"
		# tomtom -oc tomtom_example_output_files -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc STRGGTCAN.meme JASPAR_CORE_2009.meme
		# tomtom -oc trial -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc motiflist.meme databaselist.meme
		# bashCom = bc + 'tomtom ' + " -oc " + path_tomtom + f + "/ -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc " + path + " " + path_db
		bashCom = tomtom_path + " -oc " + path_tomtom_out + " -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc " + path_meme_file + " " + path_db
		os.system(bashCom)
	except Exception as e:
		print("Error al analizar el TOMTOM")
		print(e[0])
		print(i[0])

		# Borrar tmp

'''
.______    __  .______    _______  __       __  .__   __.  _______
|   _  \  |  | |   _  \  |   ____||  |     |  | |  \ |  | |   ____|
|  |_)  | |  | |  |_)  | |  |__   |  |     |  | |   \|  | |  |__
|   ___/  |  | |   ___/  |   __|  |  |     |  | |  . `  | |   __|
|  |      |  | |  |      |  |____ |  `----.|  | |  |\   | |  |____
| _|      |__| | _|      |_______||_______||__| |__| \__| |_______|
                                                                   '''
def pipe():
	print("========")
	print("Pipeline")
	print("========")
	inicializar()
	up_bdd(conf[2])
	crear_fas()
	meme(conf[1],conf[3])
	print("¡Pipeline completo! Revise los resultados.")

'''
.___  ___.      ___       __  .__   __.
|   \/   |     /   \     |  | |  \ |  |
|  \  /  |    /  ^  \    |  | |   \|  |
|  |\/|  |   /  /_\  \   |  | |  . `  |
|  |  |  |  /  _____  \  |  | |  |\   |
|__|  |__| /__/     \__\ |__| |__| \__|
                                        '''
if __name__ == '__main__':
	pip_pip = "false"
	conf = parametros()
	print (conf)
	if pip_pip == "true":
		pipe()
	while True:
		menu()
		opcionMenu = input("Ingrese una opción: ")
		if opcionMenu == "0":
			exit()
		elif opcionMenu == "1":
			inicializar()
		elif opcionMenu == "2":
			up_bdd(conf[2])
		elif opcionMenu == "3":
			crear_fas()
		elif opcionMenu == "4":
			meme(conf[1],conf[3])
		elif opcionMenu == "9":
			pipe()
		##########################################################################
		# elif opcionMenu == "--":
		##########################################################################
		else:
			print("Opcion incorrecta. Intente de nuevo.")