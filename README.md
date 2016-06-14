# Pipeline de Promotores de Tomate

Script para extraer secuencia de promotores de la especie Solanum lycopersicum from the web Solgenomics, para luego ser analizados con MEME y TOMTOM.

![Tomate](http://www.poesi.as/cuadros/tomate.jpg "Tomate")

# Requisitos

#### Software base para la ejecución del script

+ Linux OS
    + python3
    + sqlite3
    + wget
    + tar
    + git


Instalación en Debian y derivados:

```bash
$ sudo apt-get install git python3 sqlite3 wget tar
```

Instalación en ArchLinux y derivados:

```bash
$ yaourt -S git python3 sqlite3 wget
```


#### Programas de análisis

Requisitos **MEME & TOMTOM**

+ MEME
    * ghostscript
    * imagemagick
    * python2
    * perl
    * tcsh
    * openmpi


Documentación: http://meme-suite.org/doc/install.html


Instalación en Debian y derivados:

```bash
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python2.6 python2.6-dev
```

```bash
$ sudo apt-get install ghostscript imagemagick openmpi-bin tcsh perl libexpat1-dev zlib1g-dev autoconf automake libtool libxml2  libxml-parser-perl
```


Instalación en ArchLinux y derivados:

```bash
$ yaourt -S python2 perl ghostscript imagemagick python2 perl-xml-parser perl-html-template openmpi tcsh autoconf automake libtool libxml2  libxslt
```


Descargar: http://meme-suite.org/doc/download.html?man_type=web

Instalación:
```bash
$ tar zxf meme_4.10.2.tar.gz
$ cd meme_4.10.2
$ ./configure --prefix=$HOME/meme --with-url=http://meme-suite.org --enable-build-libxml2 --enable-build-libxslt
$ make
$ make test
$ make install
```

Then, edit your shell configuration file to add $HOME/meme/bin to your shell path. This can often be done by editing the file named *.profile* to add the following line:

**export PATH=$HOME/meme/bin:$PATH**


# Descarga y ejecución del script

```bash
$ git clone http://github.com/lalebot/pip-prom-tom.git
$ cd pip-prom-tom
$ python3 pip_prom_tom.py -i list_prom.txt -o proyecto1 -u 1000 -g 250
```

Donde:
+ **-i** es el archivo de entrada.
+ *list_prom.txt* es el nombre del archivo que contiene la lista de promotores y se encuentra en el mismo directorio que el script.
+ **-o** es la salida.
+ *proyecto1* es el nombre de salida del proyecto.
+ **-u** es la cantidad de pares de bases *upstream* que queremos descargar.
+ **-g** es el gap.

Para descargar los pares de base *downstream* usamos el parámetro **-d**.

Obtener *ayuda* de los parámetros admitidos por líneas de comando ejecutar:
```bash
$ python3 pip_prom_tom.py -h
```

Para ejecutar el script en modo pipeline agregar **-p 1**
```bash
$ python3 pip_prom_tom.py -i list_prom.txt -o proyecto1 -u 1000 -g 250 -p 1
```

Los resultados se almacena en una sub-carpeta que tiene el *nombre-del-proyecto_out*.


# Contenido de los archivos

### README.md
Es este archivo.

### conf.ini
Contiene el archivo de configuración parametrizable.

```bash
# Archivo de configuración inicial

# Pipeline on/off por defecto
pipeline = false

# Número de threads que se lanzan
threads = 20

# Path del MEME
meme-path = /usr/bin/meme-meme
# Parámetros de MEME. Default = -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc
meme-param = -dna -mod oops -w 8 -minw 8 -maxw 12 -maxsize 1000000000 -oc

# Path del TOMTOM
tomtom-path = /usr/bin/meme-tomtom
# Parámetros de TOMTOM. Default = -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc
tomtom-param = -min-overlap 5 -dist pearson -evalue -thresh 10 -no-ssc
```


### exa_prom.txt
Contiene una lista de códigos de promotores de ejemplo.


### pip_prom_tom.py
Contiene el código del script.

---
<img src="https://theapproachdotorg.files.wordpress.com/2012/05/killer-tomato.jpg" align="left" width="200">
