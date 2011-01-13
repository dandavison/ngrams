
%counts = {};
while( <> ) {
    ($ngram, $year, $count) =  split '\t';
    $counts{$year} += $count;
}
while( ($key, $val) = each %counts ) {
    print "$key\t$val\n" if $val;
}
