from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE = (('Student', 'student'), ('Professional', 'professional'))

    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='student')
    profile_picture = models.ImageField(upload_to='pfp', default='/pfp/nopfp.jpg')
    expertise_field = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True)
    #--------aspetto social-----------------------------
    friends = models.ManyToManyField('self', through='social.Friendship', symmetrical=True, related_name='friend_of')

    @property
    def is_professional(self):
        return self.user_type == 'Professional'
    
    def save(self, *args, **kwargs):
        if self.pk:
            old = CustomUser.objects.get(pk=self.pk)
            if old.profile_picture != self.profile_picture:
                if old.profile_picture and old.profile_picture.name != '/pfp/nopfp.jpg':
                    old.profile_picture.delete(save=False)
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.username
    