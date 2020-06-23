import csv
from geopy.distance import geodesic


def calcCoeff(raif, filename, index1, index2):
    output = 0
    k = 0
    with open(filename, 'r') as f1:
        reader1 = csv.reader(f1)

        for row in reader1:
            other = (float(row[index1]), float(row[index2]))
            dist = int(geodesic(raif, other).kilometers)
            if dist <= 1.0:
                k += 1
                output += (1 - (dist / 1.0))
        if k != 0:
            print(output / k)
            a = output / k
        else:
            a = 0.0001
    return a

def calcCoeffCian(raif, filename):
    k = 0
    price = 0
    with open(filename, 'r') as f1:
        reader1 = csv.reader(f1)

        for row in reader1:
            other = (float(row[2]), float(row[3]))
            dist = int(geodesic(raif, other).kilometers)
            if dist <= 3.0:
                k += 1
                price += (float(row[1]) / 500000.0)
        if k != 0:
            print(price / k)
            a = price / k
        else:
            a = 0.0001
    return a

def write_csv(ans):
    with open('coeffs_n.csv', 'a') as f:
        for i in range(0, 12):
            f.write(str(ans[i]))
            f.write(str(','))
        f.write('\n')

def csv_dict_reader():
    ans = [1.0]*12
    with open('atms2.csv', 'r') as f:
        reader = csv.reader(f)

        for line in reader:
            raif = (float(line[0]), float(line[1]))

            ans[0] = calcCoeff(raif, 'bankotherfind.csv', 0, 1)
            ans[1] = calcCoeff(raif, 'bankraifind.csv', 0, 1)
            ans[2] = calcCoeff(raif, 'businesscenter.csv', 1, 2)
            ans[3] = calcCoeff(raif, 'metro.csv', 1, 2)
            ans[4] = calcCoeff(raif, 'shoppingmall.csv', 1, 2)
            ans[5] = calcCoeff(raif, 'university.csv', 1, 2)
            ans[6] = calcCoeff(raif, 'venues.csv', 1, 2)
            ans[7] = calcCoeffCian(raif, 'cian.csv')
            ans[8] = calcCoeff(raif, 'theatres.csv', 1, 2)
            ans[9] = calcCoeff(raif, 'attractions.csv', 1, 2)
            ans[10] = calcCoeff(raif, 'hotels.csv', 1, 2)
            ans[11] = calcCoeff(raif, 'parks.csv', 1, 2)
            write_csv(ans)

if __name__ == '__main__':
    csv_dict_reader()
    population = list()
    with open("population2.csv", 'r') as f2:
        reader2 = csv.reader(f2)

        for row in reader2:
            coeff = float(row[0])
            population.append(coeff)
    print(population)

    with open('coeffs_n.csv') as fin, open('coeffs2.csv', 'w') as fout:
        index = 0
        for line in iter(fin.readline, ''):
            fout.write(line.replace('\n', ', ' + str(population[index]) + '\n'))
            index += 1
