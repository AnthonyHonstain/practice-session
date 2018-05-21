from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import PracticeSession


class PracticeSessionModelTests(TestCase):

  def test_practice_session_created_with_only_type_and_start(self):
    time = timezone.now()
    create_session = PracticeSession.objects.create(start=time, type='TestSession')

    session = PracticeSession.objects.get(pk=create_session.id)
    self.assertIsNone(session.finish)
    self.assertIsNone(session.rating)
    self.assertIsNone(session.feel)
    self.assertIsNone(session.attemptCount)


class DetailViewTests(TestCase):

  def test_unknown_practice_session(self):
    response = self.client.get(reverse('record:detail', kwargs={'pk': 1}))
    self.assertEqual(response.status_code, 404)

  def test_empty_practice_session(self):
    session = create_practice_session('TestSession')
    response = self.client.get(reverse('record:detail', kwargs={'pk': session.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['practice_session'].type, session.type)


def create_practice_session(new_type):
  time = timezone.now()
  session = PracticeSession.objects.create(start=time, type=new_type)
  return session
