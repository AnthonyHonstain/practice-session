from django.urls  import path

from . import views


app_name = 'record'
urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('<int:pk>', views.DetailView.as_view(), name='detail'),
  path('createPracticeSession', views.create_practice_session, name='create'),
  path('createPracticeSessionQuick', views.create_practice_session_quick, name='createQuick'),
]
