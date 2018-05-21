from django.urls  import path

from . import views


app_name = 'record'
urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('create', views.CreateView.as_view(), name='createClass'),
  path('<int:pk>/update', views.UpdateView.as_view(), name='updateClass'),
  path('finishNow/<int:pk>', views.finish_practice_session_now, name='finishNow'),
]
