#!/usr/bin/perl
$i=-1;
while($_=<>)
{
    if($_ =~ /Begin/) {
	$i++;
	open OUT, '>', "dhdata$i";
    }
    else {
	$_ =~ s/^(\d\d)/-\1./;
	$_ =~ s/\t(\d\d)/\t\1./;
	print OUT $_;
    }
}
