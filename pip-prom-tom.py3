#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Simple Pipeline que extrae Promotores de genes de Tomate - Pip-Prom-Tom
Author: Alejandro Damián Pistilli <apistillAAA@unr.edu.ar> (Con el triple 'AAA' eliminado)
'''

import urllib.request
import urllib.parse
import sqlite3 as lite
import time
import os
import threading

'''
.___  ___.  _______ .__   __.  __    __  
|   \/   | |   ____||  \ |  | |  |  |  | 
|  \  /  | |  |__   |   \|  | |  |  |  | 
|  |\/|  | |   __|  |  . `  | |  |  |  | 
|  |  |  | |  |____ |  |\   | |  `--'  | 
|__|  |__| |_______||__| \__|  \______/  
'''
def menu():
	print("Bienvenido al Pip-Prom-Tom")
	print("Un Simple Pipeline que extrae Promotores de genes de Tomate.")
	##############
	print("Menu:")
	print(" 1 - Inicializar la Base de datos y cargar la lista de promotores")
	print(" 2 - Cargar la Bdd desde -SolGenomics- y armarse de paciencia")
	print(" 3 - Crear archivos FASTA por Familia")
	print(" 4 - Análisis MEME")
	print(" 5 - Análisis TOMTOM")
	print(" 6 - Análisis PlantCare")
	print(" 10 - PIPELINE")
	print(" 0 - Salir")
	##############


def parametros():
	try:
		file_param = open('init.conf', 'r')
	except: 
		print("Error al abrir el archivo de configuración")
		exit()
	for linea in file_param.readlines():
		# Averiguo si el script debe ejecutarse en modo pipeline o mostrar menú
		if 'pipeline =' in linea:
			pip_pip = linea.split('= ')[1]
		if 'meme-path =' in linea:
			memepath = linea.split('= ')[1]
		if 'threads =' in linea:
			nro_threads = linea.split('= ')[1]
	file_param.close()


'''
 __  .__   __.  __    ______  __       ___       __       __   ________      ___      .______      
|  | |  \ |  | |  |  /      ||  |     /   \     |  |     |  | |       /     /   \     |   _  \     
|  | |   \|  | |  | |  ,----'|  |    /  ^  \    |  |     |  | `---/  /     /  ^  \    |  |_)  |    
|  | |  . `  | |  | |  |     |  |   /  /_\  \   |  |     |  |    /  /     /  /_\  \   |      /     
|  | |  |\   | |  | |  `----.|  |  /  _____  \  |  `----.|  |   /  /----./  _____  \  |  |\  \----.
|__| |__| \__| |__|  \______||__| /__/     \__\ |_______||__|  /________/__/     \__\ | _| `._____|
                                                                                                   
'''
def inicializar():
	print("Inicialización")
	try:
		con = lite.connect('prom.db')
		conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
		conn.execute("DROP TABLE IF EXISTS Prom") # Elimnar la Bdd
		conn.execute("CREATE TABLE Prom(nom TEXT UNIQUE NOT NULL, fam TEXT, mf TEXT, cab_adn TEXT, adn TEXT, cod_sg_bus TEXT, cod_sg_up TEXT, exp TEXT)") # Crear las tablas de la bdd
		con.commit()
	except lite.Error as e:
		print("Error borrar la tabla y crear Bdd: ", e.args[0])
	# Abrir el archivo con los datos de los promotores
	try:
		file_list_prom = open('exa_prom.txt', 'r')
		list_prom = file_list_prom.read()
		file_list_prom.close()
	except: 
		print("Error al abrir el archivo: exa_prom.txt")
	list_prom = list_prom.split('\n')
	try:
		list_prom.remove('')
	except:
		print("list_prom sin vacio")
	# Cargar la Bdd
	for i in list_prom:
		i=i.split('\t')
		try:
			conn.execute("INSERT INTO Prom (nom,fam,mf) VALUES(?,?,?)",(i[0],i[1],i[2]))
		except:
			print("error en Insert 1")
	# Grabar los cambios en la Bdd
	try: 
		con.commit()
		print("Bdd entrada cargada.")
	except:
		print("Commit error Bdd entrada")
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
def up_bdd():
	for i in range(nro_threads):
		i = threading.Thread(target=up1_bdd)
		i.start()
	b = 1
	while b > 0:
		time.sleep(3)
		while True:
			try:
				con = lite.connect('prom.db')
				conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
				conn.execute("SELECT count(nom) FROM Prom WHERE adn is null")
				b = conn.fetchone()
				conn.close()
				con.close()
				break
			except Exception as e:
				print (e.args[0])
				if con:
					conn.close()
					con.close()
				time.sleep(0.25)
		#os.system('cls' if os.name == 'nt' else 'clear')
		#print("Porcentaje de carga: %3.2f Procesados: %4d Faltantes: %4d" % (round((2497-b[0])*100/2497,2),2497-b[0],b[0]))
	time.sleep(5)
	print("Carga exitosa :)")


'''
 __    __  .______    __     .______    _______   _______  
