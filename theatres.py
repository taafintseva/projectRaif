import requests, time, csv, random, json
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('theatres.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['adress'],
                         data['index1'],
                         data['index2']))

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
    ads = soup.find('div', class_='post-list-big').find_all_next('article', class_='post-list-item')
    for ad in ads:
        try:
            adress = ad.find('span', class_='addressItem addressItem--single').text.strip()
            adress = adress.partition(adress[1])[2]
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
            continue

def main():
    url_gen1 = 'https://kudago.com/msk/list/luchshie-dramaticheskie-teatry-moskvy/'
    html1 = get_html(url_gen1)
    get_page_data(html1)

if __name__ == '__main__':
    main()
