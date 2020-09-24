import urllib.parse, urllib.request, requests

def get(url, args, headers={}):
  if args and len(args) != 0:
    url = url + '?' + urllib.parse.urlencode(args)

  # If you do not pass the data argument, urllib uses a GET request.
  req = urllib.request.Request(url, None, headers)
  response = urllib.request.urlopen(req)

  return response

def post(url, query_args={}, headers={}):
  data = urllib.parse.urlencode(query_args).encode('utf-8')

  req = urllib.request.Request(url, data, headers)
  response = urllib.request.urlopen(req)
  # print(response.read())

  return response

def post_file(url, content, parameter_name, file_name, headers={}):
  files = {parameter_name: (file_name, content)}
  return requests.post(url, data={}, files=files, headers=headers)

def get_client_ip(http_x_forwarded_for, remote_addr):
  x_forwarded_for = http_x_forwarded_for
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = remote_addr
  return ip

def load_image_binary(url):
    response = get(url, {},  {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'
    })
    # https://stackoverflow.com/questions/1308584/is-it-possible-to-peek-at-the-data-in-a-urllib2-response
    # response.read = lambda: picBinary
    return response
