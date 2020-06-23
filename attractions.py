import requests, time, csv, random, json, lxml
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def write_csv(data):
    with open('attractions.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['adress'],
                         data['index1'],
                         data['index2']))

def number_of_pages(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    strr = soup.find('div', class_='searchresults-title-inner').text.strip()
    i = 0
    num = ''
    while i < len(strr):
        if strr[i].isdigit():
            num += strr[i]
        i += 1
    num = int(num)
    if num/50 != 0:
        return (int(num) // 50) + 1
    return int(num) // 50

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
    ads = soup.find('div', class_='td-paragraph-padding-1').find_all_next('ul')[2:-1]
    for ad in ads:
        try:
            adress = ad.find('li').text.strip()
            adress = adress[7:]
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
    url_gen = 'https://hi-travelly.ru/what-to-see/dostoprimechatelnosty-moskvy.html'

    html = get_html(url_gen)
    get_page_data(html)

if __name__ == '__main__':
    main()
