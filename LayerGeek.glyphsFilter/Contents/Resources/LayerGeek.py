#!/usr/bin/env python
# encoding: utf-8

import objc
import GlyphsApp
from GlyphsApp.plugins import *
import sys, os, re



"""
	Using Interface Builder (IB):
	
	Your code communicates with the UI through
	- IBOutlets (.py->GUI): values available to a UI element (e.g. a string for a text field)
	- IBActions (GUI->.py): methods in this class, triggered by buttons or other UI elements
	
	In order to make the Interface Builder items work, follow these steps:
	1. Make sure you have your IBOutlets (other than _theView)
	   defined as class variables at the beginning of this controller class.
	2. Immediately *before* the def statement of a method that is supposed to be triggered
	   by a UI action (e.g., setMyValue_() triggered by the My Value field), put:
		@objc.IBAction
	   Make sure the method name ends with an underscore, e.g. setValue_(),
	   otherwise the action will not be able to send its value to the class method.
	3. Open the .xib file in XCode, and add and arrange interface elements.
	4. Add this .py file via File > Add Files..., Xcode will recognize IBOutlets and IBACtions
	5. In the left sidebar, choose Placeholders > File's Owner,
	   in the right sidebar, open the Identity inspector (3rd icon),
	   and put the name of this controller class in the Custom Class > Class field
	6. IBOutlets: Ctrl-drag from the File's Owner to a UI element (e.g. text field),
	   and choose which outlet shall be linked to the UI element
	7. IBActions: Ctrl-drag from a UI element (e.g. button) to the File’s Owner in the left sidebar,
	   and choose the class method the UI element is supposed to trigger.
	   If you want a stepping field (change the value with up/downarrow),
	   then select the Entry Field, and set Identity Inspector > Custom Class to:
		GSSteppingTextField
	   ... and Attributes Inspector (top right, 4th icon) > Control > State to:
		Continuous
	8. Compile the .xib file to a .nib file with this Terminal command:
		ibtool xxx.xib --compile xxx.nib
	   (Replace xxx by the name of your xib/nib)
	   Please note: Every time the .xib is changed, it has to be recompiled to a .nib.
	   Check Console.app for error messages to see if everything went right.
"""

