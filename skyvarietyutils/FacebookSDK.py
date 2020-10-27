import facebook, json, urllib
import skyvarietyutils

# get user access token
# from https://developers.facebook.com/tools/explorer/

# debug access token + click extend user access token
# https://developers.facebook.com/tools/debug/accesstoken

# get page access token
# curl -i -X GET "https://graph.facebook.com/{page-id}?fields=access_token&access_token={user-access-token}"

# ref : https://medium.com/@yasithlokuge/how-to-generate-a-never-expiring-facebook-page-access-token-24ac5c1a95f1

class FacebookSDK:
  def __init__(self, access_token, app_id=None, app_secret=None, callback_url=''):
    self.APP_ID = app_id
    self.APP_SECRET = app_secret
    self.CALLBACK_URL = callback_url

    if access_token:
      self.graph = facebook.GraphAPI(access_token)
    else :
      self.graph = facebook.GraphAPI()

  def login(self, scopes):
    return self.graph.get_auth_url(self.APP_ID, self.CALLBACK_URL, scopes)

  def callback_url_verification(self, code):
    args = {
      'client_id': self.APP_ID,
      'redirect_uri': self.CALLBACK_URL,
      'client_secret': self.APP_SECRET,
      'code': code,
    }
    access_token = None
    try:
      response = json.loads(skyvarietyutils.http.get('https://graph.facebook.com/oauth/access_token', args).read())
      access_token = response['access_token']
    except urllib.error.HTTPError as err:
      print(err.read())
    return access_token

  def get_long_lived_user_access_token(self, user_access_token):
    args = {
      'client_id': self.APP_ID,
      'client_secret': self.APP_SECRET,
      'grant_type': 'fb_exchange_token',
      'fb_exchange_token': user_access_token,
    }
    response = json.loads(skyvarietyutils.http.get('https://graph.facebook.com/oauth/access_token', args).read())
    access_token = response['access_token']
    return access_token

  def me(self, fields):
    return self.graph.get_object('me', fields=fields)

  # def get_page_access_token(self, page_id):
  #   return self.graph.get_object('page')

  # # https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing/
  # def get_long_lived_page_access_token(self, user_id, long_lived_user_access_token):
  #   args = {
  #     'access_token': long_lived_user_access_token
  #   }
  #   try:
  #     response = json.loads(skyvarietyutils.http.get('https://graph.facebook.com/'+user_id+'/accounts', args).read())
  #     data = response['data']
  #   except urllib.error.HTTPError as err:
  #     print(err.read())
  #   return data

  def postImages(self, *args, **kwargs):
    page_id = args[0]

    link = kwargs['link']
    message = kwargs['message']
    scheduled_publish_time = kwargs['scheduled_publish_time']
    image_urls = kwargs['image_urls']

    # https://developers.facebook.com/docs/graph-api/photo-uploads#upload
    if len(image_urls) == 1:
      self.upload(page_id,
        url=image_urls[0],
        caption=message,
        scheduled_publish_time=scheduled_publish_time,
      )
    else:
      postKwargs = {
        'message': message,
        'scheduled_publish_time': scheduled_publish_time,
      }

      if len(image_urls) > 1:
          media_ids = self.bulk_upload(page_id, image_urls, message)
          if len(media_ids) > 0:
            postKwargs['attached_media'] = json.dumps(media_ids)
          else :
            postKwargs['link'] = link
      else :
        postKwargs['link'] = link

      self.post(page_id,
        **postKwargs,
      )

  def post(self, *args, **kwargs):
    kwargs['connection_name'] = 'feed'
    if 'scheduled_publish_time' in kwargs:
      kwargs['published'] = False

    return self.graph.put_object(
      *args,
      **kwargs
    )

  def upload(self, *args, **kwargs):
    kwargs['connection_name'] = 'photos'
    if 'scheduled_publish_time' in kwargs:
      kwargs['published'] = False

    return self.graph.put_object(
      *args,
      **kwargs
    )

  def bulk_upload(self, page_id, image_urls, caption):
    media_ids = []
    for image in image_urls:
      uploadResult = self.upload(page_id,
        url=image,
        caption=caption,
        published=False,
      )
      media_ids.append({'media_fbid': uploadResult['id']})
    return media_ids
