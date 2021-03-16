#!/bin/bash

RESULT=""

if [ -z "$1" ] 
	then
		RESULT=`python3 src/Main.py MAD LCV NOR`
	else
		RESULT=`python3 src/Main.py MAD LCV NOR $1`
fi

echo "$RESULT"
