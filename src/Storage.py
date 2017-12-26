'''

stage_depth is a local reference depth within an object
	-> all calc's are performed using this property

elevation is an absolute reference between objects
	-> stage_depth is computed from elevation by subtracting start_stage_elevation
	-> all output is translated from stage_depth to elevation
	-> this is the primary io between the SSD object and all child objects

'''
import math
from sympy.solvers import solve
from sympy import integrate, log, exp, oo, symbols

import Base

if __name__ == '_ _main__':
	derivation_string = '''
	***** Storage Volume Derivation ******

	Volume = Integral(Length * Width, from=0, to=Height, WRT=Height)
		where Length = bottom_length + Height * Slopes * 2
	'''
	print(derivation_string)
	# Assumes Slope is uniform around the pond/vault:
	x,y,z,Slope = symbols(('x','y','z','Slope'))

	volume = integrate((x + 2 * (Slope * z)) * (y + 2 * (Slope * z)),(z, 0, z))

	print('Uniform side slopes: x = {0}, y = {1}, z = {2}, Slopes = {3}:1'.format(10,20,5,3))
	print('Pond Volume =',volume, '\nPond Volume =', volume.evalf(subs={x:10, 
																		y:20, 
																		z:5, 
																		Slope:3}) / 43560)
	print()

	# Generalized form, all slopes are independent:
	x,y,z,slope_x_1, slope_x_2, slope_y_1, slope_y_2 = symbols(
		('x','y','z','slope_x_1',' slope_x_2',' slope_y_1',' slope_y_2'))

	volume = integrate( (x + (slope_x_1 * z) + (slope_x_2 * z)) * 
						(y + (slope_y_1 * z) + (slope_y_2 * z)),
						(z, 0, z))
	print('Unique side slopes')
	print('Pond Volume =',volume, '\nPond Volume =', volume.evalf(subs={x:10, 
																		y:20, 
																		z:5, 
																		slope_x_1:3, 
																		slope_x_2:3, 
																		slope_y_1:3, 
																		slope_y_2:3}) / 43560)
	print()									  


		
	# Generalized form, all slopes are independent, length is a function of width:
	x,y,z,slope_x_1, slope_x_2, slope_y_1, slope_y_2, volume, len_to_width = symbols(
		('x','y','z','slope_x_1',' slope_x_2',' slope_y_1',' slope_y_2', 'volume', 'len_to_width'))


	# x == length
	# y == width
	# y = len_to_width * x
	y =  x / len_to_width

	# Solve for width given a depth, volume, and side slopes (output is mostly usable because quadratic roots):
	answer = solve(	x*y*z + 
			z**3*(  slope_x_1*slope_y_1/3 + 
					slope_x_1*slope_y_2/3 + 
					slope_x_2*slope_y_1/3 + 
					slope_x_2*slope_y_2/3) +
			z**2*(  slope_x_1*y/2 + 
					slope_x_2*y/2 + 
					slope_y_1*x/2 + 
					slope_y_2*x/2) - volume, x)

	print(30*'#', 5*'\n', answer[0], 5*'\n', 30*'#')
	'''
	# Solve for depth given a width, volume, and side slopes (output is not very usable due to cubic roots)
	answer_z = solve(	x*y*z + 
			z**3*(  slope_x_1*slope_y_1/3 + 
					slope_x_1*slope_y_2/3 + 
					slope_x_2*slope_y_1/3 + 
					slope_x_2*slope_y_2/3) +
			z**2*(  slope_x_1*y/2 + 
					slope_x_2*y/2 + 
					slope_y_1*x/2 + 
					slope_y_2*x/2) - volume, z)
	'''


	print(30*'#' + 5*'\n')
	_slope = 0
	ltw = 1
	root_1 = answer[0].subs({		slope_x_1:_slope,
									slope_x_2:_slope,
									slope_y_1:_slope,
									slope_y_2:_slope,
									z:1,
									len_to_width:ltw,
									volume:3600,
									})


	print(5*'\n', answer[0])

	print(root_1, root_1.evalf(), root_1.evalf() / ltw)
	print(5*'\n' + 30*'#')


