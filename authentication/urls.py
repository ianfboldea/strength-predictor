from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]
