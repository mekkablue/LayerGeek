# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Filter without dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class LayerGeek(FilterWithDialog):
	
	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	
	# Text field in dialog
	layerFunctionField = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Layer Geek',
			'de': u'Layer Geek',
		})
		self.actionButtonLabel = Glyphs.localize({
			'en': u'Execute',
			'de': u'Ausführen',
		})
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	@objc.python_method
	def start(self):
		Glyphs.registerDefault('com.mekkablue.LayerGeek.layerFunction', 'correctPathDirection')
		# Set value of text field
		self.layerFunctionField.setStringValue_( Glyphs.defaults['com.mekkablue.LayerGeek.layerFunction'] )
		# Set focus to text field
		self.layerFunctionField.becomeFirstResponder()
		
	# Action triggered by UI:
	@objc.IBAction
	def setLayerFunction_( self, sender ):
		# Store value coming in from dialog
		Glyphs.defaults['com.mekkablue.LayerGeek.layerFunction'] = sender.stringValue()
		# Trigger redraw
		self.update()
	
	# Actual filter
	@objc.python_method
	def filter(self, Layer, inEditView, customParameters):
		if customParameters:
			# Called on font export, get value from customParameters:
			numberedParameters = [k for k in customParameters.keys() if type(k) is int]
			layerFunctions = [customParameters[x] for x in sorted(numberedParameters)]
		else:
			# Called through UI, use stored value
			layerFunctions = Glyphs.defaults['com.mekkablue.LayerGeek.layerFunction'].split(";")

		for layerFunction in layerFunctions:
			if layerFunction:
				try:
					# fix layerFunction input:
					layerFunction = "Layer." + ( layerFunction.strip().strip( "." ) + "()" ).replace( ")()", ")" )
					# execute layerFunction:
					eval( layerFunction )
				except:
					# exit gracefully:
					pass
		
	@objc.python_method
	def generateCustomParameter( self ):
		return "%s; %s" % (
			self.__class__.__name__,
			Glyphs.defaults['com.mekkablue.LayerGeek.layerFunction'] 
		)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