class LayerGeek ( GSFilterPlugin ):
	"""
	All 'myValue' and 'myValueField' references are just an example.
	They correspond to the 'My Value' field in the .xib file.
	Replace and add your own class variables.
	"""
	layerFunctionField = objc.IBOutlet()
	
	
	def init( self ):
		"""
		Do all initializing here.
		This is a good place to call random.seed() if you want to use randomisation.
		In that case, don't forget to import random at the top of this file.
		"""
		try:
			NSBundle.loadNibNamed_owner_( "LayerGeekDialog", self )
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is the name as it appears in the menu
		and in the title of the dialog window.
		"""
		try:
			return "Layer Geek"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def actionName( self ):
		"""
		This is the title of the button in the settings dialog.
		Use something descriptive like 'Move', 'Rotate', or at least 'Apply'.
		"""
		try:
			return "Execute"
		except Exception as e:
			self.logToConsole( "actionName: %s" % str(e) )
	
	def keyEquivalent( self ):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def setup( self ):
		try:
			"""
			Prepares and pre-fills the dialog fields.
			"""
			super( LayerGeek, self ).setup()
			FontMaster = self.valueForKey_( "fontMaster" )
			self.layerFunction = self.setDefaultStringValue( "layerFunction", "correctPathDirection()", FontMaster )
			self.layerFunctionField.setStringValue_( self.layerFunction )
			# self.layerFunctionField.cell().setBackgroundStyle_( NSBackgroundStyleDark )
			self.process_( None )
			return None
		except Exception as e:
			self.logToConsole( "setup: %s" % str(e) )
			# if something goes wrong, you can return an NSError object with details
	
	def setDefaultFloatValue( self, userDataKey, defaultValue, FontMaster ):
		"""
		Returns either the stored or default value for the given userDataKey.
		Assumes a floating point value. For use in self.setup().
		"""
		try:
			if userDataKey in FontMaster.userData:
				return FontMaster.userData[userDataKey].floatValue()
			else:
				return defaultValue
		except Exception as e:
			self.logToConsole( "setDefaultFloatValue: %s" % str(e) )

	def setDefaultFloatValue( self, userDataKey, defaultValue, FontMaster ):
		"""
		Returns either the stored or default value for the given userDataKey.
		Assumes a floating point value. For use in self.setup().
		"""
		try:
			if userDataKey in FontMaster.userData:
				return FontMaster.userData[userDataKey].floatValue()
			else:
				return defaultValue
		except Exception as e:
			self.logToConsole( "setDefaultFloatValue: %s" % str(e) )
			
	def setDefaultStringValue( self, userDataKey, defaultValue, FontMaster ):
		"""
		Returns either the stored or default value for the given userDataKey.
		Assumes an integer value. For use in self.setup().
		"""
		try:
			if userDataKey in FontMaster.userData:
				return FontMaster.userData[userDataKey]
			else:
				return defaultValue
		except Exception as e:
			self.logToConsole( "setDefaultStringValue: %s" % str(e) )
	
	@objc.IBAction
	def setLayerFunction_( self, sender ):
		"""
		Called whenever the corresponding dialog field is changed.
		Gets the contents of the field and puts it into a class variable.
		Add methods like this for each option in the dialog.
		Important: the method name must end with an underscore, e.g., setValue_(),
		otherwise the dialog action will not be able to connect to it.
		"""
		try:
			layerFunction = sender.stringValue()
			if layerFunction != self.layerFunction:
				self.layerFunction = layerFunction
				self.process_( None )
		except Exception as e:
			self.logToConsole( "setLayerFunction_: %s" % str(e) )
	
	@objc.IBAction
	def copyParameter_( self, sender ):
		"""
		Copies the current setting as custom parameter to the clipboard.
		"""
		try:
			parameterFunction = self.layerFunction
			parameterText = """(
        {
        Filter = "LayerGeek;%s";
    }
)""" % ( parameterFunction )
			
			myClipboard = NSPasteboard.generalPasteboard()
			myClipboard.declareTypes_owner_( [NSStringPboardType], None )
			myClipboard.setString_forType_( parameterText, NSStringPboardType )
		except Exception as e:
			self.logToConsole( "copyParameter_: %s" % str(e) )
	
	def processLayerWithValues( self, Layer, layerFunctions ):
		"""
		This is where your code for processing each layer goes.
		This method is the one eventually called by either the Custom Parameter or Dialog UI.
		Don't call your class variables here, just add a method argument for each Dialog option.
		"""
		try:
			listOfLayerFunctions = layerFunctions.split(";")
			for layerFunction in listOfLayerFunctions:
				if layerFunction:
					try:
						# fix layerFunction input:
						layerFunction = "Layer." + ( layerFunction.strip( "." ) + "()" ).replace( ")()", ")" )
						# execute layerFunction:
						eval( layerFunction )
					except:
						pass
		except Exception as e:
			self.logToConsole( "processLayerWithValues: %s" % str(e) )
	
	def processFont_withArguments_( self, Font, Arguments ):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			# set glyphList to all glyphs
			glyphList = Font.glyphs
			
			# Override defaults with actual values from custom parameter:
			if len( Arguments ) > 1:
				
				# change glyphList to include or exclude glyphs
				if "exclude:" in Arguments[-1]:
					excludeList = [ n.strip() for n in Arguments.pop(-1).replace("exclude:","").strip().split(",") ]
					glyphList = [ g for g in glyphList if not g.name in excludeList ]
				elif "include:" in Arguments[-1]:
					includeList = [ n.strip() for n in Arguments.pop(-1).replace("include:","").strip().split(",") ]
					glyphList = [ Font.glyphs[n] for n in includeList ]
				
				# process Arguments:
				for thisArgument in Arguments[1:]:
					layerFunction = str( thisArgument )
				
					# With these values, call your code on every glyph in glyphList:
					FontMasterId = Font.fontMasterAtIndex_(0).id
					for Glyph in glyphList:
						Layer = Glyph.layerForKey_( FontMasterId )
						self.processLayerWithValues( Layer, layerFunction ) # add your class variables here
		except Exception as e:
			self.logToConsole( "processFont_withArguments_: %s" % str(e) )
	
	def process_( self, sender ):
		"""
		This method gets called when the user invokes the Dialog.
		"""
		try:
			# Create Preview in Edit View, and save & show original in ShadowLayers:
			ShadowLayers = self.valueForKey_( "shadowLayers" )
			Layers = self.valueForKey_( "layers" )
			checkSelection = True
			for k in range(len( ShadowLayers )):
				ShadowLayer = ShadowLayers[k]
				Layer = Layers[k]
				Layer.setPaths_( NSMutableArray.alloc().initWithArray_copyItems_( ShadowLayer.pyobjc_instanceMethods.paths(), True ) )
				Layer.setSelection_( NSMutableArray.array() )
				if len(ShadowLayer.selection) > 0 and checkSelection:
					for i in range(len( ShadowLayer.paths )):
						currShadowPath = ShadowLayer.paths[i]
						currLayerPath = Layer.paths[i]
						for j in range(len(currShadowPath.nodes)):
							currShadowNode = currShadowPath.nodes[j]
							if ShadowLayer.selection.containsObject_( currShadowNode ):
								Layer.addSelection_( currLayerPath.nodes[j] )
								
				self.processLayerWithValues( Layer, self.layerFunction ) # add your class variables here
			Layer.clearSelection()
		
			# Safe the values in the FontMaster. But could be saved in UserDefaults, too.
			FontMaster = self.valueForKey_( "fontMaster" )
			FontMaster.userData[ "layerFunction" ] = self.layerFunction
			
			# call the superclass to trigger the immediate redraw:
			super( LayerGeek, self ).process_( sender )
		except Exception as e:
			self.logToConsole( "process_: %s" % str(e) )
			
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Filter %s:\n%s" % ( self.title(), message )
		NSLog( myLog )
