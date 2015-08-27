#!/usr/local/perl

use strict;
use warnings;

use LWP::Simple;
use HTTP::Request;

my $filename = '/home/lale/pip-prom-tom/exa_prom.txt';
my $fileout = '/home/lale/pip-prom-tom/exa_prom_out.fasta';

my $content;
my @tmpstr;

open(my $fi, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
open(my $fo, ">$fileout") or die "No se puede abrir '$fileout' $!";

# Buscar a cada uno de los promotores de heinz de solgeniomics los motivos 1000 upstream
# que estan en la lista y descargar la cadena generando un fasta


#while (my $linea = <$fi>) {
	my $linea = "Solyc10g083560";
	chomp $linea;
	$content = get("http://solgenomics.net/search/quick?term=$linea&x=51&y=8");
	print $linea;
	@tmpstr = (split '<li><a class="xref xref_link xref_link_featurepages" href="/feature/">', $content);
	#print $_, "\n" for split ' ', 'file1.gz file1.gz file3.gz';
	print $fo "@tmpstr[1]\n";
#	}

close $fi;
close $fo;