class RDStorage(Base.RDObject):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def volume_at_stage(self, stage_depth):
		raise(Exception('You must define the ".volume_at_stage" method in the subclass directly.'))

	def stage_depth_with_volume(self, volume, precision = 0.1):
		'''
		This returns the stage_depth at which the input volume is achieved to a given accuracy (default == 1e-5)

		The solution complexity is log(n) via the bisection method

		Precedure:
			1. Define upper and lower bounds
				upper = max_stage
				lower = 0
			2. Test if between initial bounds 
				If greater than upper: upper = upper * 2; repeat 2.;
				If less than lower and lower = 0: raise error; 			exit;
				Set middle initially
			
			3. Check precision
				If good: break loop;									exit;
				Limit iteration;
			4. Test if greater than middle
				If greater: lower = middle
				if not greater: upper = middle
			5. Find middle (avg(upper, lower)); repeat 3.;
			6. return middle

		'''
		# 1.
		upper_stage  = self.max_depth
		lower_stage  = 0		# By Definition: Volume == 0

		# 2.
		while self.volume_at_stage(upper_stage) < volume:
			upper_stage = upper_stage * 2

		if volume < 0:
			raise(Exception('\nVolume must be greater than 0.\n'))
		

		middle_stage = (upper_stage + lower_stage) / 2 

		# 3.
		itr = 0
		while abs(volume - self.volume_at_stage(middle_stage)) > precision and itr < 100:
			itr += 1
			
			# 4.
			if volume > self.volume_at_stage(middle_stage):
				lower_stage = middle_stage
			else:
				upper_stage = middle_stage
			
			# 5.
			middle_stage = (upper_stage + lower_stage) / 2	
				
		# 6.
		return middle_stage



class Pond(RDStorage):
	def __init__(self,  bottom_length = 0, 
						bottom_width = 0, 
						depth = None, 
						slope_width_1 = 3, 
						slope_width_2 = 3, 
						slope_length_1 = 3, 
						slope_length_2 = 3,
						slope = None,
						elevation = 0,
						len_to_width = 1,
						volume = None,
						):
		super().__init__(elevation_bottom = elevation)

		self.x = bottom_width
		self.y = bottom_length
		self.z = depth
		self.len_to_width = len_to_width
		print(slope)
		if slope != None:
			self.slope_width_1 = slope
			self.slope_width_2 = slope
			self.slope_length_1 = slope
			self.slope_length_2 = slope
		else:
			self.slope_width_1 = slope_width_1
			self.slope_width_2 = slope_width_2
			self.slope_length_1 = slope_length_1
			self.slope_length_2 = slope_length_2
		
		print(self.slope_width_1)
		if volume and depth:
			self.set_len_and_width(volume = volume, depth = depth)
		else:
			self.volume_max = 0

		self.compute_max_volume()
	
	def set_max_depth(self, depth):
		self.z = depth

	@property
	def max_depth(self):
		return self.z

	def set_bottom_width(self, width):
		self.x = width

	@property
	def bottom_width(self):
		return self.x

	def set_bottom_length(self, length):
		self.y = length

	@property
	def bottom_length(self):
		return self.y
	
	def compute_max_volume(self):
		self.volume_max = self.volume_at_stage(self.max_depth)
	
	def width_at_stage(self, stage_depth):
		return self.bottom_width  + (stage_depth * self.slope_width_1)  + (stage_depth * self.slope_width_2)
	
	def length_at_stage(self, stage_depth):
		return self.bottom_length + (stage_depth * self.slope_length_1) + (stage_depth * self.slope_length_2)
	
	def area_at_stage(self, stage_depth):
		width = self.width_at_stage(stage_depth)
		length = self.length_at_stage(stage_depth)
		return length * width
		
	def volume_at_stage(self, stage_depth):
		'''
		# # # # # # # # # # # # # # # # # # 
		#   Derivation of volume formula
		#
		
		from sympy import integrate, log, exp, oo, symbols
		
		# Generalized form, all slopes are independent:
		x,y,z,slope_x_1, slope_x_2, slope_y_1, slope_y_2 = symbols(
			('x','y','z','slope_x_1',' slope_x_2',' slope_y_1',' slope_y_2'))
		
		volume = integrate( (x + (slope_x_1 * z) + (slope_x_2 * z)) * 
							(y + (slope_y_1 * z) + (slope_y_2 * z)),
							(z, 0, z))
		
		# This is the output required for the class method below:
		print(volume)
		
	   
		
		print(volume, '\n', volume.evalf(subs={ x:10, 
												y:20, 
												z:5, 
												slope_x_1:3, 
												slope_x_2:3, 
												slope_y_1:3, 
												slope_y_2:3}) / 43560)

		'''
		x = self.bottom_width
		y = self.bottom_length
		z = stage_depth
		slope_x_1 = self.slope_width_1
		slope_x_2 = self.slope_width_2
		slope_y_1 = self.slope_length_1
		slope_y_2 = self.slope_length_2
		
		return (	x*y*z + 
					z**3*(  slope_x_1*slope_y_1/3 + 
							slope_x_1*slope_y_2/3 + 
							slope_x_2*slope_y_1/3 + 
							slope_x_2*slope_y_2/3) +
					z**2*(  slope_x_1*y/2 + 
							slope_x_2*y/2 + 
							slope_y_1*x/2 + 
							slope_y_2*x/2)
				)
	

	@property
	def elevation_at_max_stage(self):
		return self.start_stage_elevation + self.max_depth

	def length_at_elevation(self, elevation):
		stage_depth = elevation - self.start_stage_elevation
		if stage_depth >= 0:
			return self.length_at_stage(stage_depth)
		else:
			return 0

	def width_at_elevation(self, elevation):
		stage_depth = elevation - self.start_stage_elevation
		if stage_depth >= 0:
			return self.width_at_stage(stage_depth)
		else:
			return 0

	def volume_at_elevation(self, elevation):
		stage_depth = elevation - self.start_stage_elevation
		if stage_depth >= 0:
			return self.volume_at_stage(stage_depth)
		else:
			return 0

	def set_len_and_width(self, volume = None, depth = None):
		len_to_width = self.len_to_width
		
		if depth:
			z = depth
		else:
			z = self.max_depth

		if volume:
			volume = volume
		else:
			volume = self.volume_max
		

		slope_x_1 = self.slope_width_1
		slope_x_2 = self.slope_width_2
		slope_y_1 = self.slope_length_1
		slope_y_2 = self.slope_length_2
		length =	( -3 * z**2 * (len_to_width*slope_y_1 + len_to_width*slope_y_2 + slope_x_1 + slope_x_2) +
					 	math.sqrt(3) *
					 	math.sqrt( z * (	3 *len_to_width**2*slope_y_1**2*z**3 + 
											6 *len_to_width**2*slope_y_1*slope_y_2*z**3 + 
											3 *len_to_width**2*slope_y_2**2*z**3 - 
											10*len_to_width*slope_x_1*slope_y_1*z**3 - 
											10*len_to_width*slope_x_1*slope_y_2*z**3 - 
											10*len_to_width*slope_x_2*slope_y_1*z**3 - 
											10*len_to_width*slope_x_2*slope_y_2*z**3 + 
											48*len_to_width*volume + 
											3*slope_x_1**2*z**3 + 
											6*slope_x_1*slope_x_2*z**3 + 
											3*slope_x_2**2*z**3)
					 	)
					) / (12*z) 
		width = length / self.len_to_width

		self.set_bottom_length(length)
		self.set_bottom_width(width)
		self.set_max_depth(depth)
		self.compute_max_volume()

	

		


