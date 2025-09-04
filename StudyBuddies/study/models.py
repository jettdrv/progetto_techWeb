from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name}"


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_sessions")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=4, decimal_places=1) 
    date = models.DateField() 
    notes = models.TextField(max_length=100)

    class Meta:
        ordering= ['-date']

    def __str__(self):
        return f"{self.subject} - {self.duration}h ({self.date})"