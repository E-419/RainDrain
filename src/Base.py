# This defines the base object that all classes inherit from


class RDObject(object):
	def __init__(self, elevation_bottom = 0):
		self.elevation_bottom = elevation_bottom

	@property
	def start_stage(self):
		return self.elevation_bottom

	@property
	def start_stage_elevation(self):
		return self.start_stage



class RDCircle(RDObject):
	'''
	This objects contains the methods typical for circular objects
	'''
	def __init__(self, elevation_bottom = 0, diameter_in = None, diameter_ft = None ):
		super().__init__(elevation_bottom = elevation_bottom)
		if diameter_ft:
			self.set_diameter(feet = diameter_ft)
		elif diameter_in:
			self.set_diameter(inches = diameter_in)


	def set_diameter(self, inches = None, feet = None):
		if inches:
			self._diameter_inches = inches
			self._diameter_feet = inches / 12
			return True
		elif feet:
			self._diameter_feet = feet
			self._diameter_inches = feet * 12
			return True
		return False

	@property
	def diameter_feet(self):
		return self._diameter_feet
	
	@property
	def radius_feet(self):
		return self._diameter_feet / 2


	