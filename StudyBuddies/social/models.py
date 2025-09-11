from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Friendship(models.Model):

    STATUS_CHOICES = (('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'))
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_request')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_request')
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    class Meta:
        unique_together = ['from_user', 'to_user']

    def accept(self):
        self.status = 'accepted'
        self.save()

        self.from_user.friends.add(self.to_user)
        self.to_user.friends.add(self.from_user)

    def reject(self):
        self.status = 'rejected'
        self.save()

    
        



