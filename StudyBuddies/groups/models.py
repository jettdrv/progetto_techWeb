from django.db import models
from django.conf import settings

class StudyGroup(models.Model):
    PRIVACY_CHOICES = (('public', 'Public') , ('private', 'Private') )
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_group')
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    #members=models.ManyToManyField(settings.AUTH_USER_MODEL, through= 'GroupMembership', related_name='study_groups')

    def __str__(self):
        return self.name


    
#una volta definito il gruppo, definisco anche la relazione di un utente con un gruppo, dove risulta creatore o amministratore oppure seplice membro
class GroupMembership(models.Model):
    ROLE_CHOICES = (('admin', 'Admin'), ('member', 'Member'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices = ROLE_CHOICES, default = 'member')

    class Meta:
        unique_together = ['user', 'group']

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class GroupDiscussion(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='discussions')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_discussions')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Discussione creata da {self.creator.username} in {self.group.name}"

class Comment(models.Model):
    discussion = models.ForeignKey(GroupDiscussion, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commento di {self.creator.username} della discussione {self.discussion.id}"

'''
class GroupInvite(models.Model):
    STATUS_CHOICES = (
        ('pending', 'In attesa'),
        ('accepted', 'Accettato'),
        ('rejected', 'Rifiutato'),
    )
    
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='invites')
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invites')
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_invites')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        unique_together = ['group', 'invitee']
'''