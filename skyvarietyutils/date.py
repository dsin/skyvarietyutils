import datetime, random

def daysSinceEpoch():
  epoch = datetime.datetime.utcfromtimestamp(0) # ( 1970-01-01 00:00:00 )
  today = datetime.datetime.today() # 13196 days, 9:50:44.266200
  d = today - epoch
  return d.days # timedelta object ( 13196 )

def tomorrowAt(hour):
  now = datetime.datetime.now()
  tomorrow = now + datetime.timedelta(days=1)
  return tomorrow.replace(hour=hour-7, minute=random.randint(0,59), second=random.randint(0,59))
  # return datetime.datetime(now.year, now.month, now.day+1, hour-7, random.randint(0,59), random.randint(0,59), tzinfo=datetime.timezone.utc)
