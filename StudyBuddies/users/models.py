from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE = (('Student', 'student'), ('Professional', 'professional'))

    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='student')
    profile_picture = models.ImageField(upload_to='static/pfp/', blank=True, null=True)
    expertise_field = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.username
    
    @property
    def is_professional(self):
        return self.user_type == 'Professional'