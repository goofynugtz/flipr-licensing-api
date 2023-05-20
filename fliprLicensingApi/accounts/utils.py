from django.core.mail import send_mail
from decouple import config

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
  return True
