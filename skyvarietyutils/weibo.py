# -*- coding: utf-8 -*-
from include.sinaweibopy.snspy import APIClient
from include.sinaweibopy.snspy import SinaWeiboMixin      # suppose you are using Twitter
from include.sinaweibopy.snspy import APIError

# https://gwu-libraries.github.io/sfm-ui/posts/2016-04-26-weibo-api-guide
# https://github.com/michaelliao/sinaweibopy

# API references : https://open.weibo.com/apps/570163951/privilege, https://open.weibo.com/wiki/API%E6%96%87%E6%A1%A3/en
# App Lists : https://open.weibo.com/webmaster

class Weibo:
  def __init__(self, app_key, app_secret, callback_url, access_token=None):
    self.APP_KEY = app_key
    self.APP_SECRET = app_secret
    self.CALLBACK_URL = callback_url

    if access_token:
      self.client = APIClient(SinaWeiboMixin,
                   app_key=self.APP_KEY,
                   app_secret=self.APP_SECRET,
                   redirect_uri=self.CALLBACK_URL,
                   access_token=access_token) # , expires=self.EXPIRES_TIME
      self.access_token = access_token
    else:
      self.client = APIClient(SinaWeiboMixin,
        app_key=self.APP_KEY,
        app_secret=self.APP_SECRET,
        redirect_uri=self.CALLBACK_URL)

  def login_url(self):
    return self.client.get_authorize_url()

  def callback_url_verification(self, code):
    r = self.client.request_access_token(code)
    access_token = r.access_token  # access token，e.g., abc123xyz456
    expires = r.expires      # token expires time, UNIX timestamp, e.g., 1384826449.252 (10:01 am, 19 Nov 2013, UTC+8:00)
    # NOTE: you should store the access_token for later use.

    return access_token

  def statuses_update(self, message):
    try :
      args = {
        'status': message
      }
      self.client.statuses.update.post(**args)

      return {'status': 'success'}
    except APIError as e:
      return {'status': 'error', 'error_code': e.error_code, 'error': e.error, 'request': e.request}

  def statuses_share(self, message, picBinary=None): # u'test'
    try :
      args = {
        'status': message
      }
      if picBinary:
        args['pic'] = picBinary
      self.client.statuses.share.post(**args)
      ##import requests

      ### ref : https://www.itengli.com/python_weibo/
      ##发表图文微博的接口
      ##url = 'https://api.weibo.com/2/statuses/share.json' #
      ##构建文本类POST参数
      ##payload={
      ##  'access_token': self.access_token,
      ##  'status': message
      ##}
      ###构建二进制multipart/form-data编码的参数
      ##files={
      ##  'pic': picBinary
      ##}
      ###POST请求，发表微博
      ##with requests.post(url,timeout=50, data=payload, files=files, stream=True) as r:
      ## print(r)
      ##resp = r.json()
      ##if hasattr(resp, 'error_code'):
      ##  raise APIError(resp.error_code, resp.get('error', ''), resp.get('request', ''))
      return {'status': 'success'}
    except APIError as e:
      return {'status': 'error', 'error_code': e.error_code, 'error': e.error, 'request': e.request}
