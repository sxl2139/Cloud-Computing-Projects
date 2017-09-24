#!/usr/bin/python
import sys
args1 = sys.argv[1]
args2 = sys.argv[2]
count5 = 0
# input comes from STDIN (standard input)
for line in sys.stdin:
    #if(count5 == 5):
	#break
    #arg1 = sys.argv[1]
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split(",")
    # increase counters
    p = '0'+','+'1'
    key = 'Agecount'
    if(words[22] > args1):
	if(words[22] < args2):
        	p = '1'+','+'0'
		count5 = count5 + 1
		print '%s-%s' % (words[2], words[22])
    else:
 	p = '0'+','+'1'
	key = 'Others'
    print '%s#%s' % (key, p)
