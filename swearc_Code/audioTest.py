#!env python

import pprint,os
from datetime import datetime

t = datetime.now().strftime("%k %M")
h = datetime.now().strftime("%k")

'''
command = "espeak 'Hello this is a test test test test testin one two three one ' 2>/dev/null > /dev/null" 
os.system(command)
last = 0

'''
#'''
command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Hello I am Moose, Please follow me' 2>/dev/null > /dev/null"
os.system(command)
last = 0
#'''

#'''
command = "espeak -ven-us -a 200 -p 30 -g 12 'Hello I am an autonomous Robot moose' 2>/dev/null > /dev/null"
os.system(command)
last = 0



command = "espeak -ven -a 200 -p 30 -g 12 'Bye bye I am heading back to the forest to find myself. It was nice meeting you. Please come and visit me or send me a post card.' 2>/dev/null > /dev/null"
os.system(command)
last = 0
#'''
