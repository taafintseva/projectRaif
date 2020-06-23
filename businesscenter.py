import requests, time, csv, random, json
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('businesscenter.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['adress'],
                         data['index1'],
                         data['index2']))

def number_of_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    str1 = soup.find('div', class_='col col-md-auto active').text.strip()
    i = 0
    num = ''
    while (str1[i]).isdigit():
        num += str1[i]
        i += 1
    num = int(num) / 30
    if (int(num) % 30) != 0:
        num += 1
    return int(num)

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
    ads = soup.find('ul', class_='listNone').find_all_next('li', class_='cardObject combinedCard rentSaleCard')
    for ad in ads:
        try:
            adress = ad.find('span', class_='openMapCard linkDashed imitation-link').text.strip()
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
    base_url = 'https://amo.ru/bc'
    page_part = '/page-'

    num = number_of_pages(get_html(base_url))
    print(num)
    if num == 0:
        return -1

    for i in range(1, num+1):
        if i == 1:
            url_gen = base_url
        else:
            url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)
        time.sleep(random.randint(2, 20))


if __name__ == '__main__':
    main()
