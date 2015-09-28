# Pipeline Especialización en Bioinformática

## Todo:
+ Recordar que es un pipeline sencillo
- [x] ~~Elegir bdd~~
- [x] Elegir archivo que contiene la lista de promotores.
- [x] Quitar la separación por familia
- [x] Git
- [x] Python
- [x] Threads
- [x] Config
- [x] Meme  
- [x] TomTom
- [ ] Log
- [x] Regular expresion
- [x] Parametrización por linea de comando- https://docs.python.org/3/library/argparse.html - https://github.com/ucdavis-bioinformatics/alignerviz/blob/master/aviz.py
- [x] -i input -o output
- [ ] ~~Bdd dinámica, crearla~~
- [ ] ~~Ampliar la busqueda a varias bases de datos~~
- [x] Crear DB SQL desde el código
- [x] ver de analizar los archivos y parametrizar el tom tom y meme
- [x] Mejorar la interfaz y los mensajes que se muestran
- [x] Chequear parámetros
- [x] Parametrización Meme y Tomtom
- [x] Modificar bp 1000up, ~~por parámetros~~ y por parseo
- [ ] Testeo de lo anterior!!!
- [ ] PlantCare, separados, exportandolo a txt
- [ ] Sentido de la hebra + o negativa, más el complemento inverso.
- [ ] 


## Materiales
Hacerlo con threads que esperen http://www.genbetadev.com/python/multiprocesamiento-en-python-threads-a-fondo-introduccion

## Bitácora
+ Datos de inicio Excel a txt
+ utilizacion de sqlite como bdd,
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
+ Elimada la opción de separar por familias
+ Agregar archivo de configuracion
+ Agrego libreria *re* de regular expresions
+ Visor SQL: sqlitebrowser
+ Descargar la última bdd de motivos de MEME utilizando wget y descomprimirla usando tar
+ Se crea una carpeta con el nombre del proyecto en donde se guarda todo el contenido de la salida
+ Agrega la verificación del archivo conf.ini
+ Pasar por parámetro el upstream y el downstream
+ Agregar el gap para ampliar la bùsqueda
