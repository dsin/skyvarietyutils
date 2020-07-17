from twitter import Twitter, OAuth

import skyvarietyutils

class TwitterSDK:
  def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.access_token = access_token
    self.access_token_secret = access_token_secret

    auth=OAuth(self.access_token, self.access_token_secret, self.consumer_key, self.consumer_secret)
    self.t = Twitter(auth=auth)

  def uploadMedias(self, image_urls):
    t_upload = Twitter(domain='upload.twitter.com',
    auth = OAuth(self.access_token, self.access_token_secret, self.consumer_key, self.consumer_secret))
    media_ids = []
    for image_url in image_urls:
      picBinary = skyvarietyutils.http.load_image_binary(image_url)
      media_ids.append(t_upload.media.upload(media=picBinary.read())["media_id_string"])
    return media_ids

  def post(self, *args, **kwargs):
    return self.t.statuses.update(*args, **kwargs)
