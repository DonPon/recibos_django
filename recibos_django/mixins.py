import os
from django.views.generic.base import ContextMixin
from dotenv import load_dotenv

load_dotenv()
to_email = os.getenv('TO_EMAIL')

dias = 40

class EnvContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ENV'] = os.getenv('ENV')
        return context