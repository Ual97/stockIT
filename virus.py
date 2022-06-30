import requests

for i in range(1000):
    a = requests.get('https://techual.tech')
    print(a.status_code)
    print(a.text)
    print(i)