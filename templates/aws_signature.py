from reqable import *
import hmac
import hashlib
import datetime

# TODO Replace with your config
access_key = 'YOUR_ACCESS_KEY'
secret_key = 'YOUR_SECRET_KEY'
region = 'us-east-1'
service = 's3'

def sign(key, msg):
  return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
  sign_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
  sign_region = sign(sign_date, region_name)
  sign_service = sign(sign_region, service_name)
  return sign(sign_service, 'aws4_request')

def onRequest(context, request):
  method = request.method
  # Build canonical query parameters.
  canonical_uri = request.path
  sorted_queries = sorted(request.queries)
  canonical_query_string = HttpQueries(sorted_queries).concat()

  # Calculate body hash.
  if request.body.isNone:
    payload_hash = hashlib.sha256(''.encode('utf-8')).hexdigest()
  elif request.body.isText:
    payload_hash = hashlib.sha256(request.body.encode('utf-8')).hexdigest()
  elif request.body.isBinary:
    payload_hash = hashlib.sha256(request.body).hexdigest()
  else:
    raise Exception('Unsupported body type.')
  request.headers['X-Amz-Content-Sha256'] = payload_hash

  # Build datetime.
  t = datetime.datetime.utcnow()
  amz_date = t.strftime('%Y%m%dT%H%M%SZ')
  request.headers['X-Amz-Date'] = amz_date

  # Build canonical headers.
  sorted_headers = sorted(request.headers)
  canonical_headers = f'host:{context.host}\n'
  signed_headers = 'host;'
  for header in sorted_headers:
    name, value = header.split(': ')
    if name.lower().startswith('x-amz-') or name.lower() is 'content-type':
      canonical_headers += name.lower().strip() + ':' + value.strip() + '\n'
      signed_headers += name.lower().strip() + ';'

  # Build canonical request.
  canonical_request = f"{method}\n{canonical_uri}\n{canonical_query_string}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

  date_stamp = t.strftime('%Y%m%d')
  credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"

  algorithm = 'AWS4-HMAC-SHA256'
  string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
  signing_key = get_signature_key(secret_key, date_stamp, region, service)
  signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

  request.headers['Authorization'] = f'{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
  return request

def onResponse(context, response):
  return response
