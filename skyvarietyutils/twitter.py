# -*- coding: utf-8 -*-
import tweepy

class Twitter():
  def __init__(self, consumer_key, consumer_secret, callback_url='', oauth_token=None):
    self.CONSUMER_KEY = consumer_key
    self.CONSUMER_SECRET = consumer_secret
    self.CALLBACK_URL = callback_url

    self.oauth_token = oauth_token

  def app_login(self):
    #auth = tweepy.AppAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)

    #self.api = tweepy.API(auth)
    self.api = None

  def login(self):
    auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.CALLBACK_URL)
    # auth = None
    redirect_url = auth.get_authorization_url()

    return (auth.request_token['oauth_token'], auth.request_token['oauth_token_secret'], redirect_url)

  def login_with_token(self, access_token, access_token_secret):
    # auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
    # auth.set_access_token(access_token, access_token_secret)

    # self.api = tweepy.API(
    #   auth,
    #   wait_on_rate_limit=True,
    #   wait_on_rate_limit_notify=True,
    # )
    self.api = None

  def callback_url_verification(self, token, token_secret, oauth_verifier):
    auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.CALLBACK_URL)
    auth.request_token = {
      'oauth_token' : token,
      'oauth_token_secret' : token_secret
    }

    auth.get_access_token(oauth_verifier)

    return (auth.access_token, auth.access_token_secret)

  def get_home_timeline(self, oauth_token):
    #http://api.twitter.com/version/statuses/home_timeline.json
    pass

  def get_twitter_search(self, q, result_type=None, since_id=None):
    h = OAuthHandle()

    url = 'http://search.twitter.com/search.json'
    params = {}
    params['count'] = str(200)
    if q :
      params['q'] = q
    if result_type :
      params['result_type'] = result_type
    if since_id :
      params['since_id'] = since_id

    ws = WebSpider()
    uri = h.get_request_uri(params, self.oauth_token)

    result = ws.get(url+'?'+uri, {}, {})
    results = simplejson.loads(result.content)
    #self.write(results[0])
    return results

  def twitter_follow(self, user_id, screen_name):
    try :
      self.api.create_friendship(None, user_id, screen_name, True)
    except tweepy.TweepError:
      logging.info('tweepy error when try to follow %s' % screen_name)

  def twitter_unfollow(self, user_id, screen_name):
    self.api.destroy_friendship(None, user_id, screen_name)

  def twitter_update_status(self, status, in_reply_to_tweet_id):
    try:
      #print(api.me().name)
      self.api.update_status(status, in_reply_to_tweet_id)
    except tweepy.error.TweepError:
      return 'Quote : %s, TweepError : %s' % (status, sys.exc_info()[0])

  def update_status(self, *args, **kwargs):
    return self.api.update_status(*args, **kwargs)

  def get_direct_messages(self, since_id, count=100):
    return self.api.direct_messages(since_id, None, count, None)

  def send_direct_message(self, screen_name, text):
    return self.api.send_direct_message(None, screen_name, None, text)

  def get_followings(self, screen_name, cursor):
    return self.api.friends_ids(None, None, screen_name, cursor)

  def get_followers(self, screen_name, cursor):
    return self.api.followers_ids(None, None, screen_name, cursor)

  def lookup_users(self, user_ids):
    return self.api.lookup_users(user_ids, None)

  def get_twitter_timeline(self, since_id=1):
      h = OAuthHandle()

      url = 'http://twitter.com/statuses/user_timeline/dsin.json'
      params = {}
      params['count'] = str(200)
      if since_id > 0:
        params['since_id'] = str(since_id)

      ws = WebSpider()
      uri = h.get_request_uri(params, self.oauth_token)

      result = ws.get(url+'?'+uri, {}, {})
      results = simplejson.loads(result.content)
      # self.write(results[0])
      return results

if __name__ == '__main__':
  twitterClient = TwitterAPI(consumer_key, consumer_secret)
  twitterClient.login()
  print(twitterClient.get_twitter_timeline())
