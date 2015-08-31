#!/usr/local/perl

#use strict;
#use warnings;

use LWP::Simple;
use HTTP::Request;

my $filename = '/home/lale/pip-prom-tom/exa_prom.txt';
my $fileout = '/home/lale/pip-prom-tom/exa_prom_out.fasta';
my $filehtml = '/home/lale/pip-prom-tom/exa_html.txt';

my $content;
my @tmpstr;
my @cod;

open(my $fi, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
open(my $fh, '<:encoding(UTF-8)', $filehtml) or die "Could not open file '$filehtml' $!";
open(my $fo, ">$fileout") or die "No se puede abrir '$fileout' $!";

# Buscar a cada uno de los promotores de heinz de solgeniomics los motivos 1000 upstream
# que estan en la lista y descargar la cadena generando un fasta

while (my $linea = <$fi>) {
	chomp $linea;
	$content = get("http://solgenomics.net/search/quick?term=$linea&x=51&y=8");
	while (my $linea = $content) {
		if(($linea =~ /feature/) && ($linea =~ /details/)){
			@cod = $linea =~ /[0-9]{8}/g;
			print for $cod[0];
		}
#	print ">test\n$tmpstr[1]\n";
	}

close $fi;
close $fo;