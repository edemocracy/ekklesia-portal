#!/usr/bin/env sh
for x in *.jade; do
    echo pyjade-compiling $x
    pyjade $x > ${x:0:-5}.html
done
