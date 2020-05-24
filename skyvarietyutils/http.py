import urllib.parse
import urllib.request
import urllib, urllib2

def get(url, args, headers={}): # {"Accept" : "text/html"}
        if args and len(args) != 0:
            url = url+'?%s' % urllib.urlencode(args)
        request = urllib2.Request(url) # , headers=headers
        for header_key, header_value in headers.iteritems():
            if header_key != '' and header_value != '':
                request.add_header(header_key, header_value)
        content = ''
        response = None
        error = None
        try:
            response = urllib2.urlopen(request, timeout=300)
        except urllib2.HTTPError as e:
            logging.info("HTTPError %s, URL %s" %(e.code, url))
            error = {'code': e.code}
            if e.code == 404:
                # do something...
                pass
            else:
                # ...
                pass
        except urllib2.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            # ...
            logging.info('URL Error')
            pass
        else:
            # 200
            content = response.read()
        return (content, response, error)

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

def load_image_binary(url):
    picBinary, response, error = get(url, {},  {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'})
    # https://stackoverflow.com/questions/1308584/is-it-possible-to-peek-at-the-data-in-a-urllib2-response
    response.read = lambda: picBinary
    return response
