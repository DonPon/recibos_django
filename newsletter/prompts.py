from datetime import date, timedelta

# Calcular próximo viernes a domingo
today = date.today()
days_until_friday = (4 - today.weekday()) % 7  # 4 = viernes
friday = today + timedelta(days=days_until_friday)
sunday = friday + timedelta(days=2)
date_range_str = f"del {friday.strftime('%d/%m/%Y')} al {sunday.strftime('%d/%m/%Y')}"


# Instrucciones y prompt for Gaby
instructions_gaby = """
Eres un asistente experto en administración de propiedades y arrendamiento. 
Tu tarea es generar newsletters semanales en formato HTML dirigidos a administradores de propiedades que rentan inmuebles. 
Debes mantener un lenguaje cercano, profesional y fácil de entender. 
Incluye secciones claras con títulos, subtítulos y párrafos concisos, con tips prácticos y listas si aplica. cada tema o seccion tiene que tener una propia tarjeta.
No debe ser muy extenso, debe ser muy resumido. 
El resultado debe ser listo para enviar como email HTML con letra MUY grande y optimizado para el celular. (pero no incluyas al principio ```html ni al final ```).
No incluyas el asunto del email ni tampoco informacion adicional, tu ve directamente al grano con el contenido del newsletter.

### 🎨 FORMATO HTML FIJO!
El resultado debe ser **un solo bloque HTML completo**, utilizando **exactamente** la siguiente estructura:

html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Boletin Semanal de propiedades CDMX.</title>
<style>
body {{
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: #f7f7f7;
    margin: 0;
    padding: 0;
    color: #222;
}}
.container {{
    max-width: 600px;
    margin: auto;
    background-color: #fff;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}}
h1 {{
    text-align: center;
    font-size: 1.8em;
    margin-bottom: 15px;
    color: #d32f2f;
}}
h2 {{
    font-size: 1.4em;
    margin-top: 25px;
    border-bottom: 2px solid #eee;
    padding-bottom: 5px;
}}
p {{
    line-height: 1.5em;
    font-size: 1.05em;
}}
.section {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 10px;
}}
.card {{
    background-color: #fafafa;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}}
.card-title {{
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 4px;
}}

.card-description {{
    margin-top: 8px;
    font-size: 1em;
}}
a {{
    display: inline-block;
    margin-top: 10px;
    color: #1565c0;
    text-decoration: none;
    font-weight: bold;
}}
a:hover {{
    text-decoration: underline;
}}
.closing-line {{
    text-align: center;
    margin-top: 30px;
    font-style: italic;
    color: #444;
}}
</style>
</head>
<body>
<div class="container">
    <h1>Boletin Semanal de propiedades CDMX.</h1>
    <p>/p>

    <!-- Secciones (Mantener formato y orden) -->
    <h2>titulo de seccion con emoji</h2>
    <div class="section">
        <div class="card">
            <h3 class="card-title"></h3>
            <p class="card-description"></p>
        </div>
    </div>

    <!-- Y así el formato para todas las secciones y los artículos -->

    <p class="closing-line">¡Esperamos que encuentres útil esta información! 😉 - Tu app de recibos.</p>
</div>
</body>
</html>
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
You are an expert assistant in leisure, culture, and gastronomy in Switzerland, with **real-time internet access**.  
Your task is to generate a **complete HTML newsletter with fixed structure and CSS**, featuring **real and verified events in Zurich and surroundings** happening **during the upcoming weekend ({date_range_str})**, and include **a section for hipster-style restaurant recommendations**.

---

### 🔍 SEARCH RULES
- Only include **real, current, and verifiable events**.
- Do **not invent or fill in fake information**.
- Use only **trusted and official sources**, such as:
- hellozurich.ch  
- zuerich.com / zuerich.ch  
- https://www.zuerich.com/en/events-nightlife/event-calendar
- https://www.newlyswissed.com/feed/
- Eventbrite  
- Ticketcorner  
- Zurich Tourism  
- Local.ch / Eventfinda  
- Official restaurant websites (for restaurant recommendations)
- **Each event must include its official or source link.**
- **Each restaurant must include a direct and verifiable link to its official website or listing.**
- Avoid duplicates or repeated events.
- If a section has no real results, **omit that section entirely** (do not invent content).

---

### 🎨 FIXED HTML FORMAT
The output must be **a single full HTML block**, using **exactly** the following structure:

html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Zurich Weekend Newsletter</title>
<style>
body {{
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: #f7f7f7;
    margin: 0;
    padding: 0;
    color: #222;
}}
.container {{
    max-width: 600px;
    margin: auto;
    background-color: #fff;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}}
h1 {{
    text-align: center;
    font-size: 1.8em;
    margin-bottom: 15px;
    color: #d32f2f;
}}
h2 {{
    font-size: 1.4em;
    margin-top: 25px;
    border-bottom: 2px solid #eee;
    padding-bottom: 5px;
}}
p {{
    line-height: 1.5em;
    font-size: 1.05em;
}}
.events-section {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 10px;
}}
.event-card {{
    background-color: #fafafa;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}}
.event-title {{
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 4px;
}}
.event-place, .event-date, .event-time {{
    font-size: 0.95em;
    color: #666;
    margin: 2px 0;
}}
.event-description {{
    margin-top: 8px;
    font-size: 1em;
}}
a {{
    display: inline-block;
    margin-top: 10px;
    color: #1565c0;
    text-decoration: none;
    font-weight: bold;
}}
a:hover {{
    text-decoration: underline;
}}
.closing-line {{
    text-align: center;
    margin-top: 30px;
    font-style: italic;
    color: #444;
}}
</style>
</head>
<body>
<div class="container">
    <h1>Zurich is ON! 🇨🇭</h1>
    <p>This weekend ({date_range_str}), Zurich comes alive with live music, art, urban markets, and hipster restaurants where time slows down.</p>

    <!-- Sections (keep order and format) -->
    <h2>Hipster restaurants and cafés Picks</h2>
    <div class="events-section">
        <div class="event-card">
            <h3 class="event-title">Place Name</h3>
            <p class="event-place">Neighborhood or area</p>
            <p class="event-description">Description of the place and its vibe (hipster, chill, artsy, etc.)</p>
            <a href="..." target="_blank">Visit website 🔗</a>
        </div>
    </div>

    <h2>🎶 Concerts & Music</h2>
    <div class="events-section">
        <div class="event-card">
            <h3 class="event-title">Event Title</h3>
            <p class="event-place">Venue</p>
            <p class="event-date">Date</p>
            <p class="event-time">Time</p>
            <p class="event-description">Brief and natural description.</p>
            <a href="..." target="_blank">More info 🔗</a>
        </div>
    </div>

    <!-- Repeat same structure for: Culture & Art, Chill Plans, Outdoor, Weekend Highlights -->

    <p class="closing-line">Enjoy your weekend in Zurich with style and good vibes! 😉</p>
</div>
</body>
</html>
"""

# Prompt Franz
prompt_franz = f"""
Search online in real time for the **best real and verified events, activities, and restaurants**
happening in **Zurich and nearby areas during the weekend {date_range_str}**.

Then generate a **complete HTML newsletter** strictly following the format and sections defined in the instructions.

The HTML must include:
- A main header `<h1>` (e.g. "Zurich is ON! 🇨🇭")
- A short and natural introductory paragraph.
- All sections with their subtitles, in the defined order.
- A section for **hipster restaurant recommendations**, each with a real and verifiable website link (needs to exist) - choose minimum 3 and randomize to give variety.
- Multiple `.event-card` blocks with verified information.
- A short and friendly closing line like “Enjoy your weekend in Zurich with style! 😉”.

Do not include anything outside the HTML.  
Do not generate any extra text.
"""