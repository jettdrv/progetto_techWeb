from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from social.models import Friendship


class CustomUser(AbstractUser):
    USER_TYPE = (('Student', 'student'), ('Professional', 'professional'))

    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='student')
    profile_picture = models.ImageField(upload_to='pfp', default='/pfp/nopfp.jpg')
    expertise_field = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True)
    daily_goal_hours = models.DecimalField(max_digits=4, decimal_places=2, default = 1, validators=[MinValueValidator(1.0), MaxValueValidator(24.0)]) #per impostare gli obiettivi personali
    weekly_goal_hours = models.DecimalField(max_digits=5, decimal_places=2, default = 1, validators=[MinValueValidator(1.0), MaxValueValidator(168.0)])
    #--------aspetto social-----------------------------
    friends = models.ManyToManyField('self', through='social.Friendship', symmetrical=True, blank = True, related_name='friend_of')

    def save(self, *args, **kwargs):
        if self.pk:
            old = CustomUser.objects.get(pk=self.pk)
            if old.profile_picture != self.profile_picture:
                if old.profile_picture and old.profile_picture.name != '/pfp/nopfp.jpg':
                    old.profile_picture.delete(save=False)
        super().save(*args, **kwargs)

    def is_friend_with(self, user):
        return self.friends.filter(id=user.id).exists()
    def remove_friend(self, user):
        Friendship.objects.filter(Q(from_user=self, to_user=user)| Q(from_user=user, to_user=self), status = 'accepted').delete()
        self.friends.remove(user)
        
    @property
    def friends_accepted(self):
        friendships = Friendship.objects.filter((models.Q(from_user=self) | models.Q(to_user=self)), status='accepted')
        return [f.to_user if f.from_user == self else f.from_user for f in friendships]


    @property
    def is_professional(self):
        return self.user_type == 'Professional'
    
    def __str__(self):
        return self.username
    