import numpy as np
import csv

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

# Optimal weights (mse = 12.43)
opt_weights = [[-0.16624908],
               [0.29196314],
               [0.17489167],
               [0.17762045],
               [-0.25446903],
               [0.97917508],
               [0.54413923],
               [-1.20076198],
               [1.83145519],
               [0.63318368],
               [0.67835166],
               [0.36697975],
               [-1.34589391]]

inputs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

with open("coeffs2.csv", 'r') as f1:
	reader1 = csv.reader(f1)

	for row in reader1:
		atm = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]), float(row[12])]
		inputs = np.vstack([inputs, atm])
	inputs = np.delete(inputs, 0, axis=0)

outputs = sigmoid(np.dot(inputs, opt_weights))

with open('atms2.csv') as fin, open('result2.csv', 'w') as fout:
		index = 0
		for line in iter(fin.readline, ''):
			fout.write(line.replace('\n', ', ' + str(outputs[index][0] * 100) + '\n'))
			index += 1

