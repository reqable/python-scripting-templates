from reqable import *
import hashlib

def onRequest(context, request):
  # Sort the query list
  queries = sorted(request.queries)
  # Concat the query parameters
  text = HttpQueries(queries).concat()
  # Sign using the md5 algorithm
  algorithm = hashlib.md5()
  algorithm.update(text.encode(encoding='utf-8'))
  signature = algorithm.hexdigest()
  # The signature is added to the request header
  request.headers['signature'] = signature
  # Done
  return request

def onResponse(context, response):
  return response