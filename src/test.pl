
%h = {};
$h{'a'} = 1;
while( ($key, $val) = each %h ) {
    print "$key -> $val\n";
}
