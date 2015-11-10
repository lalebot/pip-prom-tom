# Pipeline Especialización en Bioinformática

+ Pipeline sencillo

## Todo:

- [x] ~~Elegir bdd~~
- [x] Elegir archivo que contiene la lista de promotores.
- [x] Quitar la separación por familia
- [x] **Git**
- [x] GitHub
- [x] Python
- [x] **Threads**
- [x] **Config**
- [x] Meme  
- [x] TomTom
- [x] Log
- [x] Regular expresion
- [x] **Parametrización por linea de comando**
- [x] -i input -o output
- [ ] ~~Bdd dinámica, crearla~~
- [ ] ~~Ampliar la busqueda a varias bases de datos~~
- [x] Crear DB SQL desde el código
- [x] ver de analizar los archivos y parametrizar el tom tom y meme
- [x] Mejorar la interfaz y los mensajes que se muestran
- [x] Chequear parámetros
- [x] Parametrización Meme y Tomtom
- [x] Modificar bp 1000up, ~~por parámetros~~ y por parseo
- [ ] PlantCare, separados, exportandolo a txt
- [ ] Sentido de la hebra + o negativa, más el complemento inverso.
- [ ] ~~Sentido de la hebra + o negativa, más el complemento inverso.~~
- [x] Verificar que los parámetros obligatorios se pasen, en caso de no hacerlo informar error
- [ ] Verificacion del archivo con cabeceras del solgenomics
- [x] Ver el tema de las licencias GPL software libre
- [ ] Traducir el archivo Leeme.md 

- [ ] Testeo beta

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

+ Multiplies instancias, random, manejo de conexiones agrupadas, sleep para esperar - mejora de 15 segundos a 2.5-3 segundos por archivo descargado. O sea de 10,5 horas a 2 horas promedio para a descarga de los 2500 cabeceras.
+ Ejecucion local de MEME
+ Análisis TomTom
+ Agrega argumentos
+ se declaran las funciones
+ threading
+ Se utiliza la combinación de Bdd (Sqlite3) y Threads para que los hilos trabajen paralelamente y puedan acceder de manera conjunta a la misma base de datos actualizándola hasta estar completa. Además ante cualquier corte del proceso de carga se puede retomar facilmente.
+ Agregar la carga de la configuracion en un archivo plano .conf con variables editables y que ese archivo se valide al inicio.
+ Elimada la opción de separar por familias
+ Agregar archivo de configuracion
+ Agrego libreria *re* de regular expresions
+ Visor SQL: sqlitebrowser
+ Descargar la última bdd de motivos de MEME utilizando wget y descomprimirla usando tar
+ Se crea una carpeta con el nombre del proyecto en donde se guarda todo el contenido de la salida
+ Agrega la verificación del archivo conf.ini
+ Pasar por parámetro el upstream y el downstream
+ Agregar el gap para ampliar la búsqueda
+ testeo de plantcare, pero no implementación
+ Agrego los logs
