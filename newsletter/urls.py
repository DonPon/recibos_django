from django.urls import path
from newsletter.views import NewsletterView

app_name = 'newsletter'

urlpatterns = [
    path('send/', NewsletterView.as_view(), name='newsletter'),
]
