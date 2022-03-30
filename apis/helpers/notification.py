from django.utils import timezone
from random import randint
from apis.helpers.mailer import send_mail
from apis.users.authentication.models import UsersVerification


def send_activation_code(user):
    code = randint(100000, 999999)
    UsersVerification.objects.update_or_create(
        user=user,
        defaults={
            "code": code,
            "valid": True,
            "validity": timezone.now()
        }
    )
    try:
        message = f"Hi {user.get_full_name()}, Your verification code is {code}"
        mail_subject = 'Welcome To Couriax'
        to_email = [user.email]
        send_mail(message=message, subject=mail_subject, email_list=to_email)
        print(message)
    except Exception as error:
        print(error)

    return {"success": True}

