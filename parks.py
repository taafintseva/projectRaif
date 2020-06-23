import requests, time, csv, random, json, quote
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('parks.csv', 'a') as f:
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
    ads = soup.find('div', class_='content').find_all_next('div', class_='content_view')
    for ad in ads[1:-1]:
        try:
            adress = ad.find('a', class_='media-preview_description').text.strip()
            print(adress)
            yandexApi = adress.replace(' ', '+')
            urlYandex = 'https://geocode-maps.yandex.ru/1.x/?apikey=5d4ae0bb-26ef-4563-b112-e98b056b6c40&geocode=' + yandexApi + '&format=json'
            response = (requests.get(urlYandex)).json()
            try:
                index = response.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', {})[0].get('GeoObject', {}).get('Point', {})['pos']
            except:
                adress = ad.find('a', class_='media-preview_name').text.strip()
                print(adress)
                yandexApi = adress.replace(' ', '+')
                urlYandex = 'https://geocode-maps.yandex.ru/1.x/?apikey=5d4ae0bb-26ef-4563-b112-e98b056b6c40&geocode=' + yandexApi + '&format=json'
                response = (requests.get(urlYandex)).json()
                index = response.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', {})[0].get('GeoObject', {}).get('Point', {})['pos']
            index = transformIndex(index)
            print(index)

        except:
            adress = ' '
            index = ' '

        data = {'adress': adress,
                'index1': index[0],
                'index2': index[1]}
        write_csv(data)


def main():
    url_gen = 'https://www.2do2go.ru/articles/7691/25-parkov-moskvy-gde-pogulyat-v-vykhodnye'
    html = get_html(url_gen)
    get_page_data(html)

if __name__ == '__main__':
    main()
