

import csv
from pathlib import Path
data_folder = Path.cwd().parent / 'data' 

# temp_csv = Path.cwd() / 'data' / 'test.csv'
# excel_csv = temp_csv.parent / 'Test_Excel.csv'

K_values_csv = data_folder / 'K-Values.csv'
kvd = dict()

with open(str(K_values_csv), newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    probabilities = dict()

    for row in reader:
    	kvd[row['P']] = row

    print(kvd['0.5000']['0.0'])
    	# print(row['P'])
    	# probabilities['P'] = row['P']
    	# for key in row.keys():

        # print(row['First Name'], row['Last Name'], 'is:', row['Age'], 'years old')




_outlier_K_values = {
	10:2.036,
	11:2.088,
	12:2.134,
	13:2.175,
	14:2.213,
	15:2.247,
	16:2.279,
	17:2.309,
	18:2.335,
	19:2.361,
	20:2.385,
	21:2.408,
	22:2.429,
	23:2.448,
	24:2.467,
	25:2.486,
	26:2.502,
	27:2.519,
	28:2.534,
	29:2.549,
	30:2.563,
	31:2.577,
	32:2.591,
	33:2.604,
	34:2.616,
	35:2.628,
	36:2.639,
	37:2.65,
	38:2.661,
	39:2.671,
	40:2.682,
	41:2.692,
	42:2.7,
	43:2.71,
	44:2.719,
	45:2.727,
	46:2.736,
	47:2.744,
	48:2.753,
	49:2.76,
	50:2.768,
	51:2.775,
	52:2.783,
	53:2.79,
	54:2.798,
	55:2.804,
	56:2.811,
	57:2.818,
	58:2.824,
	59:2.831,
	60:2.837,
	61:2.842,
	62:2.849,
	63:2.854,
	64:2.86,
	65:2.866,
	66:2.871,
	67:2.877,
	68:2.883,
	69:2.888,
	70:2.893,
	71:2.897,
	72:2.903,
	73:2.908,
	74:2.912,
	75:2.917,
	76:2.922,
	77:2.927,
	78:2.931,
	79:2.935,
	80:2.94,
	81:2.945,
	82:2.949,
	83:2.953,
	84:2.957,
	85:2.961,
	86:2.966,
	87:2.97,
	88:2.973,
	89:2.977,
	90:2.981,
	91:2.984,
	92:2.989,
	93:2.993,
	94:2.996,
	95:3,
	96:3.003,
	97:3.006,
	98:3.011,
	99:3.014,
	100:3.017,
	101:3.021,
	102:3.024,
	103:3.027,
	104:3.03,
	105:3.033,
	106:3.037,
	107:3.04,
	108:3.043,
	109:3.046,
	110:3.049,
	111:3.052,
	112:3.055,
	113:3.058,
	114:3.061,
	115:3.064,
	116:3.067,
	117:3.07,
	118:3.073,
	119:3.075,
	120:3.078,
	121:3.081,
	122:3.083,
	123:3.086,
	124:3.089,
	125:3.092,
	126:3.095,
	127:3.097,
	128:3.1,
	129:3.102,
	130:3.104,
	131:3.107,
	132:3.109,
	133:3.112,
	134:3.114,
	135:3.116,
	136:3.119,
	137:3.122,
	138:3.124,
	139:3.126,
	140:3.129,
	141:3.131,
	142:3.133,
	143:3.135,
	144:3.138,
	145:3.14,
	146:3.142,
	147:3.144,
	148:3.146,
	149:3.148
}

def outlier_10_percent(sample_size):
	'''
	input: 	Integer number of water years >= 10
	output: K_N corresponding to one-sided 10% significance level
	'''

	if sample_size < 10:
		raise Exception('Too few years on record for K_N (Appx4-#17B)')
		return _outlier_K_values[10]
	elif sample_size > 149:
		return _outlier_K_values[149]


	return _outlier_K_values[sample_size]




def for_weighted_skew_and_return_period(skew, return_period):
	skew = str(round(skew, 1))
	probability = str(round(1 / return_period, 5))
	zeros_needed = 6 - len(probability)
	probability = probability + '0' * zeros_needed

	return float(kvd[probability][skew])

def K(weighted_skew = None, return_period = None):
	return for_weighted_skew_and_return_period(weighted_skew, return_period)



if __name__ == "__main__":
	print(_outlier_K_values[148])














