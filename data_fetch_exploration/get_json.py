import requests

URL = "https://s3.amazonaws.com/assets.mailcharts.com/~emails:ea084f6d-0d2e-35fa-8606-b9f1f0b00b79.json"

resolve = requests.get(URL)
print(resolve.json().keys())
print(resolve.json()['subject'])
print(resolve.json()['body-html'])

