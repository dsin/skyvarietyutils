import skyvarietyutils, json

class VkSDK:
  def __init__(self, client_id, access_token):
    self.api_url = 'https://api.vk.com/method'
    self.version = '5.21'
    self.client_id = client_id
    self.access_token = access_token

  def vk_get(self, uri, args):
    args['access_token'] = self.access_token
    args['v'] = self.version
    return json.loads(skyvarietyutils.http.get('%s/%s' % (self.api_url, uri), args).read())

  def vk_post(self, uri, args):
    args['access_token'] = self.access_token
    args['v'] = self.version
    return json.loads(skyvarietyutils.http.post('%s/%s' % (self.api_url, uri), args).read())

  # scope ref : https://vk.com/dev/permissions
  def get_authorization_url(self, scope):
    return 'https://oauth.vk.com/authorize?client_id=%s&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=%s&response_type=token&v=%s'  % (
      self.client_id,
      scope,
      self.version,
    )

  # Uploading Photos on User Wall : https://vk.com/dev/upload_files?f=2.%20Uploading%20Photos%20on%20User%20Wall
  def upload_files(self, image_urls, caption):
    save_wall_photo_responses = []
    for image_url in image_urls:
      upload_url = (self.get_wall_upload_server())['response']['upload_url']
      print('[upload_url] %s' % upload_url)

      picBinary = skyvarietyutils.http.load_image_binary(image_url).read()
      upload_response = self.post_file(upload_url, picBinary).json()
      print('[upload response]')
      print(upload_response)

      save_wall_photo_response = self.save_wall_photo(upload_response, caption)['response']
      print('[save wall photo]')
      print(save_wall_photo_response)
      save_wall_photo_responses = save_wall_photo_responses + save_wall_photo_response
    return save_wall_photo_responses

  def get_wall_upload_server(self):
    args = {
      # 'group_id': ''
    }
    return self.vk_get('photos.getWallUploadServer', args)

  def post_file(self, url, content):
    return skyvarietyutils.http.post_file(url, content, 'photo', 'whatever.png')

  def save_wall_photo(self, upload_response, caption=''):
    args = {
      'server': upload_response['server'],
      'photo': upload_response['photo'],
      'hash': upload_response['hash'],
    }
    if caption :
      args['caption'] = caption
    return self.vk_get('photos.saveWallPhoto', args)

  def format_wall_post_attachments_photo(self, save_wall_photo_responses):
    return list(map(lambda save_wall_photo_response: 'photo%s_%s' % (save_wall_photo_response['owner_id'], save_wall_photo_response['id']), save_wall_photo_responses))

  # should be post from a standalone app
  # https://vk.com/dev/publications
  # parameter references : https://vk.com/dev/wall.post?params[friends_only]=0&params[from_group]=0&params[message]=New%20post%20on%20group%20wall%20via%20API.console.&params[services]=twitter&params[signed]=0&params[mark_as_ads]=0&params[close_comments]=0&params[mute_notifications]=0&params[v]=5.124
  def wall_post(self, message, attachments=[]):
    args = {
      #'owner_id': -1,
      'message': message,
      'attachments': ','.join(attachments),
    }
    return self.vk_get('wall.post', args)
