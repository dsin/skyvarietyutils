# -*- coding: utf-8 -*-

def exerpt(str, length):
  return str[:length] + '...' if len(str) > length else str

def camelcase_to_dashstyle(name):
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def dashstyle_to_camelcase(name):
  components = name.split('-')
  # We capitalize the first letter of each component except the first one
  # with the 'title' method and join them together.
  return components[0] + "".join(x.title() for x in components[1:])

def getCSV(rows):
  import io
  import csv

  output = io.StringIO()
  writer = csv.writer(output)
  for row in rows:
    writer.writerow(row)
  return output.getvalue()

def remove_prefix(text, prefix):
  if text.startswith(prefix):
      return text[len(prefix):]
  return text  # or whatever
