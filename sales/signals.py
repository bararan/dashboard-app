from .models import Sale
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Sale.positions.through)
def calculate_price(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove': 
        total_price = sum([p.price for p in instance.get_positions()])
        instance.total_price = total_price
        instance.save()
        # print(instance)