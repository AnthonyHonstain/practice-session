import datetime

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


class IndexViewTests(TestCase):

  def test_index_with_no_data(self):
    response = self.client.get(reverse('record:index'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['practice_session_list'].count(), 0)

  def test_index_with_several_sessions(self):
    session1 = create_practice_session('TestSession1')
    session2 = create_practice_session('TestSession2')
    response = self.client.get(reverse('record:index'))
    self.assertEqual(response.status_code, 200)
    # This final assertQuersetEqual should be simpler than this
    # https://docs.djangoproject.com/en/2.0/topics/testing/tools/#django.test.TransactionTestCase.assertQuerysetEqual
    self.assertQuerysetEqual(response.context['practice_session_list'], [repr(r) for r in [session1, session2]])


class DetailViewTests(TestCase):

  def test_unknown_practice_session(self):
    response = self.client.get(reverse('record:detail', kwargs={'pk': 1}))
    self.assertEqual(response.status_code, 404)

  def test_get_basic_practice_session(self):
    session = create_practice_session('TestSession')
    response = self.client.get(reverse('record:detail', kwargs={'pk': session.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['practice_session'].type, session.type)


class CreateViewTests(TestCase):

  def test_create_practice_session(self):
    response = self.client.get(reverse('record:createClass'))
    self.assertEqual(response.status_code, 200)

  def test_create_practice_session_with_data(self):
    response = self.client.post(reverse('record:createClass'),
                                {'type': 'CreateTest', 'start_0': '2018-05-21', 'start_1': '05:05:00',
                                 'rating': 3, 'feel': 'Good', 'attemptCount': 1})
    self.assertEqual(response.status_code, 302)
    session = PracticeSession.objects.filter(type='CreateTest').first()
    self.assertEqual(session.type, 'CreateTest')
    self.assertEqual(session.start, datetime.datetime(2018, 5, 21, 12, 5, tzinfo=timezone.utc))
    self.assertIsNone(session.finish)
    self.assertEqual(session.rating, 3)
    self.assertEqual(session.feel, 'Good')
    self.assertEqual(session.attemptCount, 1)


class UpdateViewTests(TestCase):

  def test_unknown_practice_session(self):
    response = self.client.get(reverse('record:updateClass', kwargs={'pk': 1}))
    self.assertEqual(response.status_code, 404)

  def test_get_update_basic_practice_session(self):
    session = create_practice_session('TestSession')
    response = self.client.get(reverse('record:updateClass', kwargs={'pk': session.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['practice_session'].type, session.type)

  def test_post_update_practice_session(self):
    orig_session = create_practice_session('OrigUpdate')
    response = self.client.post(reverse('record:updateClass', kwargs={'pk': orig_session.pk}),
                                {'type': 'UpdateTest',
                                 'start_0': '2018-05-21', 'start_1': '05:05:00',
                                 'finish_0': '2018-05-21', 'finish_1': '05:10:00',
                                 'rating': 3, 'feel': 'Good', 'attemptCount': 1})
    self.assertEqual(response.status_code, 302)

    self.assertIsNone(PracticeSession.objects.filter(type='OrigUpdate').first())
    session = PracticeSession.objects.filter(type='UpdateTest').first()
    self.assertEqual(session.id, orig_session.id)
    self.assertEqual(session.type, 'UpdateTest')
    self.assertEqual(session.start, datetime.datetime(2018, 5, 21, 12, 5, tzinfo=timezone.utc))
    self.assertEqual(session.finish, datetime.datetime(2018, 5, 21, 12, 10, tzinfo=timezone.utc))
    self.assertEqual(session.rating, 3)
    self.assertEqual(session.feel, 'Good')
    self.assertEqual(session.attemptCount, 1)


def create_practice_session(new_type):
  time = timezone.now()
  session = PracticeSession.objects.create(start=time, type=new_type)
  return session
