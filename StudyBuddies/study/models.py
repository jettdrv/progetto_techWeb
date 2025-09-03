from django.db import models
from django.contrib.auth import get_user_model
from users.models import CustomUser

User=get_user_model()

class StudySession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="study_sessions")
    subject = models.CharField(max_length=100) # Es: "Matematica", "Python"
    duration = models.DecimalField(max_digits=4, decimal_places=1) # Es: 1.5 ore
    date = models.DateField() 
    notes = models.TextField(max_length=100)
    def __str__(self):
        return f"{self.subject} - {self.duration}h ({self.date})"