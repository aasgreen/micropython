#!/bin/bash
if [ -z $1 ];
then
    echo "You need to specify a dir as argument."
    echo "Usage:"
    echo "$0 <dir>"
    exit 1
fi

while true;
do
    for a in $(ls -1 $1/* 2>/dev/null);
    do
    otherscript $a && rm $a #calls otherscript with the file a as argument and removes it if otherscript returned something non-zero
    done
    sleep 10s
    done
