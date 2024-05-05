from django.db import models
from django.contrib.auth.models import User,AbstractUser,Group,Permission

# Create your models here.


class userRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=11)
    is_verified = models.BooleanField(null=True)
    
    #fullAddress = models.CharField(max_length=50)

    def __str__(self):
        return self.firstName + " " + self.lastName

# class CustomUser(AbstractUser):
#     phone = models.CharField(max_length=11)
#     is_verified = models.BooleanField()

#     groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
#     user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)


#     class Meta:
#         # Add a unique related_name for the groups and user_permissions fields
#         # This prevents clash with the default User model's reverse accessors
#         # You can choose any unique related_name you prefer
#         db_table = 'custom_user'
#         verbose_name = 'Custom User'
#         verbose_name_plural = 'Custom Users'
#         swappable = 'AUTH_USER_MODEL'