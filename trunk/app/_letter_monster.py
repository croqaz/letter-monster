#  Letter Monster  #
#        v1        #
#    Main Class    #

import Image, ImageFilter
from os import getcwd                # Get currend directory.
from os import system as cmd         # Command line.
import numpy as np                   # Numpy arrays.
from yaml import load, dump          # Used for reading XML data.
from yaml import CLoader as Loader
from yaml import CDumper as Dumper
from yaml import add_representer, add_constructor
from bz2 import compress, decompress # Compress data in raster.
from time import clock               # Used for timing operations.
from psyco import full ; full ()     # Performance boost.
import sys ; sys.path.insert(0, getcwd() ) # Save current dir in path.
from _classes import * # Need to add curr dir as path to import classes.

print 'I am Python r22!'

#
# Define YAML represent for numpy ndarray.
def ndarray_repr(dumper, data): # NDARRAY.dumps can save any array, Unicode or Integer.
    return dumper.represent_scalar( u'!ndarray', compress(data.dumps()).decode('latin_1') )
add_representer(np.ndarray, ndarray_repr)
#
# Define YAML construct data for numpy ndarray.
def ndarray_construct(loader, node):
    return np.loads( decompress(loader.construct_scalar(node).encode('latin_1')) )
add_constructor(u'!ndarray', ndarray_construct)
#
def sort_zorder(x):
    return x.z
#

class LetterMonster:
    '''This is the Letter Monster Class.\n\
    ^-^ You would have never guessed it.\n\
    It uses no arguments for initialization.'''
    #
    def __init__(self):
        #
        self.DEBUG = True
        #
        self.body = {}
        self.max_morph_rate = 1
        self.visible_size = (100, 100)
        self.bp = Backpack() # Helper functions instance.
        #
        self.data_types = ('raster', 'vector', 'event', 'macro')
        self.Patterns = {
        'default'    : u'&80$21|;:\' ',                        # Original Patrick T. Cossette pattern
        'cro'        : u'MWBHASI+;,. ',                        # Cristi Constantin pattern
        'dos'        : u'\u2588\u2593\u2592\u2665\u2666\u263b\u256c\u263a\u25ca\u25cb\u2591 ', # Cristi Constantin DOS pattern.
        'sharp'      : u'#w4Axv^*\"\'` ',                      # Cristi Constantin Sharp
        'smooth'     : u'a@\u00a9\u0398O90c\u00a4\u2022. ',    # Cristi Constantin Smooth
        'vertical'   : u'\u00b6\u0132I|}\u00ce!VAi; ',         # Cristi Constantin Vertical
        'horizontal' : u'\u25ac\u039e\u00ac\u2261=\u2248~-. ', # Cristi Constantin Horizontal
        'numbers'    : u'0684912357',
        'letters'    : u'NADXEIQOVJL ',
        }
        #
    #
#---------------------------------------------------------------------------------------------------
    #
    def __str__(self):
        '''String representation of the engine.'''
        return 'I am Letter Monster. Baaah!'
        #
    #
#---------------------------------------------------------------------------------------------------
    #
    def Hatch(self, visible_size=(100,100), max_morph_rate=1):
        '''Setup the engine.'''
        self.visible_size = visible_size
        self.max_morph_rate = max_morph_rate
        #
    #
#---------------------------------------------------------------------------------------------------
    #
    def _execute(self, object):
        '''Automatically execute object instructions. "Object" is the name of a data structure.'''
        #
        try:
            vElem = self.body[object]
            vInstructions = vElem.instructions
        except: print( '"%s" object doesn\'t have instructions, or doesn\'t exist! Exiting execute!' % object ) ; return
        #
        if not vInstructions:
            print( '"%s" has null instructions! Exiting execute!' % object ) ; return
        #
        ti = clock()
        if str(vElem)=='vector':
            for vInstr in vInstructions: # For each dictionary in the instructions list.
                vFunc = vInstr['f']      # Save the function to call, then delete this mapping.
                del vInstr['f']
                #
                f = getattr(self.bp, vFunc, 'Error') # Save the function call.
                #
                if f!='Error': # If function is not Error, means it's valid.
                    #
                    # Overwrite the name of the layer with the data of the layer.
                    try: vInstr['vInput'] = self.body[vInstr['vInput']].data
                    except: print( '"%s" doesn\'t have valid data! Call ignored!' % vInput ) ; continue
                    #
                    # Try to call the function with parameters and catch the errors.
                    try: vData = f( **vInstr )
                    except TypeError: print( 'Incorrect arguments for function "%s"! Call ignored!' % vFunc ) ; continue
                    except: print( 'Unknown error occured in "%s" function call! Call ignored!' % vFunc ) ; continue
                    #
                    # Explode data back.
                    if vData: self.body[object].data = vData
                    else: self.body[object].data = []
                    #
                else:
                    print( 'Function "%s" doesn\'t exist! Call ignored!' % vFunc )
                #
        else:
            print( 'Instructions for "%s" object not yet implemented!' % str(vElem) ) ; return
        #
        tf = clock()
        if self.DEBUG: print( 'Execute took %.4f seconds.' % (tf-ti) )
        #
    #
