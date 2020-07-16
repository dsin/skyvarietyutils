import re

# trim to TWITTER_LIMIT_CHARACTERS also considering minify link to https://t.co
def trimTwitterText(txt):
  TWITTER_LIMIT_CHARACTERS = 280
  # https://developer.twitter.com/en/docs/basics/counting-characters
  TWITTER_T_CO_URL_LENGTH = 23

  url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
  found_regex_obj = re.findall(url_pattern, txt)
  found_obj = [x[0] for x in found_regex_obj]

  currentURLLength = sum(map(lambda url: len(url), found_obj))
  realURLLength = len(found_obj) * TWITTER_T_CO_URL_LENGTH
  adjustedLength = TWITTER_LIMIT_CHARACTERS + currentURLLength - realURLLength

  return txt[:adjustedLength]

def removeLastTag(txt):
  index = txt.rfind('#')
  return txt[:index]
