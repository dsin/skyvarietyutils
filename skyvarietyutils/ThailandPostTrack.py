import skyvarietyutils, json

class ThailandPostTrack:
  def __init__(self, token):
    self.DOMAIN = 'https://trackapi.thailandpost.co.th'
    self.WEBHOOK_DOMAIN = 'https://trackwebhook.thailandpost.co.th'
    self.STATUS_ITEM = {
      101: {
        'TH': 'เตรียมการฝากส่ง',
      },
      102: {
        'TH': 'รับฝากผ่านตัวแทน',
      },
      103: {
        'TH': 'รับฝาก',
      },
      201: {
        'TH': 'อยู่ระหว่างการขนส่ง',
      },
      202: {
        'TH': 'ดำเนินพิธีการศุลกากร',
      },
      203: {
        'TH': 'ส่งคืนต้นทาง',
      },
      204: {
        'TH': 'ถึงที่ทำการแลกเปลี่ยนระหว่างประเทศขาออก',
      },
      205: {
        'TH': 'ถึงที่ทำการแลกเปลี่ยนระหว่างประเทศขาเข้า',
      },
      206: {
        'TH': 'ถึงที่ทำการไปรษณีย์',
      },
      207: {
        'TH': 'เตรียมการขนส่ง',
      },
      208: {
        'TH': 'ส่งออกจากที่ทำการแลกเปลี่ยนระหว่างประเทศขาออก',
      },
      301: {
        'TH': 'อยู่ระหว่างการนำจ่าย',
      },
      302: {
        'TH': 'นำจ่าย ณ จุดรับสิ่งของ',
      },
      401: {
        'TH': 'นำจ่ายไม่สำเร็จ',
      },
      501: {
        'TH': 'นำจ่ายสำเร็จ',
      },
      901: {
        'TH': 'โอนเงินให้ผู้ขายเรียบร้อยแล้ว',
      },
    }
    self.TOKEN = token

  def track(self, barcode, language='TH'):
    token = (self.auth())['token']

    url = self.DOMAIN + '/post/api/v1/track'
    data = {
      'status': 'all',
      'language': language,
      'barcode': [
        barcode
      ]
    }
    print(data)
    return json.loads(skyvarietyutils.http.post(url, data, {
      'Authorization': 'Token ' + token,
      }, type='json').read())['response']['items'][barcode]

  def register_hook(self, barcode, language='TH'):
    token = (self.auth())['token']

    url = self.WEBHOOK_DOMAIN + '/post/api/v1/hook'
    data = {
      'status': 'all',
      'language': language,
      'barcode': [
        barcode
      ]
    }
    print(url)
    return json.loads(skyvarietyutils.http.post(url, data, {
      'Authorization': 'Token ' + token,
      }, type='json').read())['response']['items']

  def auth(self):
    url = self.DOMAIN + '/post/api/v1/authenticate/token'

    return json.loads(skyvarietyutils.http.post(url, {}, {
      'Authorization': 'Token ' + self.TOKEN,
      'Content-Type': 'application/json',
      }).read())
