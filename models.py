from django.db import models
from django.contrib.auth.models import User #import from Django Admin page, User
# from django.db.models.signals import post_save #signals
# Create your models here.

class Customer(models.Model):
    #"blank = True" means that you can create a customer without a user attached to it in the Django Admin page
    #OneToOneField means that a User can only have one customer, vice versa
    user = models.OneToOneField(User, null=True, blank = True, on_delete = models.CASCADE)   #CASCADE means whenever a User is deleted, the relationship to the customer will be deleted
    name = models.CharField(max_length = 255, null = True)
    phone = models.CharField(max_length = 255, null = True)
    email = models.CharField(max_length = 255, null = True)
    profile_pic = models.ImageField(default = "profile_pic.jpg",null = True, blank = True)
    data_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 255, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
            ('Fashion', 'Fashion'),
            ('Sports', 'Sports'),
            ('Furniture', 'Furniture'),
            ('Gardening', 'Gardening'),
            ('Kids', 'Kids'),
            ('Electronics', 'Electronics'),
            )

    name = models.CharField(max_length = 255, null = True)
    price = models.FloatField(null = True)
    category = models.CharField(max_length = 255, null = True, choices = CATEGORY)
    description = models.CharField(max_length = 255, null = True, blank = True)
    data_created = models.DateTimeField(auto_now_add = True, null = True)
    tags = models.ManyToManyField(Tag, null = True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
            ('Pending', 'Pending'),
            ('Out for delivery', 'Out for delivey'),
            ('Delivered', 'Delivered'),
            )

    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add = True, null = True)
    status = models.CharField(max_length = 255, null = True, choices = STATUS)
    #note = models.CharField(max_length = 1000, null = True)

    def __str__(self):
        return self.product.name








# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True)
#     first_name = models.CharField(max_length = 200, null = True, blank = True)
#     last_name = models.CharField(max_length = 200, null = True, blank = True)
#     phone = models.CharField(max_length = 200, null = True, blank = True)
#
#     def __str__(self):
#         return self.first_name
#
# def create_profile(sender, instance, created , **kwargs):
#
#     if created:
#         Profile.objects.create(user=instance)
#         print("Profile created!")
#
# post_save.connect(create_profile, sender=User) #occurs after save() function is completed
#
# def update_profile(sender, instance, created, **kwargs):
#
#     if created == False:
#         instance.profile.save()
#         print("Profile updated!")
#
# post_save.connect(update_profile, sender=User) #occurs after save() function is completed