|  |  |  | |   _  \  /_ |    |   _  \  |       \ |       \ 
|  |  |  | |  |_)  |  | |    |  |_)  | |  .--.  ||  .--.  |
|  |  |  | |   ___/   | |    |   _  <  |  |  |  ||  |  |  |
|  `--'  | |  |       | |    |  |_)  | |  '--'  ||  '--'  |
 \______/  | _|       |_|    |______/  |_______/ |_______/ 
'''
def up1_bdd():
	# Consultar la bdd y traer sólo los datos que tengan el adn vacio y luego armar una lista y grabar
	numeros = "1234567890" # Para buscar el codigo dentro del html
	caracteres = "1234567890." # Para buscar los caracteres dentro del 1000 up
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
			print("Error al traer la lista de nom desde la Bdd")
			if con:
				conn.close()
				con.close()
			time.sleep(0.5) # Esperar para volver a intentar acceder a la bdd
	# Para cada una de las consultas que tengan ADN vacio
	while i != None:
		# Inicializacion dentro del For
		opener = ""
		url = ""
		f= ""
		content = ""
		contents = "" #  cab_fasta y fasta
		op = "" # cod_sg_up
		cod = "" # cod_sg_bus8
		opener = urllib.request.FancyURLopener({})
		fasta=[]
		# PRIMERA ETAPA buscar el cod
		try:
			url = "http://solgenomics.net/search/quick?term="+i[0]+"&x=51&y=8"
			f = opener.open(url)
			# response = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
			content = f.read()
			contents = content.decode(encoding='UTF-8')
			if contents.find("Genomic detail") >= 0:
				contents= contents.split('/details">')[0]
				contents= contents.split('Genomic detail')[1]
				if len(contents) != 0:
					for ele in contents:
						if ele in numeros:
							cod+=ele
			else:
				cod = "NoGenDet";
		except Exception as problema:
			print ("1- Se ha producido un problema al acceder a la web:" + url)
			print (problema)
		# Segunda etapa 1000 upstream
		try:
			if cod != "NoGenDet":
				url = "http://solgenomics.net/feature/" + cod + "/details"
				f = opener.open(url)
				content = f.read()
				contents= content.decode(encoding='UTF-8')
				contents= contents.split(">1000 bp upstream</option>")[0]
				contents= contents.split("3000 bp upstream</option>")[1]
			else:
				contents= contents.split(">1000 bp upstream</option>")[0]
				contents= contents.split("3000 bp upstream</option>")[1]
		except Exception as problema:
			print ("2 - Se ha producido un problema al acceder a la web:" + url)
			print (problema)
		if len(contents) != 0:
			for ele in contents:
				if ele in caracteres:
					op+=ele
				else:
					if ele == ":":
						op+="%3A"
		# Tercera etapa bajo el FASTA y doy forma
		try:
			url = "http://solgenomics.net/api/v1/sequence/download/multi?format=fasta&s=" + op
			f = opener.open(url)
			content = f.read()
			contents = content.decode(encoding='UTF-8')
			fasta = contents.split('\n',1)
		except Exception as problema:
			print ("3 - Se ha producido un problema al acceder a la web:" + url)
			print (problema)
		# Grabar en la Bdd
		if cod != '' and op !='' and len(fasta)!=0:
			while True:
				try:
					con = lite.connect('prom.db')
					conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
					conn.execute("UPDATE Prom SET cab_adn=?,adn=?,cod_sg_bus=?,cod_sg_up=? WHERE nom = ? ",(fasta[0],fasta[1],cod,op,i[0])) # Guardo los datos extraids en la bdd
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
					# time.sleep(1)
		else:
			print("Cod, o op o fasta estan vacios")


'''
  ______     ___      .______        _______      ___      .______          _______    ___      .___  ___. 
 /      |   /   \     |   _  \      /  _____|    /   \     |   _  \        |   ____|  /   \     |   \/   | 
|  ,----'  /  ^  \    |  |_)  |    |  |  __     /  ^  \    |  |_)  |       |  |__    /  ^  \    |  \  /  | 
|  |      /  /_\  \   |      /     |  | |_ |   /  /_\  \   |      /        |   __|  /  /_\  \   |  |\/|  | 
|  `----./  _____  \  |  |\  \----.|  |__| |  /  _____  \  |  |\  \----.   |  |    /  _____  \  |  |  |  | 
 \______/__/     \__\ | _| `._____| \______| /__/     \__\ | _| `._____|   |__|   /__/     \__\ |__|  |__| 
                                                                                                           
