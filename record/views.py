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


def createPracticeSession(request):
  practice_session = PracticeSession()
  practice_session.type = request.POST['practiceType']
  practice_session.start = request.POST['start']
  #practice_session.finish = request.POST['finish']
  practice_session.save()
  return HttpResponseRedirect(reverse('record:index'))

