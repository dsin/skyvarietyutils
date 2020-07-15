import datetime

def daysSinceEpoch():
  epoch = datetime.datetime.utcfromtimestamp(0) # ( 1970-01-01 00:00:00 )
  today = datetime.datetime.today() # 13196 days, 9:50:44.266200
  d = today - epoch
  return d.days # timedelta object ( 13196 )
