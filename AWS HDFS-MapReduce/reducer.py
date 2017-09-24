#!/usr/bin/python
import sys

cred_word = None
#status_word = None
no_count = 0
yes_count = 0
#cred_count = 0
a = None
b = None
value =None
count = 0

for line in sys.stdin:
    if(count == 5):
	break

    line = line.strip()
    value, count = line.split('#')
    name, age = line.split('-')
    a, b = count.split(',')

    if(len(name) > 0):
	print '%s,%s' % (name, age)

    try:
        a = int(a)
        b = int(b)
    except ValueError:
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if cred_word == value:
        yes_count += a
        no_count += b

    else:
        if cred_word:
		#if cred_word == 'Agecount':
                count += 1
		print '%s,%s' % (cred_word, yes_count)

        cred_word = value
        #cred_count=1

# do not forget to output the last word if needed!
if cred_word == value:
	#if cred_word == 'Agecount':
	print '%s,%s' % (cred_word, 5)
