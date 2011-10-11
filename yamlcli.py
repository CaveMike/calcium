#!/usr/bin/python
import sys
import os
from optparse import OptionParser
from UserString import MutableString
import yaml

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-t', '--test', action='store_true', dest='test', default=False, help='do not execute the command')
    parser.add_option('-s', '--schema', dest='schema', default=os.path.dirname(sys.argv[0]) + '/cli.yaml', metavar='FILE', help='specify the schema file')

    (options, args) = parser.parse_args()
    #print sys.argv
    #print 'options', options
    #print 'args', args

    # Read schema.
    try:
        f = open(options.schema)
        root = yaml.load(f)
    except yaml.YAMLError, e:
        print 'Invalid schema, %s.' % options.schema
        f.close()
        sys.exit(-1)
    except IOError, e:
        print 'Failed to open schema, %s.' % options.schema
        sys.exit(-1)

    f.close()
    #print yaml.dump(root)

    # Header
    s = MutableString()
    if root.has_key('_HEADER'):
        s += root['_HEADER']

    # Arguments
    node = root
    for arg in args:
        #print yaml.dump(node)
        try:
            node = node[arg]
            s += node['_VALUE']
        except KeyError, e:
            s += arg

    # Body
    if root.has_key('_FOOTER'):
        s += root['_FOOTER']

    # Execute
    print '# ' + s

    if not options.test:
        os.system(str(s))

