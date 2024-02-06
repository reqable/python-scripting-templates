from reqable import *

import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# TODO Replace with your key and iv
key = '1234567812345678'.encode('utf-8')
iv = '1234567812345678'.encode('utf-8')

def encrypt(key, iv, plaintext):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
  encryptor = cipher.encryptor()
  padder = padding.PKCS7(algorithms.AES.block_size).padder()
  padded_data = padder.update(plaintext) + padder.finalize()
  ciphertext = encryptor.update(padded_data) + encryptor.finalize()
  return ciphertext

def decrypt(key, iv, ciphertext):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
  decryptor = cipher.decryptor()
  decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
  unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
  plaintext = unpadder.update(decrypted_data) + unpadder.finalize()
  return plaintext

def onRequest(context, request):
  # TODO Replace with your plaintext data.
  plaintext = 'Your plaintext data'.encode('utf-8')
  # Optional: Use base64 to encode encrypt bytes.
  ciphertext = base64.b64encode(encrypt(key, iv, plaintext)).decode('utf-8')
  print(f'encrypted: {ciphertext}')
  return request

def onResponse(context, response):
  # TODO Replace with your encrypted data.
  # Optional: Use base64 to decode encrypt bytes.
  ciphertext = base64.b64decode('KjiPMFKJFB4e0WTL74lAKR0/BG08Zkn36UqSs3obsnQ=')
  plaintext = decrypt(key, iv, ciphertext).decode('utf-8')
  print(f'decrypted: {plaintext}')
  return response
