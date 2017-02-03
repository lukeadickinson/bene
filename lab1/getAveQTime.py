from __future__ import print_function
import sys
sys.path.append('..')
import random

def parseFile(loadPercent):
	with open('./experiment'+ str(loadPercent)+'.txt') as f:
		content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	totalValue = 0
	totalCount = 0
	for line in content:
		totalValue += float(line)
		totalCount += 1

	print(str(loadPercent) + " " + str(totalValue / totalCount))
	
parseFile(10)
parseFile(20)
parseFile(30)
parseFile(40)
parseFile(50)
parseFile(60)
parseFile(70)
parseFile(80)
parseFile(90)
parseFile(95)
parseFile(98)
