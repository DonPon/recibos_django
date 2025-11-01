import subprocess
import threading
import sys
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from datetime import date, timedelta

from src.src_email import send_email
from src.ai_utils import ask_gemini, ask_apertus
from recibos_django.mixins import EnvContextMixin
from newsletter.prompts import instructions_gaby, prompt_gaby, instructions_franz, prompt_franz


NEWSLETTERS = [
    {"id": 1, "title": "Boletín Semanal de Propiedades CDMX", "recipient": "gaby"},
    {"id": 2, "title": "Zurich Weekend Newsletter", "recipient": "franz"},
]

class NewsletterView(View, EnvContextMixin):
    def get(self, request, newsletter_id=None):
        # Check if the request is to send all newsletters
        if 'send/all/' in request.path:
            try:
                to_email_gaby = User.objects.get(username='franz').email
                to_email_franz = User.objects.get(username='franz').email

                self.send_newsletter_gaby(to_email_gaby)
                self.send_newsletter_franz(to_email_franz)

                return JsonResponse({"status": "success", "message": "All newsletters sent successfully."},
                                    status=200)
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)

        # Check if a newsletter_id is provided to send a specific newsletter
        if newsletter_id:
            try:
                # Get the email addresses of the users
                to_email_gaby = User.objects.get(username='franz').email
                to_email_franz = User.objects.get(username='franz').email

                # Send a specific newsletter
                newsletter = next((n for n in NEWSLETTERS if n["id"] == int(newsletter_id)), None)
                if not newsletter:
                    return JsonResponse({"status": "error", "message": "Newsletter not found."},
                                        status=404)

                if newsletter["recipient"] == "gaby":
                    self.send_newsletter_gaby(to_email_gaby)
                elif newsletter["recipient"] == "franz":
                    self.send_newsletter_franz(to_email_franz)
                
                return JsonResponse({"status": "success", "message": f"Newsletter '{newsletter['title']}' sent successfully."},
                                    status=200)
            except Exception as e:
                # Handle any errors and return a failure response
                return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
        # If no newsletter_id is provided, display the list of newsletters
        return render(request, 'newsletter_list.html', {"newsletters": NEWSLETTERS})


    def send_newsletter_gaby(self, to_email):
        # Generate the newsletter
        newsletter_status_gaby, newsletter_text_gaby = ask_gemini(prompt=prompt_gaby, instructions=instructions_gaby)

        # Send the email
        send_email(subject="Boletin Semanal", body=newsletter_text_gaby, to_email=to_email, is_html=True, cc_email=False)


    def send_newsletter_franz(self, to_email):
        # Generate the newsletter
        newsletter_status_franz, newsletter_text_franz = ask_gemini(prompt=prompt_franz, instructions=instructions_franz)

        # Send the email
        send_email(subject="Zurich Weekend Newsletter", body=newsletter_text_franz, to_email=to_email, is_html=True, cc_email=False)
