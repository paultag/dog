# Copyright (c) Paul R. Tagliamonte <tag@pault.ag>, 2011 under the terms and
# conditions of the Expat license.

import sys

root = "/usr/share/dog/colors"

class ccat:
	def __init__( self ):
		self.parse_state = "entry"
		self.colors      = {}
		self.states      = {}
	
	def cat( self, filepath ):
		foo = open(filepath, 'r').read()
		self.print_string_block( foo )
	
	def doThing( self, passThrough, nS, charzard ):
		if nS != self.parse_state:
			self.parse_state = nS
			sys.stdout.write("[%sm" % self.colors[nS])
			if passThrough == 'p':
				self.handleChar( charzard )
				return
		sys.stdout.write( charzard )
	
	def handleChar( self, charzard ):
		try:
			passThrough, nS = self.states[self.parse_state][charzard]
			self.doThing( passThrough, nS, charzard )
		except KeyError as e:
			passThrough, nS = self.states[self.parse_state]["default"]
			self.doThing( passThrough, nS, charzard )
	
	def print_string_block( self, to_parse ):
		for line in to_parse.split('\n'):
			for char in line:
				self.handleChar( char )
			self.handleChar( "\n" )
	
	def set_colors_by_name( self, name ):
		
		path = "%s/%s" % ( root, name )
		
		color = open( "%s/%s" % (path, "states.color"), 'r' ).read()
		rules = open( "%s/%s" % (path, "states"),       'r' ).read()
		
		for c in color.split('\n'):
			cp = c.split()
			if len(cp) == 2:
				self.colors[cp[0]] = cp[1]
		for rule in rules.split('\n'):
			if rule[:1] == ' ':
				trans = rule.split()
				if len(trans) == 1:
					# attempt to read...
					trans.append(trans[0])
					trans[0] = ' '


				trans[0] = trans[0].decode('string_escape')
				if trans[1][:1] == '^':
					cur_state[trans[0]] = ( "p", trans[1][1:] )
				else:
					cur_state[trans[0]] = ( "d", trans[1] )
			elif rule.strip() == '':
				pass
			else:
				trans = rule.split()
				if trans[1][:1] == '^':
					self.states[trans[0]] = {
						"default" : ( "p", trans[1][1:] )
					}
				else:
					self.states[trans[0]] = {
						"default" : ( "d", trans[1] )
					}
				cur_state = self.states[trans[0]]
