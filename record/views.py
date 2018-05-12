from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils.timezone import utc
import datetime

from record.models import PracticeSession


class IndexView(generic.ListView):
  template_name = 'record/index.html'
  context_object_name = 'practice_session_list'

  def get_queryset(self):
    """Return the current sessions"""
    return PracticeSession.objects.all().order_by('start')


class DetailView(generic.DetailView):
  model = PracticeSession
  template_name = 'record/detail.html'
  context_object_name = 'practice_session'

  def get_queryset(self):
    # TODO - leaving this for when I want to start building more rules about what details can be seen and when.
    return PracticeSession.objects.all()


class UpdateForm(forms.ModelForm):
  # TODO - review this in detail https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/
  type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  start = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget())
  finish = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(), required=False)
  rating = forms.ChoiceField(widget=forms.RadioSelect(),
                             choices=((1, 1), (2, 2), (3, 3), (4,4), (5,5)),
                             required=False)

  class Meta:
    model = PracticeSession
    fields = ['start', 'finish', 'type', 'rating', 'feel', 'attemptCount']


class CreateView(generic.CreateView):
  model = PracticeSession
  template_name = 'record/create.html'
  context_object_name = 'practice_session'
  success_url = reverse_lazy('record:index')
  form_class = UpdateForm

  def form_valid(self, form):
    temp = form.save(commit=False)
    # TODO - still having difficult modify the form's validation logic
    return super().form_valid(form)


class UpdateView(generic.UpdateView):
  model = PracticeSession
  template_name = 'record/update.html'
  context_object_name = 'practice_session'
  success_url = reverse_lazy('record:index')
  form_class = UpdateForm

  def form_valid(self, form):
    #print(form)
    temp = form.save(commit=False)
    # TODO - still having difficult modify the form's validation logic
    return super().form_valid(form)


def create_practice_session_quick(request):
  print("TODO - logging framework - practiceTypeQuick:{0} startQuick:{1}"
        .format(request.POST['practiceTypeQuick'], request.POST['startQuick']))

  practice_session = PracticeSession()
  practice_session.type = request.POST['practiceTypeQuick']
  practice_session.start = request.POST['startQuick']
  practice_session.save()
  return HttpResponseRedirect(reverse('record:detail', kwargs={'pk': practice_session.id}))


def finish_practice_session_now(request, pk):
  practice_session = get_object_or_404(PracticeSession, pk=pk)
  print("TODO - logging framework - practiceType:{0} start:{1}".format(practice_session.type, practice_session.start))

  practice_session.finish = datetime.datetime.utcnow().replace(tzinfo=utc)
  practice_session.save()
  return HttpResponseRedirect(reverse('record:updateClass', kwargs={'pk': practice_session.id}))


def update_practice_session(request, pk):
  practice_session = get_object_or_404(PracticeSession, pk=pk)
  print("TODO - logging framework - practiceType:{0} start:{1}".format(practice_session.type, practice_session.start))
  print(request.POST)

  practice_session.type = request.POST['typeInput']
  practice_session.start = request.POST['startInput']
  practice_session.finish = request.POST['finishInput']
  practice_session.rating = request.POST['ratingInput']
  practice_session.feel = request.POST['feelInput']
  practice_session.attemptCount = request.POST['attemptInput']
  practice_session.save()
  return HttpResponseRedirect(reverse('record:detail', kwargs={'pk': practice_session.id}))