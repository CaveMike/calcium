#!/usr/bin/env python
from optparse import OptionParser
from UserString import MutableString
import math
import os
import pickle
import string
import sys

class LogEater:
	def __init__( self, threshold ):
		self.threshold = threshold

		all = ''.join( chr(n) for n in xrange(256) )
		self.filter = all[:65] + all[91:97] + all[123:]

		self.data = {}
		self.files = 0

	def __walk( self, filename, function ):
		f = open( filename, 'r' )

		l = True
		while l:
			l = f.readline()
			l2 = l.translate( None, self.filter )
			if l2:
				if function:
					function( l, l2 )

		f.close()

	def __build( self, l, l2 ):
		self.data[l2] = self.data.setdefault( l2, 0 ) + 1

	def __test( self, l, l2 ):
		v = self.data.setdefault( l2, 0 )
		if v < self.threshold:
			print l,

	def build( self, filename ):
		self.__walk( filename, self.__build )
		self.files += 1

	def test( self, filename ):
		print 'Testing ' + str(filename)
		self.__walk( filename, self.__test )

	def purge( self ):
		new = {}
		for ( key, value ) in self.data.iteritems():
			if value >= self.threshold:
				new[key] = value

		self.data = new

	def stats( self ):
		s = MutableString()

		s += 'files: '
		s += str(self.files)
		s += '\n'

		s += 'lines: '
		s += str( sum( [ v for v in self.data.values() ] ) )
		s += '\n'

		s += 'unqiue lines: '
		s += str(len(self.data))
		s += '\n'

		return str(s)

	def hits( self ):
		s = MutableString()

		# Calculate hit table.
		hits = {}
		for (key, value) in self.data.iteritems():
			#value = int( 10 * math.log(value ))
			hits[value] = hits.setdefault( value, 0 ) + 1
		# Print hit table.
		for key in sorted(hits.keys()):
			s += str(key)
			s += ': '
			s += str(hits[key])
			s += '\n'

		return str(s)

	def __str__( self ):
		s = MutableString()

		s += self.stats()

		for key in sorted(self.data.keys()):
			s += str(key)
			s += ': '
			s += str(self.data[key])
			s += '\n'

		return str(s)


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('--threshold', action='store_true', dest='threshold', default=3, help='set the test threshold')
	parser.add_option('-t', '--test', dest='test', default=None, metavar='FILE', help='test file')
	parser.add_option('-r', '--read', dest='readfile', default=None, metavar='FILE', help='read database file')
	parser.add_option('-w', '--write', dest='writefile', default=None, metavar='FILE', help='write database file')

	(options, args) = parser.parse_args()
	#print sys.argv
	#print 'options', options
	#print 'args', args

	e = LogEater( options.threshold )

	if options.readfile:
		e = pickle.load( open(options.readfile, 'r') )
		print e.stats()

	for arg in args:
		e.build( arg )
		print e.stats()

	if options.test:
		e.test( options.test )

	if options.writefile:
		e.purge()
		pickle.dump( e, open(options.writefile, 'w') )

