
$OUTDIR = 'eng-all-split-clean';
while( <> ) {
    ($ngram) = split '\t';
    next unless $ngram =~ /^[A-Za-z][a-z']*$/;
    if($ngram ne $ngram_old) {
        $dir = substr($ngram, 0, 2);
        close FILE if $ngram_old;
        mkdir "$OUTDIR/$dir";
        open FILE, ">$OUTDIR/$dir/$ngram";
        $ngram_old = $ngram;
    }
    print FILE;
}
