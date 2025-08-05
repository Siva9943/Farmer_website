from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def set_username_from_google(request, user, **kwargs):
    if user.first_name:
        user.username = user.first_name.lower()  # you can append a number if needed
        user.save()
