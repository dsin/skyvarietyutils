# from http://daily.profeth.de/2008/04/using-recaptcha-with-google-app-engine.html
# download from : http://dev.feth.com/Python/Google%20App%20Engine/recaptcha/captcha.source
import skyvarietyutils
import json

"""
    Adapted from http://pypi.python.org/pypi/recaptcha-client
    to use with Google App Engine
    by Joscha Feth <joscha@feth.com>
    Version 0.1
"""

API_SSL_SERVER  ='https://www.google.com'
API_SERVER      ='http://www.google.com'
VERIFY_SERVER   ='www.google.com'

class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid   = is_valid
        self.error_code = error_code

def displayhtml(public_key,
                use_ssl=True):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    return """<div class="g-recaptcha" data-sitekey="%(PublicKey)s"></div>
              <script src='%(ApiServer)s/recaptcha/api.js'></script>""" % {'ApiServer' : server,
       'PublicKey' : public_key
      }

def submit(recaptcha_challenge_field,
           recaptcha_response_field,
           private_key,
           remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field  and # recaptcha_challenge_field
            len (recaptcha_response_field)): # and len (recaptcha_challenge_field)
        return RecaptchaResponse(is_valid=False, error_code='incorrect-captcha-sol')

    headers = {
               'Content-type':  'application/x-www-form-urlencoded',
               "User-agent"  :  "reCAPTCHA GAE Python"
               }

    params = {
        'secret': private_key,
        'remoteip' : remoteip,
        'response' : recaptcha_response_field,
    }

    #params = urllib.urlencode({
    #    'secret': private_key,
    #    'remoteip' : remoteip,
  #    'response' : recaptcha_response_field,
  #    })

    #httpresp = urlfetch.fetch(
    #               url      = "https://%s/recaptcha/api/siteverify" % VERIFY_SERVER,
    #               payload  = params,
    #               method   = urlfetch.POST,
    #               headers  = headers
    #                )

    httpresp = skyvarietyutils.http.post('https://%s/recaptcha/api/siteverify' % VERIFY_SERVER, params, headers)

    if httpresp.getcode() == 200:
        # response was fine

        # get the return values
        return_values = json.loads(httpresp.read())
        #return_values = httpresp.content.splitlines();
        # get the return code (true/false)
        return_code = return_values['success']
        #return_code = return_values[0]

        if return_code == True:
            # yep, filled perfectly
            return RecaptchaResponse(is_valid=True)
        else:
            # nope, something went wrong
            return RecaptchaResponse(is_valid=False, error_code=return_values['error-codes'] if 'error-codes' in return_values.keys() else '') # error_code = return_values[1]
    else:
        # recaptcha server was not reachable
        return RecaptchaResponse(is_valid=False, error_code="recaptcha-not-reachable")
