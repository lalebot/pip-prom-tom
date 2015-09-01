#!/usr/local/perl

use strict;
use warnings;

use LWP::Simple;
use HTTP::Request;

my $filename = '/home/lale/pip-prom-tom/exa_prom.txt';
my $fileout = '/home/lale/pip-prom-tom/exa_prom_out.fasta';
my $filehtml = '/home/lale/pip-prom-tom/exa_html.txt';

my $content;
my $content2;
my $fasta;
my @cod;
my @op;

open(my $fi, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
#open(my $fh, '<:encoding(UTF-8)', $filehtml) or die "Could not open file '$filehtml' $!";
open(my $fo, ">$fileout") or die "No se puede abrir '$fileout' $!";

# Buscar a cada uno de los promotores de heinz de solgeniomics los motivos 1000 upstream
# que estan en la lista y descargar la cadena generando un fasta

while (my $linea = <$fi>) {
	chomp $linea;
	$content = get("http://solgenomics.net/search/quick?term=$linea&x=51&y=8");
	# $content = $fh;
	while (my $linea_html = $content) {
		if(($linea_html =~ /feature/) && ($linea_html =~ /details/)){
			@cod = $linea_html =~ /[0-9]{8}/g;
		}
	$content2 = get("http://solgenomics.net/feature/$cod[0]/details");
	while (my $linea_html2 = $content2) {
		if($linea_html2 =~ /1000 bp upstream/){
			@op = $linea_html =~ /[0-9]{8}/g;
		}
	}
	$fasta = get("http://solgenomics.net/api/v1/sequence/download/multi?format=fasta&s=$op[0]:$op[1]..$op[3]");
	print $fo $fasta;
	#<option value="19629078:63343955..63342956">1000 bp upstream</option>
}

close $fi;
close $fo;