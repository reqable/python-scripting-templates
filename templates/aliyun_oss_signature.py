from reqable import *
import hmac
import hashlib
import base64
import datetime

# TODO Replace with your keys
access_key_id = 'Your key id'
access_key_secret = 'Your key secret'

def onRequest(context, request):
  date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
  signature_string = f"GET\n\n\n{date}\n"
  signature_string += f"/{context.host.split('.')[0]}{request.path}"
  signature = base64.b64encode(hmac.new(access_key_secret.encode('utf-8'), signature_string.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')
  request.headers['Date'] = date
  request.headers['Authorization'] = f'OSS {access_key_id}:{signature}'
  return request

def onResponse(context, response):
  return response
