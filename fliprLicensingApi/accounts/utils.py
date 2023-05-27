from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from celery import shared_task
from decouple import config

@shared_task
def send_password_reset_mail(to_email, token):
  password_reset_uri = f"https://{config('BASE_URI')}/accounts/reset-password/{token}/"
  from_mail = config("FROM_ACCOUNT")
  subject = "Password Reset"
  body = f"""
Your requested link for resetting password is:
{password_reset_uri}

This is an auto-generated mail. Please, do not reply.
"""
  send_mail(subject, body, from_mail, [to_email])

@shared_task
def send_verification_mail(to_email, confirmation_token):
  confirmation_uri = f"https://{config('BASE_URI')}/accounts/verify/{confirmation_token}/"
  from_mail = config("FROM_ACCOUNT")
  subject = "Confirm your Account"
  body = f"""
We have a signup request from this email. To confirm signup, visit the following link:
{confirmation_uri}
If it wasn't you, then please ignore this mail.

This is an auto-generated mail. Please, do not reply.
"""
  send_mail(subject, body, from_mail, [to_email])
