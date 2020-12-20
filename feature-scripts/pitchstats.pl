#!/usr/bin/perl

use strict;
use warnings;
use Statistics::Lite qw(:all);

# read STDIN and report some statistics on the numbers expected in every line
# switches: -1 -- ignore lines that contain -1 (which is often used as no-pitch-marker

my $ignoreMinus1Lines = $#ARGV == 0;
print "ignoring lines containing -1\n" if($ignoreMinus1Lines);
my @hzentries;
my @cententries;
while (my $line = <STDIN>) {
	chomp $line; chomp $line;
	$line =~ s/\s//g;
	unless (0+$line == -1 && $ignoreMinus1Lines) {
		push @hzentries, $line;
		push @cententries, 1731.2340490667560888319096172*log($line/110.0);
	}
}
printStats(@hzentries);
#printStats(@cententries);

sub printStats {
	my @entries = @_;
	print statsinfo(@entries);
	@entries = sort {$a <=> $b} @entries;
	my $length = $#entries + 1;
	print "quartiles: ", $entries[$length*25/100], "\t", $entries[$length*75/100], "\n";
#	print STDERR $entries[$length*75/100]-$entries[$length*25/100], "\t";
	print "5/95quant: ", $entries[$length* 5/100], "\t", $entries[$length*95/100], "\n";
#	print STDERR $entries[$length*95/100]-$entries[$length* 5/100], "\n";
}
