from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import StudySession, Subject
from django.urls import reverse
from datetime import datetime
from django.core.exceptions import ValidationError

User = get_user_model()
class StudySessionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usernametesting", password="beepboop")
        self.subject =Subject.objects.create(name='matematica')
        self.client.login(username='usernametesting', password='beepboop')

    def test_study_session_create(self):
        session=StudySession.objects.create(user = self.user, subject =self.subject, duration = 2.5, date=datetime.now().date(), notes='session created by unit test')
        self.assertEqual(session.duration, 2.5)
        self.assertEqual(session.user.username, 'usernametesting')
        self.assertEqual(session.subject.name, 'matematica')
        self.assertIsInstance(session.subject, Subject)

    def test_study_session_create(self):
        session=StudySession.objects.create(user = self.user, subject =self.subject, duration = 25.0, date=datetime.now().date(), notes='session created by unit test2')
        with self.assertRaises(ValidationError):
            session.full_clean()
        
    def test_study_session_list(self):
        response = self.client.get(reverse('study:session_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'study/session_list.html')

class SubjectTest(TestCase):
    def setUp(self):
        self.subject = Subject(name="testSubject")

    def test_subject_name(self):
        self.assertEqual(self.subject.name, 'testSubject')
        self.subject.name = 'TestSubject'
        self.assertNotEqual(self.subject.name, 'testSubject')