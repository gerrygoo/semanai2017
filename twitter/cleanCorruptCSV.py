# cleanCorruptCSV.py

import csv

# csvfile = open('finalDictionary.csv', 'r').read()
# # fieldnames = ['word', 'value']
# reader = csv.DictReader(csvfile)

# for element in reader:
# 	print("element = " + str(element))

# csvfile2.close()

wholeString = open('finalDictionary.csv', 'r').read()
# print(wholeString)
wholeString = wholeString.replace(':', ',')
wholeString = wholeString.replace('\'', '')
print(wholeString)