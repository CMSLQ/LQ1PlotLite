#!/usr/bin/env python

import subprocess as sp
import os

command = "ps aux | grep gdb | egrep -v 'grep|kill_gdb'"
output = sp.Popen (command, shell=True, stdout=sp.PIPE).communicate()[0].split("\n")

for line in output:
    if not line: continue
    command = "kill -9 " + line.split()[1]
    print command
    os.system ( command ) 
    
