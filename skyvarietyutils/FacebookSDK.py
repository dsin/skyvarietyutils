import facebook, json

# get user access token
# from https://developers.facebook.com/tools/explorer/

# debug access token + click extend user access token
# https://developers.facebook.com/tools/debug/accesstoken

# get page access token
# curl -i -X GET "https://graph.facebook.com/{page-id}?fields=access_token&access_token={user-access-token}"

# ref : https://medium.com/@yasithlokuge/how-to-generate-a-never-expiring-facebook-page-access-token-24ac5c1a95f1

class FacebookSDK:
  def __init__(self, page_access_token):
    self.graph = facebook.GraphAPI(page_access_token)

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
