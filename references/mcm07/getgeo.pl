#!/usr/bin/perl
$_=<>;
while($_=<>) {
  $type = substr($_,8,3);
  if($type eq "080") {
    $pop=substr($_,292,9);
    $lat=substr($_,311,8);
    $lon=substr($_,320,9);
    $are=substr($_,172,13);
    $are=0 if($are==0);
    $nam=substr($_,200,90);
    $tot+=$pop;
    print "$pop $lat $lon $are\n";
  }
}
print "$tot\n";
