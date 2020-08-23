#!/bin/bash

cd /Users/alvaroaguirre/Documents/Projects/Covid

/Users/alvaroaguirre/opt/anaconda3/bin/python ./covid.py

cd .. 

git add Covid

git commit -m 'Daily change'

git push origin master