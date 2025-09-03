from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_sessions")
    subject = models.CharField(max_length=100) # Es: "Matematica", "Python"
    duration = models.DecimalField(max_digits=4, decimal_places=1) # Es: 1.5 ore
    date = models.DateField() # Data della sessione
    notes = models.TextField(max_length=100)
    def __str__(self):
        return f"{self.subject} - {self.duration}h ({self.date})"