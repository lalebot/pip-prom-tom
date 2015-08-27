#!/usr/local/perl

use strict;
use warnings;

use LWP::UserAgent;
use HTTP::Request;

my $filename = '/home/lale/pip-prom-tom/exa_prom.txt';
my $fileout = '/home/lale/pip-prom-tom/exa_prom_out.fasta';
my $ua = LWP::UserAgent->new;
my $url;
my $req;
my $response;
my $content;

$ua->agent("Mozilla/4.0 (compatible; MSIE 5.0; Windows 98; DigExt)");
open(my $fi, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
open(my $fo, ">$fileout") or die "No se puede abrir '$fileout' $!";

# Buscar a cada uno de los promotores de heinz de solgeniomics los motivos
# que estan en la lista y descargar la cadena generando un fasta

while (my $linea = <$fi>) {
	chomp $linea;
	$url = "http://solgenomics.net/search/quick?term=$linea&x=51&y=8";
	print "$url";
	$req = HTTP::Request->new(GET => $url);
	$response = $ua->request($req);
	#$content = $response->content();
	print $fo "$linea\n";
	#print $content;
	}

close $fi;
close $fo;