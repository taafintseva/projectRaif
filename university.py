import requests, time, csv, random, json
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('university.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['adress'],
                         data['index1'],
                         data['index2']))

def transformAdress(str):
    i = 0
    while str[i].isdigit() == False:
        i += 1
    return str[i] + str.partition(str[i])[2]

def transformIndex(str):
    if str:
        i = 0
        a = ''
        while str[i] != ' ':
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

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('ul', class_='colleges').find_all_next('li')
    for ad in ads:
        try:
            adress = transformAdress(ad.text.strip())
            print(adress)
            yandexApi = adress.replace(' ', '+')
            urlYandex = 'https://geocode-maps.yandex.ru/1.x/?apikey=5d4ae0bb-26ef-4563-b112-e98b056b6c40&geocode=' + yandexApi + '&format=json'
            response = (requests.get(urlYandex)).json()
            index = response.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', {})[0].get('GeoObject', {}).get('Point', {})['pos']
            index = transformIndex(index)
            print(index)
            data = {'adress': adress,
                    'index1': index[0],
                    'index2': index[1]}
            write_csv(data)

        except:
            adress = ' '
            index = ' '



def main():
    url_gen = 'https://eduscan.net/region/Москва'

    html = get_html(url_gen)
    get_page_data(html)


if __name__ == '__main__':
    main()
