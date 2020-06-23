import requests, time, csv, random, json, lxml
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def write_csv(data):
    with open('hotels.csv', 'a') as f:
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
    ads = soup.find('div', class_='view-content').find_all_next('div', class_='hotel-list-item without-dates')
    #print(ads)
    for ad in ads:
        try:
            adress = ad.find('span', class_='address').text.strip()
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
    url_gen = 'https://planetofhotels.com/searchresults/42050?'
    page_part = 'page='
    url_end = 'f%5B0%5D=stars%3A3.0&f%5B1%5D=stars%3A4.0&f%5B2%5D=stars%3A5.0&f%5B3%5D=stars%3A2.0&f%5B4%5D=hotel_type%3A14'

    html = get_html(url_gen + url_end)
    get_page_data(html)
    num = number_of_pages(url_gen + url_end)
    for i in range(2, num + 1):
        html = get_html(url_gen + page_part + str(i) + '&' + url_end)
        get_page_data(html)

if __name__ == '__main__':
    main()
