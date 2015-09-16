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
+ MEME & TOMTOM


## Descarga e instalación del script

```bash
$ git clone https://github.com/lalebot/pip-prom-tom.git
$ cd pip-prom-tom
$ python pip-prom-tom.py3 -i list_prom.txt -o proy_out
```

Obtener ayuda de las opciones agregar **-h**
```bash
$ python pip-prom-tom.py3 -h
```

Para ejecutar el script en modo pipeline agregar **-p 1**
```bash
$ python pip-prom-tom.py3 -i list_prom.txt -o proy_out -p 1
```

## Uso
ejemplos


## Contenido de los archivos

#### README.md
Este archivo.

#### conf.ini
Archivo de configuración parametrizable.

#### exa_prom.txt
Lista de códigos de promotores de ejemplo.

#### pip-prom-tom.py3
Código del script.


#### ¡Tomates!
![Tomate](https://theapproachdotorg.files.wordpress.com/2012/05/killer-tomato.jpg "Tomate")