# -*- coding: utf-8 -*-
# https://github.com/twitterdev/twitter-python-ads-sdk/blob/master/examples/scheduled_tweet.py
from datetime import datetime, timedelta

from twitter_ads.client import Client
from twitter_ads.http import Request
from twitter_ads.campaign import ScheduledPromotedTweet
from twitter_ads.creative import ScheduledTweet
from twitter_ads.restapi import UserIdLookup
from twitter_ads.enum import MEDIA_CATEGORY

class TwitterAds:
  def __init__(self, access_token, access_token_secrets, twitter_ads_account_id, ADS_ACCOUNT_ID_MAPPER):
    self.ADS_ACCOUNT_ID_MAPPER = ADS_ACCOUNT_ID_MAPPER
    ads_account = TwitterAdsAPI.getAdsAccount(twitter_ads_account_id)

    # initialize the client
    self.client = Client(ads_account['consumer_key'], ads_account['consumer_secret'], access_token, access_token_secrets)
    self.twitter_ads_account_id = twitter_ads_account_id

    #class Test:
    #  def __init__(self, ADS_ACCOUNT_ID, client):
    #    self.id = ADS_ACCOUNT_ID
    #    self.client = client

    ##self.account =Test(self.ADS_ACCOUNT_ID, self.client)
    # load the advertiser account instance
    self.account = self.client.accounts(self.twitter_ads_account_id)

  @staticmethod
  def getAdsAccount(twitter_ads_account_id):
    return TwitterAdsAPI.ADS_ACCOUNT_ID_MAPPER[twitter_ads_account_id]

  def uploadMedia(self, mediaBinary):
    # upload an image to POST media/upload
    # https://developer.twitter.com/en/docs/ads/creatives/guides/media-library
    resource = '/1.1/media/upload.json'
    params = {
        'additional_owners': self.ADS_ACCOUNT_ID_MAPPER[self.twitter_ads_account_id]['account_id'],
        'media_category': MEDIA_CATEGORY.TWEET_IMAGE
    }
    domain = 'https://upload.twitter.com'
    files = {'media': (None, mediaBinary)}
    response = Request(self.client, 'post', resource, files=files, domain=domain, params=params).perform()

    # extract the media_key value from the response
    media_key = response.body['media_key']
    return media_key

  # ('', datetime.utcnow() + timedelta(days=2), 'your_twitter_handle_name')
  def scheduleTweets(self, message, scheduled_at, media_keys=[]):
    try :
      screen_name = self.ADS_ACCOUNT_ID_MAPPER[self.twitter_ads_account_id]['screen_name']

      # get user_id for as_user_id parameter
      user_id = UserIdLookup.load(self.account, screen_name=screen_name).id

      # create the Scheduled Tweet
      scheduled_tweet = ScheduledTweet(self.account)
      scheduled_tweet.text = message
      scheduled_tweet.as_user_id = user_id
      scheduled_tweet.scheduled_at = scheduled_at
      scheduled_tweet.media_keys = media_keys
      scheduled_tweet.nullcast = False # not `Promoted-only` tweet
      scheduled_tweet.save()

      return {'status': 'success'}
    except Exception as e:
      print(e)

      return {'status': 'error', 'error_code': e.details[0]['code'], 'error': e.details[0]['message']}