class Pipe(RDStorage, Base.RDCircle):
	def __init__(	self, 
					elevation, 				# Feet
					diameter, 				# Feet
					length, 				# Feet
					void_ratio = 0.33,		# unitless, typically 0.33 for Perf. CMP systems, 0.00 for non-Perf. CMP
					perforated = True):		
		super().__init__(elevation_bottom = elevation, diameter_ft = diameter)
		self.length = length
		self.perforated = perforated
		self.void_ratio_ag = void_ratio
		self.set_void_ratio_ag(void_ratio)

		

	def set_void_ratio_ag(self, void_ratio):
		if not self.perforated:
			self.void_ratio_ag = 0
		else:
			self.void_ratio_ag = void_ratio

	def volume_at_stage(self, stage_depth):
		pass




if __name__ == '__main__':
	
	pipe1 = Pipe(0, 1, 120)


	# Crude SSD output:
	p1 = Pond(143.26, 286.52, 10, 2,2,2,2)
	# p4 = Pond(len_to_width = 130/95,
	# 			depth = 6,
	# 			slope = 3,
	# 			volume = 100992)
	# p1 = p4
	inc = 10/90
	print('Stage\t', 'Area\t', 'Volume\t', 'Discharge')
	for i in range(0, 93):
		stage = i * inc
		print(round(stage, 3), '\t', int(p1.area_at_stage(stage)) , '\t', round(p1.volume_at_stage(stage)/43560, 4))
					
	
	p2 = Pond(
		bottom_length = 130, 
		bottom_width = 55, 
		depth = 6, 
		slope = 3)
	
	print('Bottom area:', p2.area_at_stage(0), '\nVolume at Riser Head:', p2.volume_at_stage(p2.z), 'cu ft',p2.volume_at_stage(p2.z)/ 43560)	
					
					
					

	p3 = Pond(
		bottom_length = 130, 
		bottom_width = 95, 
		depth = 6, 
		slope = 3)
	
	print('Bottom area:', p3.area_at_stage(0), '\nVolume at Riser Head:', p3.volume_at_stage(p3.z), 'cu ft',p3.volume_at_stage(p3.z)/ 43560)	
					

	p4 = Pond(len_to_width = 130/95,
				depth = 6,
				slope = 3,
				volume = 100992)
					
	print('Bottom area:', p4.area_at_stage(0), '\nVolume at Riser Head:', p4.volume_at_stage(p4.z), 'cu ft',p4.volume_at_stage(p4.z)/ 43560)	
					
					
	p5 = Pond(len_to_width = 1, depth = 6, volume = 10000, slope = 0)
	print(p5.stage_depth_with_volume(10001))
					
					