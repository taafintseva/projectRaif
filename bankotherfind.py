import csv
import requests

def transformIndex(str):
    if str:
        i = 0
        a = ''
        while (str[i] != ' '):
            a += str[i]
            i += 1
        a = float(a)
        i += 1
        b = ''
        while (i < len(str)):
            b += str[i]
            i += 1
        b = float(b)
    return [b, a]


def csv_dict_reader(f):

    with open('bankother.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
         row = ' '.join(line)
         yandexApi = row.replace(' ', '+')
         urlYandex = 'https://geocode-maps.yandex.ru/1.x/?apikey=5d4ae0bb-26ef-4563-b112-e98b056b6c40&geocode=' + yandexApi + '&format=json'
         response = (requests.get(urlYandex)).json()
         index = response.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', {})[0].get('GeoObject', {}).get('Point', {})['pos']
         index = transformIndex(index)
         write_csv(index)


def write_csv(index):
    with open('bankotherfind.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(index)

if __name__ == "__main__":
    with open("bankother.csv") as f:
        csv_dict_reader(f)
