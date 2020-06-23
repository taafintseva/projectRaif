import requests, time, csv, random, json
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('cian.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['adress'],
                         data['price'],
                         data['index1'],
                         data['index2']))


def number_of_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    str1 = soup.find('div', class_='_93444fe79c--totalOffers--22-FL')
    if str1:
        str2 = str1.text.replace(' ', '')
        i = 0
        num = ''
        while (str2[i]).isdigit():
            num += str2[i]
            i += 1
        num = int(num) / 1500
        return int(num)
    else:
        return 0

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
    ads = soup.find('div', class_='_93444fe79c--wrapper--E9jWb').find_all_next('div', class_='_93444fe79c--card--_yguQ')

    for ad in ads:
        try:
            adress = ad.find('div', class_='c6e8ba5398--address-links--1tfGW').text.strip()
            print(adress)
            yandexApi = adress.replace(' ', '+')
            urlYandex = 'https://geocode-maps.yandex.ru/1.x/?apikey=5d4ae0bb-26ef-4563-b112-e98b056b6c40&geocode=' + yandexApi + '&format=json'
            response = (requests.get(urlYandex)).json()
            index = response.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', {})[0].get('GeoObject', {}).get('Point', {})['pos']
            index = transformIndex(index)
            print(index)

            price = ad.find('div', class_='c6e8ba5398--term--3kvtJ').text.replace(' ', '')
            i = 0
            num = ''
            while (price[i]).isdigit():
                num = num + price[i]
                i += 1
            price = int(num)
            print(num)

            data = {'adress': adress,
                    'price': price,
                    'index1': index[0],
                    'index2': index[1]}
            write_csv(data)

        except:
            price = ' '
            adress = ' '
            index = ' '


def main():
    base_url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&'
    page_part = 'p='
    city_part = '&region=1'

    url = base_url + page_part + str(1) + city_part
    num = int(number_of_pages(get_html(url)))
    if num == 0:
        return -1

    for i in range(1, num):
        url_gen = base_url + page_part + str(i) + city_part
        html = get_html(url_gen)
        get_page_data(html)
        time.sleep(random.randint(2, 59))


if __name__ == '__main__':
    main()

