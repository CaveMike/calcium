#!/usr/bin/env python
from optparse import OptionParser
from UserString import MutableString
import math
import random
import os
import sys

class Results:
	def __init__( self ):
		self.data = {}

	def accum( self, value ):
		self.data[value] = self.data.setdefault( value, 0 ) + 1

	def __str__( self ):
		l = sum( [ v for v in self.data.values() ] )
		if not l:
			return 'No results'

		s = MutableString()

		y = float(1) / len(self.data)

		s += 'size: '
		s += str(len(self.data))
		s += '\n'

		s += 'num results: '
		s += str(l)
		s += '\n'

		for key in self.data:
			x = float(self.data[key]) / l

			s += str(key)
			s += ': '

			s += 'hits: '
			s += str(self.data[key])
			s += ', '

			s += 'h/t: '
			s += str(x)
			s += ', '

			s += 'dev: '
			s += str(y - x)
			s += '\n'

		return str(s)

class SourceRand:
	def __init__( self, size, num ):
		self.size = size
		self.num = num

	def get( self ):
		while True:
			yield random.randint( 0, self.size - 1 )

def testSourceRand( size, num ):
	get = SourceRand( size, 1 ).get().next

	results = Results()
	for i in range(num):
		v = get()
		results.accum(v)

	print str(results)

class SourceEach:
	def __init__( self, size, num ):
		self.size = size
		self.num = num

	def get( self ):
		while True:
			t = self.size**self.num
			for i in range(0, t):
				for j in range(self.num):
					yield i / (self.size**(j)) % self.size

def testSourceEach( size, num ):
	get = SourceEach( size, num ).get().next

	results = Results()
	for i in range(size**num):
		#print i, ':',
		for j in range(0, num):
			v = get()
			results.accum(v)
			#print v,
		#print
	print str(results)

class Randformer:
	def __init__( self, source, destination ):
		self.source = source
		self.destination = destination
		self.numDice = 0
		self.MAX_DICE = self.destination
		self.threshold = 0
		self.ratio = 0

		self.get = None

	# destination * d / source ^ s >= ratio
	def calcThreshold( self, ratio ):
		for s in range(1, self.MAX_DICE):
			y = self.source**s
			for d in range( y / self.destination, 0, -1):
				x = self.destination * d
				r = float(x) / y
				#print 'calc', s, d, x, y, r
				if r >= ratio and r <= 1:
					self.numDice = s
					self.threshold = x
					self.ratio = r
					return

		raise Exception( 'Failed to find an algorithm for converting from ' + str(self.source) + ' to ' + str(self.destination) + '.' )

	# r = x
	# r = s(y-1) + x
	# r = s^2(z-1) + s(y-1) + x
	def randDestination( self ):
		while True:
			x = self.get()
			for s in range(1, self.numDice):
				y = self.source**s * ( self.get() )
				#print 'i:', s, 'x:', x, 'y:', y, 'x+y:', (x+y)
				x += y

			if x < self.threshold:
				r = x % self.destination
				#print 'randDestination:', r
				return r

	def __str__( self ):
		s = MutableString()

		s += 'source: '
		s += str(self.source)
		s += ', '

		s += 'numDice: '
		s += str(self.numDice)
		s += ', '

		s += 'maxSource: '
		s += str(self.source * self.numDice)
		s += ', '

		s += 'destination: '
		s += str(self.destination)
		s += ', '

		s += 'cycles: '
		s += str(self.threshold / self.destination)
		s += ', '

		s += 'threshold: '
		s += str(self.threshold)
		s += ', '

		s += 'ratio: '
		s += str(int(self.ratio*100))
		s += '%, '

		return str(s)

def test( options ):
	r = Randformer( options.source, options.destination )
	r.calcThreshold( options.ratio )
	print r

	# Test each random combination.
	r.get = SourceEach( r.source, r.numDice ).get().next
	results = Results()
	for i in range(r.threshold):
		v = r.randDestination()
		results.accum(v)
	print results

	# Test random values.
	r.get = SourceRand( r.source, r.numDice ).get().next
	results = Results()
	for i in range(options.loops):
		v = r.randDestination()
		results.accum(v)

		if options.every and (i+1) % options.every == 0:
			print results
	print results
	print

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-d', '--dst', type='int', dest='destination', default=7, help='')
	parser.add_option('-e', '--every', type='int', dest='every', default=1000000, help='')
	parser.add_option('-l', '--loops', type='int', dest='loops', default=100, help='')
	parser.add_option('-s', '--src', type='int', dest='source', default=5, help='')
	parser.add_option('-r', '--ratio', type='float', dest='ratio', default=0.8, help='')
	parser.add_option('--seed', type='int', dest='seed', help='')
	#parser.add_option('-w', '--write', dest='writefile', default=None, metavar='FILE', help='write database file')

	(options, args) = parser.parse_args()
	#print sys.argv
	#print 'options', options
	#print 'args', args

	if options.seed:
		print 'Seeding with ' + str(options.seed) + '.'
		random.seed( options.seed )

	testSourceRand( options.source, options.source**2 )
	testSourceEach( options.source, 2 )

	test( options )

