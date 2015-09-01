#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;

use LWP::Simple;

my $filename = getcwd . '/exa_prom.txt';
my $fileout = getcwd . '/exa_prom_out.fasta';

print $filename;
print $fileout;

my $content;
my $content2;
my $fasta;
my @cod;
my @op;

# Abro el archivo de entrada.
open(my $fi, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
# Abro el archivo de salida para.
open(my $fo, ">>$fileout") or die "No se puede abrir '$fileout' $!";

# Recorro la lista de motivos.
while (my $linea = <$fi>) {
	# my $linea = 'Solyc10g079380';
	chomp $linea;
	# Realizo la búsqueda en la web.
	$content = get("http://solgenomics.net/search/quick?term=$linea&x=51&y=8") or die "Error al acceder a Solgenomics 1";
	while (my $linea_html = $content) {
		# Busco el código del resultado para poder navegar por los detalles.
		if(($linea_html =~ /feature/) && ($linea_html =~ /details/)){
			@cod = $linea_html =~ /[0-9]{8}/g;
		}
	}
	$content2 = get("http://solgenomics.net/feature/$cod[0]/details") or die "Error al acceder a Solgenomics 2";
	while (my $linea_html2 = $content2) {
		# Selecciono los "1000 pares de bases upstream"
		if($linea_html2 =~ /1000 bp upstream/){
			# Obtengo 3 número de 8 cifras que corresponden al lugar en donde está el motivo
			@op = $linea_html2 =~ /[0-9]{8}/g;
		}
	}
	# Obtengo un archivo fasta.
	$fasta = get("http://solgenomics.net/api/v1/sequence/download/multi?format=fasta&s=$op[0]:$op[1]..$op[3]") or die "Error al acceder a Solgenomics 3";
	# Guardo los resultados en el archivo de salida.
	print $fo "$fasta\n";
}

close $fi;
close $fo;