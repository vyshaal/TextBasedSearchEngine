import regex as re
import os
import sys
import glob

def create_index():
	hand = open("cacm_stem.txt")

	for line in hand:
		line = line.rstrip()
		if re.match(r'# [\d]+', line):

			digit = line.rsplit(" ",1)[1]
			if len(digit) < 4:
				for i in range(4-len(digit)):
					digit = '0' + digit


			document_name = "CACM-" + digit + ".html"
			print(document_name)

			newfile = open(os.path.join("cacm",document_name), "a")
		else:
			words = line.split(" ")
			for word in words:
				newfile.write(word + "\n")


if __name__ == "__main__":
	create_index()