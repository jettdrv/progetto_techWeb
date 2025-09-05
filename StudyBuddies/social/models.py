from django.db import models
from users import CustomUser

class Friendship(models.Model):

    STATUS_CHOICES = (('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'))
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_request')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_request')
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique = ['from_user', 'to_user']