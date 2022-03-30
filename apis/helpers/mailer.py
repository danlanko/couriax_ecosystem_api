import threading
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import serializers


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        try:
            msg.send()
        except Exception as error:
            print(error)


def send_mail(subject, message, email_list):
    try:
        EmailThread(subject=subject, html_content=message, recipient_list=email_list).start()
    except Exception as error:
        raise serializers.ValidationError({
            'details': ['Email sending failed: %s' % error]
        })