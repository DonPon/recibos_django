from django.urls import path
from newsletter.newsletter_views import NewsletterView

app_name = 'newsletter'

urlpatterns = [
    path('', NewsletterView.as_view(), name='newsletter_list'),  # List newsletters
    path('send/', NewsletterView.as_view(), name='send_all_newsletters'),  # Send all newsletters
    path('send/<int:newsletter_id>/', NewsletterView.as_view(), name='send_newsletter'),  # Send specific newsletter
]