import urllib.parse
import urllib.request

def post(url, query_args={}, headers={}):
  data = urllib.parse.urlencode(query_args).encode('utf-8')
  req = urllib.request.Request(url, data, headers)
  response = urllib.request.urlopen(req)
  # print(response.read())

  return response

def get_client_ip(http_x_forwarded_for, remote_addr):
  x_forwarded_for = http_x_forwarded_for
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = remote_addr
  return ip
