# MangaMood API 📖

API REST construida con **FastAPI**, conectada a **Supabase** e integrada con **IA (Groq)** para analizar reseñas de manga/manhwa y detectar su *mood* (estado de ánimo).

A diferencia de un simple análisis de sentimiento (positivo/negativo), MangaMood clasifica cada reseña dentro de **8 categorías de mood** pensadas para el mundo del manga: `emocionante`, `triste`, `oscuro`, `divertido`, `tierno`, `decepcionante`, `intenso`, `relajante`.

Incluye además un pequeño frontend (una sola página HTML, servida por la misma API) para crear, ver y eliminar reseñas sin necesidad de Swagger.

---

## Tecnologías

- **FastAPI** — framework principal de la API
- **Supabase** (PostgreSQL) — base de datos
- **Groq API** (`llama-3.3-70b-versatile`) — IA externa para clasificar el mood
- **httpx** — cliente HTTP asíncrono hacia Groq
- **HTML + CSS + JS vanilla** — frontend simple, sin frameworks

---

## Estructura del proyecto

```
mangamood-api/
│
├── core/
│   ├── __init__.py
│   └── config.py            # Carga variables de entorno
│
├── database/
│   ├── __init__.py
│   └── supabase.py           # Cliente de Supabase
│
├── routes/
│   ├── __init__.py
│   └── reviews.py            # Endpoints CRUD + /analyze
│
├── schemas/
│   ├── __init__.py
│   └── review_schema.py      # Modelos Pydantic
│
├── services/
│   ├── __init__.py
│   └── ai_service.py         # Integración con Groq (IA)
│
├── static/
│   └── index.html            # Frontend simple (servido en /app)
│
├── docs/
│   ├── supabase_schema.sql   # Script para crear la tabla
│   └── screenshots/          # Capturas de las pruebas
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd mangamood-api
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Crear la tabla en Supabase

1. Crea un proyecto en [supabase.com](https://supabase.com).
2. Ve a **SQL Editor** y ejecuta el script de `docs/supabase_schema.sql`.
3. Copia la **URL del proyecto** y la **anon key** desde *Project Settings → API*.

### 4. Obtener una API key de Groq (IA)

1. Crea una cuenta gratuita en [console.groq.com](https://console.groq.com).
2. Genera una API key en *API Keys*.

### 5. Configurar variables de entorno

Copia `.env.example` a `.env` y completa tus valores:

```bash
cp .env.example .env
```

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
GROQ_API_KEY=tu_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

### 6. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Documentación interactiva (Swagger): http://127.0.0.1:8000/docs
- Frontend simple: http://127.0.0.1:8000/app

---

## Endpoints

| Método | Endpoint | Descripción |
| --- | --- | --- |
| GET | `/reviews` | Listar todas las reseñas |
| GET | `/reviews/{id}` | Obtener una reseña por ID |
| POST | `/reviews` | Crear una reseña (el mood se calcula automáticamente con IA) |
| PUT | `/reviews/{id}` | Actualizar una reseña (si cambia el contenido, se recalcula el mood) |
| DELETE | `/reviews/{id}` | Eliminar una reseña |
| POST | `/reviews/analyze` | Analizar el mood de un texto sin guardarlo |

---

## Ejemplos de uso

### Crear una reseña

```http
POST /reviews
```

```json
{
  "manga_title": "Solo Leveling",
  "author": "Sthevan",
  "content": "Cada capítulo se siente más intenso que el anterior, no puedo parar de leerlo."
}
```

Respuesta:

```json
{
  "id": 1,
  "manga_title": "Solo Leveling",
  "author": "Sthevan",
  "content": "Cada capítulo se siente más intenso que el anterior, no puedo parar de leerlo.",
  "mood": "intenso",
  "created_at": "2026-06-20T10:00:00Z"
}
```

### Analizar un texto sin guardarlo

```http
POST /reviews/analyze
```

```json
{
  "content": "El final me dejó destrozado, no esperaba esa traición."
}
```

Respuesta:

```json
{
  "content": "El final me dejó destrozado, no esperaba esa traición.",
  "mood": "oscuro"
}
```

### Petición inválida

```http
POST /reviews
```

```json
{
  "manga_title": "",
  "author": "",
  "content": ""
}
```

Respuesta:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "manga_title"],
      "msg": "Field required"
    }
  ]
}
```

---

## Pruebas de la API

### 1. Prueba válida — crear una reseña

![Crear reseña](docs/screenshots/test-valid-1.png)

### 2. Prueba válida — analizar mood con IA

![Analizar mood](docs/screenshots/test-valid-2.png)

### 3. Prueba inválida — campos vacíos

![Prueba inválida](docs/screenshots/test-invalid-1.png)

> Reemplaza las imágenes anteriores con tus propias capturas dentro de `docs/screenshots/`.

---

## Video de funcionamiento

🎥 [Ver video de demostración](https://link-a-tu-video.com)

El video muestra:
- Estructura del proyecto en el editor de código.
- Ejecución del servidor con `uvicorn main:app --reload`.
- Documentación automática en `/docs`.
- Una prueba válida y una inválida.
- Los datos guardados en la tabla `reviews` de Supabase.
- El endpoint `/reviews/analyze` funcionando con IA.

---

## Notas

- El archivo `.env` **no** se sube al repositorio; usa `.env.example` como referencia.
- Si la IA no puede clasificar el texto (error de red, key inválida, etc.), la reseña se guarda igual con `mood: "indefinido"` para que la API nunca se caiga por un fallo externo.
- El frontend en `/app` es intencionalmente simple: una sola página HTML con fetch a la API, sin frameworks ni build step.
