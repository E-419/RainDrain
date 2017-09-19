'''
This module defines all of the statistics required for stormwater analysis
'''


import math



import K_values
# import scipy
# import scipy.stats as st
# from scipy.stats import pearson3








def mean_squared_error(skew, N):
	'''
	Mean Squared Error, Eqn #6 (pg 13) of Bulletin #17B
		Input: skew value
	   return: MSE_skew
	'''

	A = None
	B = None
	abs_skew = abs(skew)
	
	# Set A
	if abs_skew <= 0.90:
		A = -0.33 + 0.08 * abs_skew
	elif abs_skew > 0.90:
		A = -0.52 + 0.30 * abs_skew

	# Set B
	if abs_skew <= 1.50:
		B = 0.94 - 0.26 * abs_skew
	elif abs_skew > 1.50:
		B = 0.55


	# Compute Mean Squared Error via Eqn. 6 (pg 13) of #17B
	MSE = 10**(A - B * math.log10(N/10))

	if __name__ == '__main__':
		print('A =', A, '\nB =', B, )
		print('MSE =', MSE, '\n')
	return MSE



# Log Pearson Type 3, Bulletin # 17B
class log_struct(object):
	class sum(object):
		def __init__(self):
			self.data = None
			self.squared = None
			self.cubed = None

	def __init__(self, raw_data, regional_skew = 0.0):
		'''
		raw_data input must be an iterable and should be sorted
		reqional_skew is a value taken from Plate I in Bulletin #17B 
			(third to the last page of the PDF)
		'''
		self.data = None 		# list()
		self.squared = list()
		self.cubed = list()
		self.sum = log_struct.sum()

		self.skew_general = regional_skew 	# From Plate I of #17B
		self.skew_general_MSE = 0.302 		# <-- Constant in the US


		# Contains Steps 1-2 of Example 1 in #17B:
		self.compute_log_data(raw_data)

		self.len = len(raw_data)
		self.mean = self._mean()
		self.std_dev = self._std_dev()
		self.skew = self._skew()

		self.outlier_high = None
		self.outlier_low = None
		self.set_outliers()

		self.skew_MSE = None
		self.set_skew_MSE()

		self.skew_weighted = None
		self.set_skew_weighted()

		self.freq = dict()
		self.set_freq()

	def set_freq(self):
		for return_period in [2,10,25,50,100]:
			K = K_values.K(return_period = return_period, weighted_skew = self.skew_weighted)
			self.freq[return_period] = self.mean + K * self.std_dev


	def set_skew_weighted(self):
		'''
		G_W = MSE_Gbar * G + MSE_G * Gbar / (MSE_Gbar + MSE_G)
		'''
		self.skew_weighted = (
			(self.skew_general_MSE * self.skew + self.skew_MSE * self.skew_general) /
			(self.skew_general_MSE + self.skew_MSE)
		)


	def set_skew_MSE(self):
		self.skew_MSE = mean_squared_error(self.skew, self.len)

	def set_outliers(self):
		K_N = K_values.outlier_10_percent(self.len)

		# self.set_high_outlier(K_N)
		# self.set_low_outlier(K_N)
		
		self.outlier_high = self.mean + K_N * self.std_dev
		self.outlier_low = self.mean - K_N * self.std_dev



	def compute_log_data(self, data):
		def log(data):
			log_data = list()
			for item in data:
				log_data.append(math.log10(item))
			return log_data
		def pow(data, pow):
			pow_dat = list()
			for item in data:
				pow_dat.append(item**pow)
			return pow_dat
		self.data = log(data)
		self.squared = pow(self.data, pow = 2)
		self.cubed = pow(self.data, pow = 3)
		self.compute_sums()
		
		

		
	def compute_sums(self):
		self.sum.data = self._sum_data()
		self.sum.squared = self._sum_squared()
		self.sum.cubed = self._sum_cubed()
	
	def _std_dev(self):
		# Equation 3b of 17B:
		# ((sum(X^2) - sum(X)^2/N) / (N-1))^0.5
		return ((self.sum.squared - (self.sum.data**2 / self.len)) / (self.len - 1))**0.5

	def _mean(self):
		# Equation 2 of 17B:
		# sum(X)/N
		return self.sum.data / self.len

	def _skew(self):
		# Equation 4b of 17B:
		# (N^2(sum(X^3)) - 3N(sum(X))(sum(X^2)) + 2(sum(X))^3) / (N(N-1)(N-2)S^3)
		# In terms of A, B, C, & D:
		# (A - B + C) / D
		A = self.len**2 * self.sum.cubed
		B = 3 * self.len * self.sum.data * self.sum.squared
		C = 2 * self.sum.data**3
		D = self.len * (self.len - 1) * (self.len - 2) * self.std_dev**3
		return (A - B + C) / D

	def _sum(self, data):
		tot = 0
		for item in data:
			tot += item
		return tot

	def _sum_data(self):
		return self._sum(self.data)

	def _sum_squared(self):
		return self._sum(self.squared)

	def _sum_cubed(self):
		return self._sum(self.cubed)



	@property
	def length(self):
		if data:
			return len(self.data)

