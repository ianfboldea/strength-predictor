from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('predictions', views.PredictionView.as_view(), name='predictions'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]
