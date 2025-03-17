from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .views.tasks import send_mail_task
from .models import Password_Token

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail_task.delay(
            "Welcome",
            f"Hello {instance.username} Welcome to our website enjoy from solving the questions.",
            settings.EMAIL_HOST_USER,
            [instance.email],
        )


@receiver(post_save, sender=Password_Token)
def send_password_token(sender, instance, created, **kwargs):
    if created:
        send_mail_task.delay(
            "Password Forgot Notification",
            f"""Please click on this link for set your new password
            <a href="{settings.PASSWORD_FORGOT_TOKEN_URL}/{instance.token}/">click here.</a>""",
            settings.EMAIL_HOST_USER,
            [instance.user.email],
        )
