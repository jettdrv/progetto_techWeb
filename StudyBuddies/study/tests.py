from django.test import TestCase, Client
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
        

    def test_study_session_create(self):
        session=StudySession.objects.create(user = self.user, subject =self.subject, duration = 2.5, date=datetime.now().date(), notes='session created by unit test')
        self.assertEqual(session.duration, 2.5)
        self.assertEqual(session.user.username, 'usernametesting')
        self.assertEqual(session.subject.name, 'matematica')
        self.assertIsInstance(session.subject, Subject)

    def test_study_session_create_invalid(self):
        session=StudySession.objects.create(user = self.user, subject =self.subject, duration = 25.0, date=datetime.now().date(), notes='session created by unit test2')
        with self.assertRaises(ValidationError):
            session.full_clean()

    def test_create_session_missing_fields(self):
        with self.assertRaises(ValueError):
            StudySession.objects.create(user = self.user, subject =' ', duration = 2.0, date=datetime.now().date(), notes='session created by unit test3')
        #adesso creo una sessione di studio senza il campo note, che è obbligatiorio
        with self.assertRaises(Exception):
            StudySession.objects.create(user = self.user, duration = 2.0, date=datetime.now().date())
        #manca la durata
        with self.assertRaises(Exception):
            StudySession.objects.create(user = self.user, date=datetime.now().date(), notes='ffvcvbgrfvd')
        
    def test_study_session_to_string(self):
        session= StudySession.objects.create(user = self.user, subject =self.subject, duration = 2.0, date=datetime.now().date(), notes='testing string format')
        self.assertEqual(str(session), f"{session.subject} - {session.duration}h ({session.date})")
        self.assertEqual(str(session), f"matematica - 2.0h ({datetime.now().date()})")

    def test_user_delete(self):
        session= StudySession.objects.create(user = self.user, subject =self.subject, duration = 2.0, date=datetime.now().date(), notes='testing user deletion')
        session2= StudySession.objects.create(user = self.user, subject =self.subject, duration = 6.0, date=datetime.now().date(), notes='testing user deletion2')
        session3= StudySession.objects.create(user = self.user, subject =self.subject, duration = 1.0, date=datetime.now().date(), notes='testing user deletion3')
        self.assertEqual(StudySession.objects.count(), 3)
        self.user.delete()
        self.assertEqual(StudySession.objects.count(), 0)

        


class SubjectTest(TestCase):
    def setUp(self):
        self.subject = Subject(name="testSubject")

    def test_subject_name(self):
        self.assertEqual(self.subject.name, 'testSubject')
        self.subject.name = 'TestSubject'
        self.assertNotEqual(self.subject.name, 'testSubject')

class StudyViewTest(TestCase):
            
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="usernametesting", password="beepboop")
        
    def test_study_session_list_non_authenticated(self):
        response = self.client.get(reverse('study:session_list'))
        self.assertIn(response.status_code, [302, 403])

    def test_study_session_list_authenticated(self):
        self.client.login(username='usernametesting', password='beepboop')
        response = self.client.get(reverse('study:session_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'study/session_list.html')

    
    def test_study_session_create_valid_form(self):
        self.client.login(username='usernametesting', password='beepboop')
        initial_sessions = StudySession.objects.count()
        subj = Subject.objects.create(name='matematica', created_by=self.user)
        
        response = self.client.post(reverse('study:add_session'), {
            'date': datetime.now().date(),
            'duration': 2.0,
            'subject': subj.id ,
            'notes':'fergfs'
        })
        #redirect con successo
        self.assertEqual(response.status_code, 302)
        self.assertEqual(StudySession.objects.count(), initial_sessions+1)

    def test_study_session_create_invalid_form(self):
        self.client.login(username='usernametesting', password='beepboop')
        initial_sessions = StudySession.objects.count()
        subj = Subject.objects.create(name='matematica', created_by=self.user)

        response = self.client.post(reverse('study:add_session'), {
            'date': datetime.now().date(),
            'duration': 45.0,
            'subject': subj.id ,
            'notes':'fergfs'
        })
        self.assertEqual(response.status_code, 200)
        #l'oggetto non dovrebbe essere creato
        self.assertEqual(StudySession.objects.count(), initial_sessions)



    def test_delete_session(self):
        self.client.login(username='usernametesting', password='beepboop')
        initial_sessions = StudySession.objects.count()
        subj = Subject.objects.create(name='matematica', created_by=self.user)
        session= StudySession.objects.create(user=self.user, subject =subj, duration = 2.0, date=datetime.now().date(), notes='testing session delete')
        self.assertEqual(StudySession.objects.count(), initial_sessions +1)

        response=self.client.post(reverse('study:delete_session', args=[session.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('study:session_list'))
        self.assertEqual(StudySession.objects.count(), initial_sessions )
        
    def test_edit_session_valid(self):
        self.client.login(username='usernametesting', password='beepboop')
        
        subj = Subject.objects.create(name='matematica', created_by=self.user)
        session= StudySession.objects.create(user=self.user, subject =subj, duration = 2.0, date=datetime.now().date(), notes='testing session edit')
        initial_sessions = StudySession.objects.count()
        response = self.client.post(reverse('study:edit_session', args=[session.pk]), {
            'date': datetime.now().date(),
            'duration': 5.0,
            'subject': subj.id ,
            'notes':'fergfs'
        })
        #redirect con successo
        self.assertEqual(response.status_code, 302)
        self.assertEqual(StudySession.objects.count(), initial_sessions)


    def test_edit_session_invalid(self):
        self.client.login(username='usernametesting', password='beepboop')
        
        subj = Subject.objects.create(name='matematica', created_by=self.user)
        session= StudySession.objects.create(user=self.user, subject =subj, duration = 2.0, date=datetime.now().date(), notes='testing session edit')

        response = self.client.post(reverse('study:edit_session', args=[session.pk]), {
            'date': datetime.now().date(),
            'duration': 26.0,
            'subject': subj.id ,
            'notes':'fergfs'
        })
       #sessione di studio non modificata
        self.assertEqual(response.status_code, 200)
        self.assertEqual(session.duration, 2)

    def test_export_list(self):
        self.client.login(username='usernametesting', password='beepboop')
        
        subj = Subject.objects.create(name='matematica', created_by=self.user)
        session= StudySession.objects.create(user=self.user, subject =subj, duration = 2.0, date=datetime.now().date(), notes='testing session export')

        response=self.client.get(reverse('study:export_list'))
        self.assertEqual(response.status_code, 200)