class log_pearson_type_3_17b(object):

	def __init__(self, data, regional_skew = 0.6):
		'''
		data input must be an iterable and should be sorted
		reqional_skew is a value taken from Plate I in Bulletin #17B 
			(third to the last page of the PDF)
		'''
		self.data = list(data)
		self.size = len(data)

		# This does the heavy lifting:
		self.log = log_struct(data, regional_skew)

		self.freq = dict()
		self.set_freq()

	def set_freq(self):
		for key in self.log.freq.keys():
			self.freq[key] = 10**self.log.freq[key]




	
	
	




def sum(data):
	tot = 0
	for item in data:
		tot += item
	return tot

def log(data):
	'''
	data input must be an iterable and should be sorted
	'''
	log_data = list()
	for item in data:
		log_data.append(item)
	return log_data

def power(data, pow):
	pow_dat = list()
	for item in data:
		pow_dat.append(item**pow)
	return pow_dat

def mean(data):
	# X_bar = sum(X) / N
	return sum(data) / len(data)

def std_dev(data):
	# For whatever reason, this mutates the original list somehow...
#	X = data
	X = list()
	X_bar = mean(data)

	# X -> X - X_bar
	for item in data:
		# Found it... this should be a new list
#		X[i] = X[i] - X_bar
		X.append(item - X_bar)
	std_dev = ((sum(X))**2/(len(X) - 1))**0.5
	return std_dev

def skew(data):
	N = len(data)
	X_bar = mean(data)
	skw = (N * sum())
















if __name__ == '__main__':

	# Example 1, Fishkill Creek, in Bulletin 17B:
	years = [x for x in range(1945, 1969)]

	fishkill_creek_annual_peaks = [
	2290,
	1470,
	2220,
	2970,
	3020,

	1210,
	2490,
	3170,
	3220,
	1760,

	8800,
	8280,
	1310,
	2500,
	1960,

	2140,
	4340,
	3060,
	1780,
	1380,

	980,
	1040,
	1580,
	3630
	]


	fishkill_creek = log_pearson_type_3_17b(fishkill_creek_annual_peaks)
	print('mean:',fishkill_creek.log.mean, '\nstd_dev:', fishkill_creek.log.std_dev, '\nskew:', fishkill_creek.log.skew)
	print('\n',
		'High Outlier:', fishkill_creek.log.outlier_high, '-> {0} cfs'.format(10**fishkill_creek.log.outlier_high), '\n',
		' Low Outlier:', fishkill_creek.log.outlier_low,  '-> {0} cfs'.format(10**fishkill_creek.log.outlier_low ),
	)

	print('\n',
		'MSE_G:', 			fishkill_creek.log.skew_MSE,
		'\nWeighted Skew:',	fishkill_creek.log.skew_weighted,
		'\nK_Val:', K_values.K(weighted_skew = fishkill_creek.log.skew_weighted, return_period = 1/0.9999),
		'\nK_Val:', K_values.K(weighted_skew = fishkill_creek.log.skew_weighted, return_period = 5),
		'\nPeaks {}-yr:'.format(2), fishkill_creek.freq[2]
		# '\nK_Val:', K_values.for_weighted_skew_and_return_period(fishkill_creek.log.skew_weighted, 100)
	)

	# annual_peaks.sort()
	# std = std_dev(annual_peaks)
	
	# log_annual_peaks = list()

	# for peak in annual_peaks:
	# 	log_annual_peaks.append(math.log10(peak))
	
	# log_annual_peaks.sort()

	# # This skew is incorrect for this application and should be replaced by the 17B skew forumae
	# skew = scipy.stats.skew(log_annual_peaks)
	# print('Skew:', skew)
	# testpdf = pearson3.pdf(log_annual_peaks, skew)
	# testcdf = pearson3.cdf(log_annual_peaks, skew)

	# print(testpdf)
	# tp = list()
	# for item in testpdf:
	# 	tp.append(10**item)
		
	# print(tp)
		

	# # import matplotlib as mpl
	# # from matplotlib import pyplot as plt
