from django.urls  import path

from . import views


app_name = 'record'
urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('createPracticeSession', views.createPracticeSession, name='create')
]
