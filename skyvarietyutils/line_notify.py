import requests, json
import urllib.parse

def notify(token, message):
  url = 'https://notify-api.line.me/api/notify'

  msg = urllib.parse.urlencode({'message':message})
  LINE_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer '+token
  }
  session = requests.Session()
  a = session.post(url, headers=LINE_HEADERS, data=msg)
  print(a.text)
