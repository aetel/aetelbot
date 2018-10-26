#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

with open(sys.argv[1], 'r') as my_file:
   lines = my_file.read()

my_list = lines.splitlines()
print list 

import subprocess

addresses = subprocess.check_output(['arp', '-a'])

print addresses

networkAdds = addresses.splitlines()[1:]
networkAdds = set(add.split(None,2)[1] for add in networkAdds if add.strip())
with open(sys.argv[1]) as infile: knownAdds = set(line.strip() for line in infile)

print networkAdds
print knownAdds

print("These addresses were in the file, but not on the network")
for add in knownAdds - networkAdds:
    print(add)

