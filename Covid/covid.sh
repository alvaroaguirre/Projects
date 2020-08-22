#!/bin/bash

python ./covid.py

cd .. 

git add Covid

git commit -m 'Daily change'

git push origin master