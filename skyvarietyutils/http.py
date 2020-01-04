import urllib

# url : 'http://localhost:8080/'
# query_args : { 'q':'query string', 'foo':'bar' }
# headers : {'User-agent', 'PyMOTW (http://www.doughellmann.com/PyMOTW/)'}
def post(url, query_args, headers={}):
  data = urllib.parse.urlencode(query_args).encode('utf-8')
  req = urllib.request.Request(url, data, headers)
  response = urllib.request.urlopen(req)
  # print(response.read())

  return response
