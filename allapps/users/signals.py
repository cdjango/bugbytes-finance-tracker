from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def create_allauth_email_address(sender, instance, created, **kwargs):
    if created and instance.email:
        EmailAddress.objects.get_or_create(
            user=instance,
            email=instance.email.lower(),
            defaults={
                "primary": True,
                "verified": True,
            },
        )
