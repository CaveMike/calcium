#!/usr/bin/python
import random
import sys

if __name__ == '__main__':
   previous = -1
   streak = 0
   topstreak = 0

   for i in range(200):
        r = random.randrange(2)
        #print r
        if r == previous:
            streak += 1

            if streak > topstreak:
               topstreak = streak
        else:
            #if streak > 1:
            #    print 'streak', streak, 'previous', previous

            streak = 0
            previous = r

   print 'topstreak', topstreak

