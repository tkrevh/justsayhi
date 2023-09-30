from django.urls import path

from . import views

urlpatterns = [
    path('', views.slack_webhook, name='justsayhi-index'),
    path('oauth', views.slack_oauth, name='justsayhi-oauth'),
    path('interactive', views.slack_receive_slash_command, name='justsayhi-interactive'),
]