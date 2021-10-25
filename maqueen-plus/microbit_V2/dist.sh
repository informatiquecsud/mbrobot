#!/bin/bash

for file in `cd src && ls *.py && cd ..`; do pyminifier.exe -o dist/$file src/$file; done
# for file in `cd src && ls *.py && cd ..`; do echo `$file; done

