from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name = 'customer')
        instance.groups.add(group)

        Customer.objects.create(
            user = instance,    #link a new user to a customer
            name = instance.username,
            email = instance.email,
        )
        print("Profile created")

post_save.connect(customer_profile, sender = User)
