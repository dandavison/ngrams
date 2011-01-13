
while ( <> ) {
    # print if /^[^0-9\$.#%\d!&<+?]+\t/;
    print if /^[A-Za-z][a-z']*\t/;
}
