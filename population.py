import requests, csv, time

url = "https://api.geointellect.com/poptools/pop_radius"

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'ccode': 'user127898',
  'key': '75276e76-c1f6-44ad-9db7-9b65ed48c081'
}

with open('atms1.csv', 'r') as f:
        reader = csv.reader(f)

        for line in reader:
            raif = (float(line[0]), float(line[1]))

            payload = 'xlon=' + str(raif[1])+'&ylat=' + str(raif[0]) + '&size=50'

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text.encode('utf8'))
            time.sleep(20)
