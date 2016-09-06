#!/usr/bin/env zsh
cd jade
for x in [^_]*.jade; do
    fn=../${x:0:-5}.html
    echo pyjade-compiling $x to $fn
    pyjade $x > $fn
done
cd ..