#---------------------------------------------------------------------------------------------------
    #
    def Consume(self, image='image.jpg', x=0, y=0, pattern='default', filter=''):
        '''Takes an image, transforms it into ASCII and stores it internally.'''
        #
        try: vInput = Image.open( image )
        except: print( '"%s" is not a valid image path! Exiting function!' % image ) ; return
        #
        if x and not y:     # If x has a value.
            if self.DEBUG: print( "Resizing to X = %i." % x )
            y = (x * vInput.size[1]) / vInput.size[0]
            print( "Y becomes %i." % y )
        elif y and not x:   # Or if y has a value.
            if self.DEBUG: print( "Resizing to Y = %i." % y )
            x = (y * vInput.size[0]) / vInput.size[1]
            print( "X becomes %i." % x )
        #
        elif x and y:       # If both x and y have a value.
            if self.DEBUG: print( "Disproportionate resize X = %i, Y = %i." % ( x, y ) )
        if x or y:          # If resize was called.
            vInput = vInput.resize((x, y), Image.BICUBIC) # Do the resize.
        del x ; del y
        #
        if filter:          # If filter was called.
            for filt in filter.split('|'):
                filt = filt.upper()
                if filt in ( 'BLUR', 'SMOOTH', 'SMOOTH_MORE', 'DETAIL', 'SHARPEN',
                            'CONTOUR', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE' ):
                    vInput = vInput.filter( getattr(ImageFilter, filt) )
                    print( "Applied %s filter." % filt )
                else:
                    print( '"%s" is not a valid fliter! Filter ignored.' % filt )
            #
        #
        if pattern.lower() in self.Patterns:
            vPattern = self.Patterns[pattern.lower()]
        else:
            print( '"%s" is not a valid pattern! Using default pattern.' % pattern )
            vPattern = self.Patterns['default']
        #
        ti = clock() # Global counter.
        tti = clock() # Local counter.
        vResult = []
        if self.DEBUG: print( "Starting consume..." )
        #
        vLen = len( vPattern )
        getpx = vInput.getpixel
        #
        for py in range(vInput.size[1]): # Cycle through the image's pixels, one by one
            #
            vTempRez = np.empty(vInput.size[0],'U')
            #
            for px in range(vInput.size[0]):
                RGB = getpx((px, py))             # Retrieve pixel RGB values
                vColor = RGB[0] + RGB[1] + RGB[2] # Find the general darkness of the pixel
                #
                for vp in range( vLen ):                      # For each element in the string pattern...
                    if vColor <= ( 255 * 3 / vLen * (vp+1) ): # Return matching character from pattern.
                        vTempRez[px] = vPattern[vp]
                        break
                    elif vColor > ( 255 * 3 / vLen * vLen ) and vColor <= ( 255 * 3 ): # If not in range, return last character from pattern.
                        vTempRez[px] = vPattern[-1]
                        break
                    #
                #
            #
            vResult.append( vTempRez )
            del vTempRez ; del RGB ; del vColor
            #
        #
        ttf = clock()
        if self.DEBUG: print( 'Transformation took %.4f seconds.' % (ttf-tti) )
        for x in range(1, 999):
            if not 'raster'+str(x) in self.body: # If "raster+x" doesn't exist.
                vElem = Raster()
                vElem.name = 'raster'+str(x)
                vElem.data = vResult
                vElem.visible = True
                vElem.lock = False
                self.body['raster'+str(x)] = vElem # Save raster in body.
                del vElem
                break
            #
        #
        del vResult ; del vInput
        tf = clock()
        #
        if self.DEBUG: print( 'Consume took %.4f seconds total.' % (tf-ti) )
        #
    #
#---------------------------------------------------------------------------------------------------
    #
    def Load(self, lmgl):
        '''Load a LMGL (Letter Monster Graphical Letters) file, using YAML.'''
        try: vInput = open( lmgl, 'r' )
        except: print( '"%s" is not a valid path! Exiting function!' % lmgl ) ; return
        #
        ti = clock()
        try: vLmgl = load( vInput )
        except: print( '"%s" cannot be parsed! Invalid YAML file! Exiting function!' % lmgl ) ; return
        #
        self.body = vLmgl
        vInput.close() ; del vInput
        tf = clock()
        #
        if self.DEBUG: print( 'Loading LMGL took %.4f seconds total.' % (tf-ti) )
        #
    #
#---------------------------------------------------------------------------------------------------
    #
    def Save(self, lmgl):
        '''Save body into a LMGL (Letter Monster Graphical Letters) file, using YAML.'''
        try:
            vInput = open( lmgl )
            print( '"%s" is a valid LMGL file! Will not overwrite. Exiting function!' % lmgl ) ; return
        except: pass # If file exists, pass.
        #
        ti = clock()
        vInput = open( lmgl, 'w' )
        dump(self.body, stream=vInput, width=99, indent=2, canonical=False, default_flow_style=False,
            explicit_start=True, explicit_end=True)
        vInput.close() ; del vInput
        tf = clock()
        #
        if self.DEBUG: print( 'Saving LMGL took %.4f seconds total.' % (tf-ti) )
        #
    #
#---------------------------------------------------------------------------------------------------
    #
    def Spit(self, format='WIN CMD'):
        '''
Render function. Returns the current reprezentation of the engine.
All visible Raster and Vector layers are represented.'''
        #
        vOutput = [[]]
        #
        for vElem in sorted(self.body.values(), key=sort_zorder): # For each visible Raster and Vector in body, sorted in Z-order.
            if (str(vElem)=='raster' and vElem.visible) or (str(vElem)=='vector' and vElem.visible):
                Data = vElem.data                 # This is a list of numpy ndarrays.
                #
                for nr_row in range( len(Data) ): # For each numpy ndarray (row) in Data.
                    #
                    NData = Data[nr_row]                     # New data, to be written over old data.
                    OData = vOutput[nr_row:nr_row+1] or [[]] # This is old data. Can be numpy ndarray, or empty list.
                    OData = OData[0]
                    #
                    if len(NData) >= len(OData): 
                        # If new data is longer than old data, old data will be completely overwritten.
                        vOutput[nr_row:nr_row+1] = [NData]
                    else: # Old data is longer than new data ; old data cannot be null.
                        TempB = np.copy(OData)
                        TempB.put( range(len(NData)), NData )
                        vOutput[nr_row:nr_row+1] = [TempB]
                        del TempB
                    #
                #
            # If not Raster or Vector, pass.
        #
        if format=='WIN CMD':
            for vLine in vOutput:
                vEcho = u''.join(u'^'+i for i in vLine)
                if vEcho: cmd( '@ECHO %s' % vEcho.encode('utf') )
                else: cmd( '@ECHO.' )
            #
        # More formats will be implemented soon.
    #
#---------------------------------------------------------------------------------------------------
    #
    def Spawn(self, lmgl=None, out='txt', filename='Out'):
        '''
Export function. Saves the current reprezentation of the engine.
Can also transform one LMGL into : TXT, Excel, HTML, without changing the engine.'''
        if lmgl: # If a LMGL file is specified, export only the LMGL, don't change self.body.
            ti = clock() # Global counter.
            tti = clock() # Local counter.
            try: vInput = open( lmgl, 'r' )
            except: print( '"%s" is not a valid path! Exiting function!' % lmgl ) ; return
            #
            try: vLmgl = load( vInput )
            except: print( '"%s" cannot be parsed! Invalid YAML file! Exiting function!' % lmgl ) ; return
            #
            vInput.close() ; del vInput
            ttf = clock()
            if self.DEBUG: print( 'Loading LMGL (Spawn) took %.4f seconds.' % (ttf-tti) )
        else: vLmgl = self.body
        #
        if out=='txt':
            pass
        elif out=='xls':
            pass
        elif out=='html':
            pass
        else: print( '"%s" is not a valid export type! Exiting function!' % out ) ; return
        #
        tti = clock() # Local counter.
        TempA = [[]]
        #
        for vElem in sorted(vLmgl.values(), key=sort_zorder): # For each visible Raster and Vector in body, sorted in Z-order.
            if (str(vElem)=='raster' and vElem.visible) or (str(vElem)=='vector' and vElem.visible):
                Data = vElem.data                 # This is a list of numpy ndarrays.
                #
                for nr_row in range( len(Data) ): # For each numpy ndarray (row) in Data.
                    #
                    NData = Data[nr_row]                     # New data, to be written over old data.
                    OData = TempA[nr_row:nr_row+1] or [[]] # This is old data. Can be numpy ndarray, or empty list.
                    OData = OData[0]
                    #
                    if len(NData) >= len(OData): 
                        # If new data is longer than old data, old data will be completely overwritten.
                        TempA[nr_row:nr_row+1] = [NData]
                    else: # Old data is longer than new data ; old data cannot be null.
                        TempB = np.copy(OData)
                        TempB.put( range(len(NData)), NData )
                        TempA[nr_row:nr_row+1] = [TempB]
                        del TempB
                    #
                #
            # If not Raster or Vector, pass.
        #
        ttf = clock()
        print( 'Overwriting data took %.4f seconds.' % (ttf-tti) )
        #
        tti = clock()
        vOut = open( filename+'.txt', 'w' )
        vOut.write( ''.join(np.hstack( np.hstack((i,np.array([u'\n'],'U'))) for i in TempA )).encode('utf8') )
        vOut.close() ; del TempA ; del vOut
        ttf = clock()
        if self.DEBUG: print( 'Unite arrays and lists took %.4f seconds.' % (ttf-tti) )
        #
        tf = clock()
        if self.DEBUG: print( 'Spawn took %.4f seconds total.' % (tf-ti) )
        #
    #

#