'''
def cargar_fam():
	# Crear todas las familias
	print("Crear todas las familias y generando archivos fasta...")
	try: 
		con = lite.connect('prom.db')
		conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
		conn.execute("select distinct fam from Prom")
	except:
		print("Error: select distinct fam from Prom")
	for i in conn:
		try:
			f=i[0].replace("/","--")
			f=f.replace(" ","-")
			file_fam = open(os.getcwd()+'/Fam/'+ f +'.fasta', 'w')
			file_fam.close()
		except:
			print("Error crear familias fasta")
			print(i)
			break
	conn.execute("SELECT * FROM Prom WHERE adn not null")
	for i in conn:
		try:
			f=i[1].replace("/","--")
			f=f.replace(" ","-")
			file_fam = open(os.getcwd()+'/Fam/'+ f +'.fasta', 'a')
			file_fam.write(i[3]+"\t"+i[0]+"\t"+i[1]+"\t"+i[2]+"\n"+i[4]+"\n")
			file_fam.close()
		except:
			print("Error guardar en familia")
			print(i)
			break
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
def meme():
	# bc="export PATH=$PATH:" + os.getcwd() + "/meme/bin; " 
	# bc=("export PATH=$PATH:$HOME/meme/bin;") # para que se ubiqeu el meme
	path_meme = os.getcwd()+'/meme_out/'
	if not os.path.exists(path_meme):
		os.makedirs(path_meme)
	try: 
		con = lite.connect('prom.db')
		conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
		conn.execute("select distinct fam from Prom")
	except:
		print("Error: select distinct fam from Prom")
	for i in conn:
		try:
			f=i[0].replace("/","--")
			f=f.replace(" ","-")
			path = os.getcwd()+'/Fam/'+ f +".fasta"
			if (len(open(path,'r').readlines())) > 25: #Sólo proceso del Meme las familias con más de un promotor
				# dna -mod oops -w 8 -minw 6 -maxw 8 -nmotifs 5 -psp dna4_8.psp -revcomp -maxsize 1000000000000 -o
				# bashCom = bc + 'meme ' + path + " -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc "+ path_meme + f + "/"
				bashCom = 'meme-meme ' + path + " -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc "+ path_meme + f + "/"
				os.system(bashCom)
		except Exception as e:
			print("Error al analizar el meme por familias fasta")
			print(e[0])
	if con:
		conn.close()
		con.close()


'''
.___________.  ______   .___  ___. .___________.  ______   .___  ___. 
|           | /  __  \  |   \/   | |           | /  __  \  |   \/   | 
`---|  |----`|  |  |  | |  \  /  | `---|  |----`|  |  |  | |  \  /  | 
    |  |     |  |  |  | |  |\/|  |     |  |     |  |  |  | |  |\/|  | 
    |  |     |  `--'  | |  |  |  |     |  |     |  `--'  | |  |  |  | 
    |__|      \______/  |__|  |__|     |__|      \______/  |__|  |__| 
                                                                      '''
def tomtom():
	print("Análisis con TOMTOM")
	#bc=("export PATH=$PATH:$HOME/meme/bin;")
	path_tomtom = os.getcwd()+'/tomtom_out/'
	if not os.path.exists(path_tomtom):
		os.makedirs(path_tomtom)
	# http://meme-suite.org/meme-software/Databases/motifs/motif_databases.12.7.tgz
	path_db = os.getcwd() + "/motif_databases/JASPAR_CORE_2014_plants.meme"
	try: 
		con = lite.connect('prom.db')
		conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
		conn.execute("SELECT DISTINCT fam FROM Prom")
	except:
		print("Error tomtom: select distinct fam from Prom")
	for i in conn:
		try:
			f=i[0].replace("/","--")
			f=i[0].replace("/","--")
			f=f.replace(" ","-")
			path = os.getcwd()+'/meme_out/'+ f +"/meme.txt" # meme
			path_fasta = os.getcwd()+'/Fam/'+ f +".fasta"
			if (len(open(path_fasta,'r').readlines())) > 25: #Sólo proceso del Meme las familias con más de un promotor
				# tomtom -oc tomtom_example_output_files -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc STRGGTCAN.meme JASPAR_CORE_2009.meme
				# tomtom -oc trial -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc motiflist.meme databaselist.meme
				# bashCom = bc + 'tomtom ' + " -oc " + path_tomtom + f + "/ -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc " + path + " " + path_db
				bashCom = 'meme-tomtom ' + " -oc " + path_tomtom + f + "/ -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc " + path + " " + path_db
				os.system(bashCom)
		except Exception as e:
			print("Error al analizar el tomtom por familias fasta")
			print(e[0])
			print(i[0])
	if con:
		conn.close()
		con.close()

'''
.______    __          ___      .__   __.   ______     ___      .______       _______ 
|   _  \  |  |        /   \     |  \ |  |  /      |   /   \     |   _  \     |   ____|
|  |_)  | |  |       /  ^  \    |   \|  | |  ,----'  /  ^  \    |  |_)  |    |  |__   
|   ___/  |  |      /  /_\  \   |  . `  | |  |      /  /_\  \   |      /     |   __|  
|  |      |  `----./  _____  \  |  |\   | |  `----./  _____  \  |  |\  \----.|  |____ 
| _|      |_______/__/     \__\ |__| \__|  \______/__/     \__\ | _| `._____||_______|
                                                                                      '''
def plant():
   print("PlantCare")


'''
.______    __  .______    _______  __       __  .__   __.  _______ 
|   _  \  |  | |   _  \  |   ____||  |     |  | |  \ |  | |   ____|
|  |_)  | |  | |  |_)  | |  |__   |  |     |  | |   \|  | |  |__   
|   ___/  |  | |   ___/  |   __|  |  |     |  | |  . `  | |   __|  
|  |      |  | |  |      |  |____ |  `----.|  | |  |\   | |  |____ 
| _|      |__| | _|      |_______||_______||__| |__| \__| |_______|
                                                                   '''
def pipe():
	print("Inicializando las Bases de datos")
	#inicializar()
	print("Cargar Bdd")
	up_bdd()
	print("Cargar")
	cargar_fam()
	print("Meme")
	meme()
	print("Tomtom")
	tomtom()
	print("¡Pipeline completo!")

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
	parametros()
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
			up_bdd()
		elif opcionMenu == "3":
			cargar_fam()
		elif opcionMenu == "4":
			meme()
		elif opcionMenu == "5":
			tomtom()
		elif opcionMenu == "6":
			plant()
		elif opcionMenu == "7":
			pipe()
		# Visualizar la Bdd
		elif opcionMenu == "4-":
			try: 
				con = lite.connect('prom.db')
				conn = con.cursor() # Objeto cursor para hacer cambios en la Bdd
			except:
				print("Error")
			conn.execute("SELECT nom FROM Prom WHERE adn is null ORDER BY random() LIMIT 30")
			i=conn.fetchone()
			print(i)
			
			dump_file = open('dump.txt', 'w')
			dump_file.close()
			conn.execute("SELECT count(nom) FROM Prom WHERE adn is null") 
			a=conn.fetchone()
			conn.execute("SELECT count(nom) FROM Prom WHERE adn is not null") 
			b=conn.fetchone()
			print("Con adn")
			print(b[0])
			print(a[0])
			print(round(b[0]/2497,2))
			conn.execute("SELECT * FROM Prom")# WHERE adn is not null")
			for i in conn:
				dump_file=open("dump.txt", 'a')
				#dump_file.write(i[0] + "\n")
				dump_file.write(i[3]+"\t"+i[0]+"\t"+i[1]+"\t"+i[2]+"\n"+i[4]+"\n")
				dump_file.close()
			if con:
				conn.close()
				con.close()
		else:
			print("Opcion incorrecta. Intente de nuevo.")
