from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from datetime import date, timedelta

from src.src_email import send_email
from src.ai_utils import ask_gemini, ask_apertus

# Calcular próximo viernes a domingo
today = date.today()
days_until_friday = (4 - today.weekday()) % 7  # 4 = viernes
friday = today + timedelta(days=days_until_friday)
sunday = friday + timedelta(days=2)
date_range_str = f"del {friday.strftime('%d/%m/%Y')} al {sunday.strftime('%d/%m/%Y')}"

class NewsletterView(View):
    def get(self, request):
        try:
            # Get the email addresses of the users
            to_email_gaby = User.objects.get(username='gaby').email
            to_email_franz = User.objects.get(username='franz').email

            # Instrucciones y prompt for Gaby
            instructions_gaby = """
            Eres un asistente experto en administración de propiedades y arrendamiento. 
            Tu tarea es generar newsletters semanales en formato HTML dirigidos a administradores de propiedades que rentan inmuebles. 
            Debes mantener un lenguaje cercano, profesional y fácil de entender. 
            Incluye secciones claras con títulos, subtítulos y párrafos concisos, con tips prácticos y listas si aplica. 
            No debe ser muy extenso, debe ser muy resumido. 
            El resultado debe ser listo para enviar como email HTML con letra MUY grande y optimizado para el celular. (pero no incluyas al principio ```html ni al final ```).
            No incluyas el asunto del email ni tampoco informacion adicional, tu ve directamente al grano con el contenido del newsletter.
            """

            prompt_gaby = """
            Crea un newsletter completo para Gaby, administradora de propiedades, incluyendo: 
            1. Noticias recientes del sector inmobiliario y arrendamiento.
            2. Actualizaciones importantes del SAT relacionadas con renta y tributación.
            3. Trucos y consejos para optimizar ingresos y ahorrar dinero.
            4. Tips de mantenimiento preventivo y gestión eficiente de inquilinos.
            Agrega un título atractivo, un resumen inicial y subtítulos para cada sección.
            """

            # Instrucciones y prompt for Franz
            instructions_franz = f"""
            Eres un asistente experto en ocio, cultura y eventos en Suiza, con acceso a internet. 
            Tu tarea es buscar información actual en línea sobre eventos y actividades en Zúrich y alrededores 
            específicamente para el próximo fin de semana ({date_range_str}).  
            Usa fuentes confiables como hellozurich.ch, zurich.ch, Eventbrite, Ticketcorner, etc.  
            Incluye únicamente eventos reales y confirmados con nombre, lugar, fecha y breve descripción.  

            Después de hacer la búsqueda, genera un newsletter HTML optimizado para celular, 
            con letra MUY grande, formato limpio y visualmente atractivo (NO INCLUYAS ```html ni ``` al final).  

            El tono debe ser cercano, divertido y natural, con un toque elegante suizo.  
            Incluye secciones con subtítulos llamativos como:  
            - 🎶 Conciertos y música  
            - 🎨 Cultura y arte  
            - 🍷 Plan relax  
            - 🌲 Al aire libre  
            - 🔥 Destacados del finde  

            Usa párrafos cortos, listas breves cuando sea útil, y emojis donde encajen.  
            No inventes información ni pongas eventos genéricos.  
            No incluyas el asunto del correo ni información adicional; solo el contenido HTML del newsletter.
            """

            prompt_franz = f"""
            Haz una búsqueda en internet para encontrar los mejores eventos, planes y actividades en Zúrich y alrededores 
            que ocurran el fin de semana {date_range_str}.  
            Luego crea un newsletter en HTML con:
            - Un título atractivo.
            - Un breve resumen inicial.
            - Secciones con subtítulos, nombres reales de eventos y fechas exactas.
            - Formato optimizado para celular, con letra grande y párrafos breves.
            - Un cierre con sugerencia o frase amable para el lector.

            Ejemplo de tono: 
            "Este finde ({date_range_str}) Zúrich se pone bueno: conciertos junto al lago, ferias gastronómicas y exposiciones que valen cada minuto 😎".
            """

            # Generar el newsletter usando instrucciones
            newsletter_status_gaby, newsletter_text_gaby = ask_gemini(prompt=prompt_gaby, instructions=instructions_gaby)
            newsletter_status_franz, newsletter_text_franz = ask_gemini(prompt=prompt_franz, instructions=instructions_franz)

            # Send the emails
            send_email(subject="Newsletter", body=newsletter_text_gaby, to_email=to_email_gaby, is_html=True, cc_email=False)
            send_email(subject="Newsletter", body=newsletter_text_franz, to_email=to_email_franz, is_html=True, cc_email=False)

            # Return a success response
            return JsonResponse({"status": "success", "message": "Newsletter sent successfully."}, status=200)
        except Exception as e:
            # Handle any errors and return a failure response
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        