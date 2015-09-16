# Pipeline de Promotores de Tomate

Script para extraer secuencia de promotores de la especie xxx desde la web Solgenomics, para luego ser analizados con MEME y TOMTOM.

![Tomate](http://www.ghesaf.ro/wp-content/uploads/2011/09/tomate-heinz-1370.jpg "Tomate")

## Requisitos

#### Programas base
+ Linux OS
    + python3
    + sqlite3
    + wget
    + tar
    + git

Instalación
```bash
$ sudo apt-get install python3 sqlite3 wget tar git
```


#### Programas de análisis
MEME & TOMTOM

Descargar la última versión desde http://meme-suite.org/doc/download.html?man_type=web


## Descarga e instalación del script

```bash
$ git clone http://github.com/lalebot/pip-prom-tom.git
$ cd pip-prom-tom
$ python pip-prom-tom.py3 -i list_prom.txt -o proyecto1
```

Donde **list_prom.txt** es el nombre del archivo que contiene la lista de promotores y **proyecto1** es el nombre del proyecto de análisis.

Obtener ayuda de las opciones agregar **-h**
```bash
$ python pip-prom-tom.py3 -h
```

Para ejecutar el script en modo pipeline agregar **-p 1**
```bash
$ python pip-prom-tom.py3 -i list_prom.txt -o proyecto1 -p 1
```

El resultado se almacena en una carpeta que tiene el *nombre-del-proyecto_out*.


## Contenido de los archivos

#### README.md
Es este archivo.

#### conf.ini
Contiene el archivo de configuración parametrizable.

```bash
# Config

# Pipeline on/off
pipeline = false

# Number of threads
threads = 20

# Path MEME
meme-path = /usr/bin/meme-meme

# Path TOMTOM
tomtom-path = /usr/bin/meme-tomtom
```


#### exa_prom.txt
Contiene una lista de códigos de promotores de ejemplo.


#### pip-prom-tom.py3
Contiene el código del script.

---
<img src="https://theapproachdotorg.files.wordpress.com/2012/05/killer-tomato.jpg" align="left" width="200">