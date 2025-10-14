from django.urls import path
from newsletter.newsletter_views import NewsletterView

app_name = 'newsletter'

urlpatterns = [
    path('send/', NewsletterView.as_view(), name='newsletter'),
]
