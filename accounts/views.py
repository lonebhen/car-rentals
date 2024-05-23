from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
import os

from django_rest_passwordreset.signals import reset_password_token_created
# Create your views here.

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "frontendurl/reset-password?token={}".format(reset_password_token.key)
    }

    email_html_message = render_to_string(
        'email/user_reset_password.html', context)
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Car Rental App"),
        # message:
        email_plaintext_message,
        # from:
        os.getenv('EMAIL_HOST_USER'),
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


class AccountEmailVerificationSentView(APIView):
    def get(self, request):
        return Response({'message': 'Account email verification sent.'})