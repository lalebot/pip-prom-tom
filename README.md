# Pipeline Especialización en Bioinformática

## Requisitos:

+ Linux OS
+ Python3
+ Sqlite3
+ MEME & TOMTOM

## Todo:

+ Recordar que es un pipeline sencillo


- [x] ~~Elegir bdd~~
- [x] ~~Elegir archivo que contiene la lista de promotores.~~
- [ ] Quitar la separación por familia
- [ ] Ampliar la busqueda a varias bases de datos

- [x] Git
- [x] Python
- [ ] Solgenomics generic
- [ ] Bdd dinámica, crearla
- [x] Threads
- [x] Config
- [x] Meme  
- [x] TomTom
- [ ] Log
- [ ] Regular expresion
- [ ] Parametrización por linea de comando- https://docs.python.org/3/library/argparse.html - https://github.com/ucdavis-bioinformatics/alignerviz/blob/master/aviz.py
- [ ] -i input -o output

## Parametrización
+ Meme 
+ Tomtom

## Materiales
Hacerlo con threads que esperen http://www.genbetadev.com/python/multiprocesamiento-en-python-threads-a-fondo-introduccion

## Bitácora
+ Datos de inicio Excel a txt, utilizacion de sqlite como bdd,
+ Inicializar y crear la Bdd a partir del archivo
+ Abrir el sqlite y luego crear la bdd

```
$ sqlite3 test.db
$ .tables
$ .exit
```


+ Multiplies instancias, random, manejo de conexiones argupadas, sleep para esperar - mejora de 15 segundos a 2.5-3 segundos por archivo descargado. O sea de 10,5 horas a 2 horas promedio para a descarga de los 2500 cabeceras
+ Ejecucion local de MEME
+ Análisis TomTom
+ Agrega argumentos
+ se declaran las funciones
+ se va transformando en un pipeline
+ threading
+ Agregar la carga de la configuracion en un archivo plano .conf con variables editables y que ese archivo se valide al inicio.
+ Agregar el análisis PlantCare
+ Agregar archivo de configuracion
