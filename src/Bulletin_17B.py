'''
This module defines all of the statistics required for stormwater analysis 
as prescribed in Bulletin 17B available at:
	https://water.usgs.gov/osw/bulletin17b/dl_flow.pdf

Equations listed in that document are defined here as functions with names that
match equation references the equation references.
'''

import math

import K_values

# X, X_sq, X_cu, X_sum, X_sq_sum, X_cu_sum, X_bar
# G, G_bar, MSE_G, MSE_G_bar
# K, S, N

def equation_1(X_bar, K, S):
	'''	
	Arguments: X_bar, K, S
	X_bar is the mean of the data
		-> For this purpose it is the mean of the log(data)
	K is the factor associated with the skew of the data and exceedance
		probability from Appendix 3
	S is the standard deviation of the data 
		-> For this purpose it is the standard deviation of the log(data)

	From pg. 9 of Bulletin #17B:
		Log(Q) = X_bar + K * S
	'''
	return X_bar + K * S

def equation_2(X_sum = None, N = None):
	'''
	Arguments: X_sum, N
	X is a list of the data values
		-> For this purpose it is a list of the log(data) values
	X_sum is the sum of the data values
		-> For this purpose it is the sum of the log(data) values
	N is the number of data points in the set
		-> This is the record length in years typically
		
	'''
	if X_sum and N:
		return X_sum/N

def equation_3a(X = None, X_bar = None, N = None):
	'''
	Arguments: X, X_bar, N
	X is a list of the data values
		-> For this purpose it is a list of the log(data) values
	X_bar is the mean of the data
		-> For this purpose it is the mean of the log(data)
	N is the number of data points in the set
		-> This is the record length in years typically
	'''
	if X and X_bar and N:
		numerator = 0
		for data in X:
			numerator += (data - X_bar)**2
		return math.sqrt((numerator / (N - 1)))


	

def equation_3b(X = None, N = None):
	'''
	Arguments: X, X_bar, N
	X is a list of the data values
		-> For this purpose it is a list of the log(data) values
	N is the number of data points in the set
		-> This is the record length in years typically
	'''
	if X and N:
		# This is the 1st term in the numerator, sum( log(data)^2 )
		numerator_1 = 0
		for i in X:
			numerator_1 += i**2

		# This is half of the second term in the numerator, sum( log(data) )^2
		numerator_2 = 0
		for i in X:
			numerator_2 += i
		numerator_2 = numerator_2**2

		return math.sqrt(((numerator_1 - numerator_2/N) / (N - 1)))


def equation_4a(X = None, X_bar = None, S = None, N = None):
	if X and X_bar and S and N:
		
		sumDeltaCubed = 
	

def equation_4b():
	pass

def equation_5(G, G_bar, MSE_G, MSE_G_bar):
	'''MSE_Gbar'''
	pass

def equation_6(skew, N):
	'''
	Mean Squared Error, pg. 13
		Input: skew value, number of events
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

def equation_7(X_bar, K_N, S):
	'''
	High outlier detection, pg. 17
	'''
	pass

def equation_8a():
	'''
	Low outlier detection, pg. 18
	'''
	pass

def equation_8b():
	'''
	Low outlier detection, pg. 18
	'''
	pass





if __name__ == "__main__":
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

	log_vals = list()
	for i in fishkill_creek_annual_peaks:
		log_vals.append(math.log10(i))

	Xbar = equation_2(sum(log_vals),len(log_vals))
	print(Xbar)
	print(equation_3a(log_vals, Xbar, len(log_vals)))
	print(equation_3b(log_vals, len(log_vals)))
