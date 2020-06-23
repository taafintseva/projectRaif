import numpy as np
import csv
import os

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

training_inputs = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
training = list()
training_outputs = np.array(np.zeros(106))

with open("coeffs1.csv", 'r') as f1:
	reader1 = csv.reader(f1)

	for row in reader1:
		atm = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), float(row[11]), float(row[12])]
		training_inputs = np.vstack([training_inputs, atm])
	training_inputs = np.delete(training_inputs, 0, axis=0)
	#print(training_inputs1)

with open("atms1.csv", 'r') as f2:
	reader2 = csv.reader(f2)

	for row in reader2:
		coeff = float(row[4]) / 100
		training.append(coeff)
	training_outputs = np.vstack([training_outputs, training])
	training_outputs = np.delete(training_outputs, 0, axis=0)
	training_outputs = training_outputs.T
	#print(training_outputs1)

mse = 20

while mse > 10:

	synaptic_weights = np.random.random((13, 1))
	print("Веса до обучения:")
	print(synaptic_weights)


	# Backpropagation method
	for i in range(900000):
		input_layer = training_inputs
		outputs = sigmoid(np.dot(input_layer, synaptic_weights))

		err = training_outputs - outputs
		adjustment = np.dot(input_layer.T, err * (outputs * (1 - outputs)))

		synaptic_weights += adjustment

	print("Веса после обучения:")
	print(synaptic_weights)

	print("Результат после обучения:")
	print(outputs)


	with open('atms1.csv') as fin, open('result.csv', 'w') as fout:
		index = 0
		for line in iter(fin.readline, ''):
			fout.write(line.replace('\n', ', ' + str(outputs[index][0] * 100) + '\n'))
			index += 1

	mean_of_error = list()

	with open("result.csv", 'r') as f3:
		reader3 = csv.reader(f3)

		for row in reader3:
			coef = np.abs(float(row[4]) - float(row[5]))
			mean_of_error.append(coef)
		mse = np.mean(mean_of_error)
		print(mse)

	os.remove("result.csv")



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


