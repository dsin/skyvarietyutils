import urllib.parse
import urllib.request

def post(url, query_args={}, headers={}):
  data = urllib.parse.urlencode(query_args).encode('utf-8')
  req = urllib.request.Request(url, data, headers)
  response = urllib.request.urlopen(req)
  # print(response.read())

  return response
