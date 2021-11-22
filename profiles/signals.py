from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created: #So that this will be invoked only when the user is created
        print(sender)
        print(instance)
        print(created)
        Profile.objects.create(user=instance)