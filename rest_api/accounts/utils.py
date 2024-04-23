import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings

def generate_OTP():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_mail(email):
    subject = ""
    otp = generate_OTP()
    user = User.objects.get(email=email)
    site = "sample.com"
    mail_body = ""
    from_mail = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp)

    send = EmailMessage(subject=subject, body=mail_body, from_email=from_mail, to=[email])
    send.send(fail_silently=True)
