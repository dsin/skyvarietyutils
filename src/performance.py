import datetime

class PerformanceUtil:
  def start(self):
    self.start_time = datetime.datetime.now()

  def end(self):
    self.end_time = datetime.datetime.now()

  def getExecutionTimeInSecond(self):
    execution_time = self.end_time - self.start_time
    return float(execution_time.microseconds)/1000000
