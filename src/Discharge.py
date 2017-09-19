'''
This module is for the definition of the outlet flows from a control structure, given a water surface elevation

Currently Available:
	Orifice() objects can be given a 

Goals:
	Use SymPy to make an algebraic solver for the stormwater detention/optimization problem.



'''
import math

class Units(object):
	def gravity():
		return 32.2


class Orifice(object):
	""" 
	Init_Property:  Units
	
	diameter:	   Inches
	elevation:	  Feet
	
	stage/water_surface_elevation is changing all the 
	time so it's passed into every function for clarity
	
	This object is set to output an SSD that matches WWHM 
	to 4 or 5 decimal places. That should be suffcient to 
	produce an SSD for use in MGS Flood for expedited 
	iteration.

	"""
	
	
	
	def __init__(self, diameter, elevation, orientation_vertical = None, orientation_horizontal = True):
		'''
		This object is set in initialize in the horizontal orientation with a coef_of_discharge == 0.62
		and the result is EXTREMELY close to the WWHM SSD tables that can be generated 
		'''
		self._diameter_inches = diameter
		self._diameter_feet = self._diameter_inches / 12
		self._elevation = elevation
		self.orientation_horizontal = None
		self.orientation_vertical = None
		self.set_orientation(orientation_horizontal)
		self.set_orientation(orientation_vertical)
	
	def coef_of_discharge():
		return 0.62 # WWHM's Value
		# return 0.62354

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

	def set_orientation(self, vertical = None, horzontal = None):
		if vertical:
			self.orientation_vertical = True
			self.orientation_horizontal = False
			return True
		elif horzontal:
			self.orientation_horizontal = True
			self.orientation_vertical = False
			return True
		return False

	@property
	def stage_elevation(self):
		return self._elevation
	
	@property
	def diameter_feet(self):
		return self._diameter_feet
	
	@property
	def radius_feet(self):
		return self._diameter_feet / 2
	
	
	def discharge(self, water_surface_elevation = 0):
		if water_surface_elevation < self.stage_elevation:
			return 0
		stage = water_surface_elevation
		return Orifice.coef_of_discharge() * self.submerged_area(stage) * math.sqrt(self.head(stage) * 2 * Units.gravity())
		
	
	def submerged_area(self, water_surface_elevation):
		stage = water_surface_elevation
		area = 0
		if self.orientation_vertical:
			if stage >= self.diameter_feet + self.stage_elevation:
				area = math.pi * self.radius_feet**2
			elif stage < self.radius_feet + self.stage_elevation:
				angle = self.angle(stage)
				area = self.radius_feet**2 * (angle - math.sin(angle))/2
			else:
				angle = self.angle(stage)
				area = math.pi * self.radius_feet**2 - self.radius_feet**2 * (angle - math.sin(angle))/2
			return area
		elif self.orientation_horizontal:
			area = math.pi * self.radius_feet**2
			return area

	def angle(self, water_surface_elevation):
		'''
		This is the angle of something... that has something to do with the 
		amount of the orifice that is submerged at a given stage.
			input: stage_elevation in feet
		'''
		stage = water_surface_elevation # always > self.stage_elevation, see Orifice.discharge() and Orifice.submerged_area()
		orifice_head = stage - self.stage_elevation

		if stage < self.radius_feet + self.stage_elevation:
			angle = 2 * math.acos( (self.radius_feet - orifice_head)/(self.radius_feet))
		else:	
			unsubmerged_orifice_height = self.diameter_feet - (orifice_head)
			angle = 2 * math.acos( (self.radius_feet - unsubmerged_orifice_height)/(self.radius_feet))

		return angle
	
	def head(self, water_surface_elevation = 0):
		if self.orientation_vertical:
			if water_surface_elevation < self.stage_elevation:
				return 0
			elif water_surface_elevation < self.stage_elevation + self.diameter_feet:
				# This looks like a shortcut for the necessary integration required for this calc
				return (water_surface_elevation - self.stage_elevation) / 2
			else:
				return (water_surface_elevation - self.stage_elevation - self.radius_feet)
		
		elif self.orientation_horizontal:
			if water_surface_elevation < self.stage_elevation:
				return 0
			else:
				return (water_surface_elevation - self.stage_elevation)



class Notch(object):
	def __init__(self, diameter, elevation, orientation_vertical = None, orientation_horizontal = True):
		'''
		This object is set in initialize in the horizontal orientation with a coef_of_discharge == 0.62
		and the result is EXTREMELY close to the WWHM SSD tables that can be generated 
		'''
		self._diameter_inches = diameter
		self._diameter_feet = self._diameter_inches / 12
		self._elevation = elevation
		self.orientation_horizontal = None
		self.orientation_vertical = None



def stage_intervals(live_storage_depth, intervals_per_foot = 12, intervals_total = None):
	intervals = live_storage_depth * intervals_per_foot
	delta = live_storage_depth / intervals
	stage_i = list()
	for stage in range(0, int(intervals) + 1):
		stage_i.append(delta * stage)
	return stage_i	

if __name__ == "__main__":
	o1 = Orifice(diameter = 8, elevation = 1)
	o2 = Orifice(diameter = 0.75, elevation = 1.5)
	o3 = Orifice(diameter = 2, elevation = 4)
	for orf in (o1,o2,o3):
		orf.set_orientation(horzontal = True)

	live_storage_depth = 8.9 # feet

	for stage in stage_intervals(live_storage_depth, intervals_per_foot = 15):
		dis = 0
		dis += o1.discharge(stage)
		dis += o2.discharge(stage)
		dis += o3.discharge(stage)
		print(round(stage, 3), 'ft', round(dis, 5) , 'cfs')


















	