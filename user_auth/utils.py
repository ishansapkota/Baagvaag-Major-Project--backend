#here the code for sending email for verification and resetting the password will be present

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

def send_email_verification(user):
        #auth_user = User.objects.get(pk=user.pk)
        token = default_token_generator.make_token(user)
        verification_link = f'http://localhost:8000/api/verify/{user.id}/{token}'
        subject = 'Verification of your Email'
        message = f'Click the following link to verify your email : {verification_link}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        try:
                send_mail( subject, message, email_from, recipient_list)
                return True
        except Exception as e:
                print(e)
                return False
        
def forgot_password(user):
        token = default_token_generator.make_token(user)
        reset_link = f'http://localhost:8000/api/reset_password/{user.id}/{token}'
        subject = 'Resetting Password'
        message = f'Click the following link to reset your password : {reset_link}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        try:
                send_mail( subject, message, email_from, recipient_list)
                return True
        except Exception as e:
                print(e)
                return False

