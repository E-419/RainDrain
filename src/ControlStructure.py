import os, sys, shutil, csv, math

from pathlib import Path



class Constant(object):
	"""
	This is the storage container for the various constants (like gravity)
	"""
	gravity = 32.2 # ft / sec**2

	def __init__(self, arg):
		super(Constant, self).__init__()
		self.arg = arg
	

class Orifice(object):
	"""
		elevation => Feet
		diameter  => Inches
		coeficient of discharge => Unitless, 0.68 by default
	"""

	def __init__(self, 
					elevation = 0,		# Feet
					diameter = 0, 		# Inches
					coefOfDischarge = 0.68):
		self.elevation = elevation
		self.diameter = diameter / 12.0
		self.coefOfDischarge = coefOfDischarge

	@property
	def area(self):
		return math.pi * (self.diameter**2) / 4

	def flow(self, waterSurfaceElevation = 0):
		flow = 0
		head = waterSurfaceElevation - self.elevation
		if head < 0:
			pass # No flow if the water surface is below (or level with) the orifice
		else:
			# This needs some work, the math needs to come from that one spreadsheet with the SSD converter
			flow = self.coefOfDischarge * self.area * math.sqrt( 2 * Constant.gravity * head )
		return flow
	pass


    
class Notch(object):
    pass

class Riser(object):
    
    def __init__(self, 
                    height = None,      # Feet
                    diameter = None,    # Inches across riser pipe
                    orifice = dict(),   # dict() of orifices, {1:orifice(), 2:orifice(), ...}
                    notch = dict(),
                ):
        self.height = height
        self.diameter = diameter
        self.orifice = orifice
        # self.
        
    def setHeight(self, newHeight):
        self.height = newHeight
    
    def setDiameter(self, newDiameter):
        self.diameter = newDiameter
    
    def test(arg1, arg2):
        return 'test worked'
    
    



def drillSizes(maxSize = 1.0, drillDenom = 64):
    totalSizes = int(maxSize * drillDenom)
    increment = 1 / drillDenom
    currentSize = increment
    for i in range(1, totalSizes):
        print(str(i) + '/' + str(drillDenom) + ' = ' + str(currentSize))
        currentSize += increment



if __name__ == "__main__":
	import matplotlib as plt


	o1 = Orifice(elevation = 0, diameter = 1.5)
	# print(o1.area)
	div = 4/45
	for i in range(0, int(7 * 1/div)):
		print(i * div, o1.flow(i*div))
   