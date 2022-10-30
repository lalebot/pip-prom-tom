# Pipeline architecture for the extraction of Solanum lycopersicum promoters

Script to extract the sequence of promoters of the species Solanum lycopersicum from the web Solgenomics, to later be analyzed with MEME and TOMTOM. 

![Tomate](http://www.poesi.as/cuadros/tomate.jpg "Tomate")

## Demo Video

[![demo](https://github.com/lalebot/pip-prom-tom/blob/master/demo.png)](https://youtu.be/QA1AEsjHLgU "Demo")


## Requirements

#### Base software for script execution

+ Linux OS
    + python3
    + sqlite3
    + wget
    + tar
    + git


Installation on Debian, Ubuntu and derivatives:

```bash
$ sudo apt-get install git python3 sqlite3 wget tar
```

Installation on ArchLinux and derivatives:

```bash
$ yaourt -S git python3 sqlite3 wget
```

#### Analysis programs

*MEME & TOMTOM**

+ MEME
    * ghostscript
    * imagemagick
    * python2
    * perl
    * tcsh
    * openmpi


Documentation: http://meme-suite.org/doc/install.html


Installation on Debian, Ubuntu and derivatives:

```bash
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python2.6 python2.6-dev
```

```bash
$ sudo apt-get install ghostscript imagemagick openmpi-bin tcsh perl libexpat1-dev zlib1g-dev autoconf automake libtool libxml2  libxml-parser-perl
```


Installation on ArchLinux and derivatives:

```bash
$ yaourt -S python2 perl ghostscript imagemagick python2 perl-xml-parser perl-html-template openmpi tcsh autoconf automake libtool libxml2  libxslt
```


Download: http://meme-suite.org/doc/download.html

Installation:
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


# Download and run the script

```bash
$ git clone http://github.com/lalebot/pip-prom-tom.git
$ cd pip-prom-tom
$ python3 pip_prom_tom.py -i exa_prom.txt -o proyecto1 -u 1000 -g 250
```

Help:
+ ** - i ** is the input file.
+ * list_prom.txt * is the name of the file that contains the list of promoters and is located in the same directory as the script.
+ ** - or ** is the output.
+ * projecto1 * is the output name of the project.
+ ** - u ** is the number of base pairs * upstream * we want to download.
+ ** - g ** is the gap.

To download the base pairs * downstream * we use the parameter ** - d **.

Get * help * of the parameters supported by command lines run: 
```bash
$ python3 pip_prom_tom.py -h
```

To run the script in pipeline mode add **-p 1**
```bash
$ python3 pip_prom_tom.py -i list_prom.txt -o proyecto1 -u 1000 -g 250 -p 1
```

The results are stored in a sub-folder that has the  *nombre-del-proyecto_out*.


# File content

### conf.ini

Contains the parameterizable configuration file.

### exa_prom.txt
Contiene una lista de códigos de promotores de ejemplo.


### pip_prom_tom.py
The code

---
