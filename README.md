# Pipeline de Promotores de Tomate

Script para extraer secuencia de promotores de la especie Solanum lycopersicum desde la web Solgenomics, para luego ser analizados con MEME y TOMTOM.

![Tomate](http://www.ghesaf.ro/wp-content/uploads/2011/09/tomate-heinz-1370.jpg "Tomate")

## Requisitos

#### Programas base
+ Linux OS
    + python3
    + sqlite3
    + wget
    + tar
    + git
    + biopython
+ MEME
    * ghostscript
    * imagemagick

Instalación en Debian y derivados.
```bash
$ sudo apt-get install python3 sqlite3 wget tar git ghostscript imagemagick
```
Para instalar Biopython descargar: https://github.com/biopython/biopython/archive/master.zip

To build and install Biopython, download and unzip the source code, go to this directory at the command line, and type:
```bash
$ python setup.py build
$ python setup.py test
$ sudo python setup.py install
```

Instalación en ArchLinux.
```bash
$ sudo pacman -S python3 python-biopython sqlite3 wget tar git ghostscript imagemagick
```

#### Programas de análisis

**MEME & TOMTOM**

Descargar: http://meme-suite.org/doc/download.html?man_type=web

Instalación:
```bash
$ tar zxf meme_4.10.1.tar.gz
$ cd meme_4.10.1
$ ./configure --prefix=$HOME/meme --with-url=http://meme-suite.org --enable-build-libxml2 --enable-build-libxslt
$ make
$ make test
$ make install
```

Then, edit your shell configuration file to add $HOME/meme/bin to your shell path. This can often be done by editing the file named .profile to add the following line: 
**export PATH=$HOME/meme/bin:$PATH**


## Descarga e instalación del script

```bash
$ git clone http://github.com/lalebot/pip-prom-tom.git
$ cd pip-prom-tom
$ python3 pip-prom-tom.py3 -i list_prom.txt -o proyecto1
```

Donde **list_prom.txt** es el nombre del archivo que contiene la lista de promotores y **proyecto1** es el nombre del proyecto de análisis.

Obtener *ayuda* de las opciones agregar **-h**
```bash
$ python pip-prom-tom.py3 -h
```

Para ejecutar el script en modo pipeline agregar **-p 1**
```bash
$ python pip-prom-tom.py3 -i list_prom.txt -o proyecto1 -p 1
```

Para elegir el tamaño de pb upstream agregar **-u** o downstream **-d** . Se puede pasar por parámetros el valor de un gap para extraer parte del motivo que codifica con **-g**
```bash
$ python pip-prom-tom.py3 -i list_prom.txt -o proyecto1 -u 1000 -g 250
```

El resultado se almacena en una carpeta que tiene el *nombre-del-proyecto_out*


## Contenido de los archivos

#### README.md
Es este archivo.

#### conf.ini
Contiene el archivo de configuración parametrizable.

```bash
# Archivo de configuración inicial

# Pipeline on/off por defecto
pipeline = false

# Número de threads que se lanzan
threads = 40

# Path del MEME
meme-path = /usr/bin/meme-meme
# Parámetros de MEME. Default = -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc
meme-param = -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc

# Path del TOMTOM
tomtom-path = /usr/bin/meme-tomtom
# Parámetros de TOMTOM. Default = -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc
tomtom-param = -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc
```


#### exa_prom.txt
Contiene una lista de códigos de promotores de ejemplo.


#### pip-prom-tom.py3
Contiene el código del script.

---
<img src="https://theapproachdotorg.files.wordpress.com/2012/05/killer-tomato.jpg" align="left" width="200">
