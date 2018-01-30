from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse

from record.models import PracticeSession


class IndexView(generic.ListView):
  template_name = 'record/index.html'
  context_object_name = 'practice_session_list'

  def get_queryset(self):
    """Return the current sessions"""
    return PracticeSession.objects.all()


class DetailView(generic.DetailView):
  model = PracticeSession
  template_name = 'record/detail.html'
  context_object_name = 'practice_session'

  def get_queryset(self):
    # TODO - leaving this for when I want to start building more rules about what details can be seen and when.
    return PracticeSession.objects.all()


def create_practice_session_quick(request):
  print("TODO - logging framework - practiceTypeQuick:{0} startQuick:{1}"
        .format(request.POST['practiceTypeQuick'], request.POST['startQuick']))

  practice_session = PracticeSession()
  practice_session.type = request.POST['practiceTypeQuick']
  practice_session.start = request.POST['startQuick']
  #practice_session.finish = request.POST['finish']
  practice_session.save()
  return HttpResponseRedirect(reverse('record:detail', kwargs={'pk': practice_session.id}))


def create_practice_session(request):
  print("TODO - logging framework - practiceType:{0} start:{1}".format(request.POST['practiceType'], request.POST['start']))

  practice_session = PracticeSession()
  practice_session.type = request.POST['practiceType']
  practice_session.start = request.POST['start']
  #practice_session.finish = request.POST['finish']
  practice_session.save()
  return HttpResponseRedirect(reverse('record:detail', kwargs={'pk': practice_session.id}))

