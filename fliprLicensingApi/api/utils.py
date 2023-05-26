from __future__ import absolute_import, unicode_literals
from base64 import b64decode, b64encode
from django.core.mail import send_mail
from celery import shared_task
from decouple import config
from .models import License
import rsa
from django.core.cache import cache

@shared_task
def generate_license(name, user, policy, validUpto):
  public_key, private_key = new_rsa()
  signature = rsa.PrivateKey.load_pkcs1(private_key)
  key = b64encode(rsa.sign(user.email.encode(), signature, 'SHA-1')).decode()
  License.objects.create(
    name=name,
    key=key,
    public_key=public_key,
    private_key=private_key,
    user=user,
    validUpto=validUpto
  )
  mail_license_keys.delay(key, user.email)
  record = License.objects.get(key=key)
  cache.set([user.email, key], True, record.status)

def new_rsa():
  public, private = rsa.newkeys(512)
  return public.save_pkcs1().decode(), private.save_pkcs1().decode()

def validate_signature(email, license_key, public_key):
  key = rsa.PublicKey.load_pkcs1(public_key)
  try:
    rsa.verify(email.encode(), b64decode(license_key), key)
  except rsa.VerificationError:
    return False
  else:
    return True

@shared_task
def mail_license_keys(key, to_email):
  from_mail = config("FROM_ACCOUNT")
  subject = "License Key"
  body = f"""
Your requested license key is mentioned below 

License Key: {key}
Issued To: {to_email}

This is an auto-generated mail. Please, do not reply.
"""
  send_mail(subject, body, from_mail, [to_email])