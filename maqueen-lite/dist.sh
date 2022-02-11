#!/bin/bash

for file in `cat dist.txt`; do pyminifier.exe -o dist/$file src/$file; done
# for file in `cd src && ls *.py && cd ..`; do echo `$file; done

