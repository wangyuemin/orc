import requests

res = requests.post('http://120.92.51.44:8080/myweb/', data={'a': 3, 'b': 4})
print(res.text)
