# Trabajo práctico en Perl

El siguiente script en *Perl* realiza una búsqueda de motivos a partir de una lista de promotores **exa_prom.txt**.

Para ello se conecta a **www.solgenomics.com** y va iterando cada código de promotor y almacenando los motivos de los mismos en **exa_prom_out.fasta**.


```perl
#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use LWP::Simple;

# Uso path relativo
my $filename = getcwd . '/exa_prom.txt';
my $fileout = getcwd . '/exa_prom_out.fasta';

my $content;
my $content2;
my $fasta;
my @cod;
my @op;

# Abro el archivo de entrada.
open(my $fi, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
# Abro el archivo de salida para.
open(my $fo, ">$fileout") or die "No se puede abrir '$fileout' $!";

# Recorro la lista de motivos.
while (my $linea = <$fi>) {
    # my $linea = 'Solyc10g079380';
    chomp $linea;
    print "Bajando: $linea\n";
    # Realizo la búsqueda en la web.
    $content = get("http://solgenomics.net/search/quick?term=$linea&x=51&y=8") or die print "Error al acceder a Solgenomics 1";
    # Busco el código del resultado para poder navegar por los detalles.
    @cod = $content =~ m{/feature/([0-9]{8})/details}g;
    $content2 = get("http://solgenomics.net/feature/$cod[0]/details") or die print "Error al acceder a Solgenomics 2";
    # Selecciono los "1000 pares de bases upstream"
    @op = $content2 =~ m{([0-9]{8}:[0-9]{8}..[0-9]{8})">1000 bp upstream}g;
    # Obtengo un archivo fasta.
    $fasta = get("http://solgenomics.net/api/v1/sequence/download/multi?format=fasta&s=$op[0]") or die print "Error al acceder a Solgenomics 3";
    # Guardo los resultados en el archivo de salida.
    print $fo "$fasta";
}

close $fi;
close $fo;
```