# HN Scraper (FastAPI)

Rastreador web que extrae las **primeras 30 entradas** de [Hacker News](https://news.ycombinator.com) y permite:

- **> 5 palabras** en el título → ordenadas por **comentarios** (desc).
- **≤ 5 palabras** en el título → ordenadas por **puntos** (desc).

Al contar palabras se **ignoran símbolos/puntuación**.  
Ej.: `Este es un ejemplo autoexplicativo` → **5** palabras.  
(`auto-explicativo` cuenta como una palabra: se limpian símbolos y se queda `autoexplicativo`).

---

## Stack

- Python 3.12
- FastAPI + Jinja2 (plantillas)
- httpx + BeautifulSoup4 + lxml (scraping)
- cachetools (caché en memoria, TTL 120 s)
- pytest + respx (tests, sin tocar la red) ← *opcional pero recomendado*

---

## Ejecutar en local

> **Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# si PowerShell bloquea la activación:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

pip install -r requirements.txt
uvicorn app.main:app --reload
Abre:

App: http://127.0.0.1:8000

Docs OpenAPI: http://127.0.0.1:8000/docs

Si el puerto 8000 está ocupado:

uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
Endpoints
/ – Listado completo (30 primeras entradas por rank).

/filter/long – Títulos > 5 palabras, orden comentarios desc (desempate por puntos y luego rank).

/filter/short – Títulos ≤ 5 palabras, orden puntos desc (desempate por comentarios y luego rank).

/api/entries – API JSON con elementos {rank, title, points, comments}.

Ejemplo de respuesta (/api/entries):

[
  {"rank": 1, "title": "RFC 9839 and Bad Unicode", "points": 100, "comments": 31},
  {"rank": 2, "title": "Manim: Animation engine for explanatory math videos", "points": 218, "comments": 42}
]
Regla de conteo de palabras
Se separa por espacios.

Cada token se normaliza a solo letras (isalpha()), descartando símbolos/puntuación.

"C++ best practices" → tokens ["C", "best", "practices"] → 3 palabras.

"One-two three" → "Onetwo" y "three" → 2 palabras.

"auto-explicativo" → "autoexplicativo" → 1 palabra.

Implementación en app/wordutils.py.

Arquitectura

app/
  main.py            # FastAPI + rutas HTML/API
  hn_scraper.py      # scraping + caché (TTL 120 s)
  service.py         # lógica de filtrado y ordenación
  wordutils.py       # conteo de palabras (ignorando símbolos)
  models.py          # dataclass HNEntry
  templates/index.html
  static/styles.css
Scraping: se seleccionan filas tr.athing y su subtext adyacente.

Caché: TTLCache(maxsize=1, ttl=120) para reducir latencia y no saturar HN.

Ordenaciones: estables y con desempates (rank como último criterio).

Tests (recomendados)
Tras añadir la carpeta tests/:

pytest -q
Cobertura sugerida:

test_wordutils.py → normalización y conteo de palabras.

test_service.py → filtros y ordenaciones según reglas.

test_scraper_parsing.py → parseo con HTML simulado usando respx (sin red).

Buenas prácticas aplicadas
Separación clara de capas (scraping / dominio / web).

Tipado y @dataclass para el modelo HNEntry.

Evitar repetición (función única de conteo de palabras).

Caché de resultados por 120 s → rendimiento y respeto al sitio origen.

Endpoints HTML y API JSON para facilitar verificación manual y automática.

Problemas conocidos / Decisiones
Si la estructura HTML de HN cambiara, los selectores podrían requerir ajuste.

En “discuss” (sin comentarios) se toma comments = 0.

Fallbacks: si no hay score o comments, los valores son 0.

Desarrollo
Historial de commits incremental y descriptivo.

.gitignore evita subir .venv, __pycache__, etc.

Puedes ajustar el TTL de la caché en app/hn_scraper.py.

Licencia
MIT
