import httpx

from core.config import settings

# Categorías cerradas de "mood" pensadas para reseñas de manga/manhwa.
# En lugar de un sentimiento binario (positivo/negativo), clasificamos
# la reseña dentro del universo de sensaciones que deja una buena lectura.
MOODS = [
    "emocionante",
    "triste",
    "oscuro",
    "divertido",
    "tierno",
    "decepcionante",
    "intenso",
    "relajante",
]

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


async def analyze_mood(text: str) -> str:
    """
    Envía el texto de una reseña a la API de Groq y devuelve una
    etiqueta de "mood" (estado de ánimo) tomada de una lista cerrada
    de categorías. Si la IA falla o no responde una categoría válida,
    se devuelve "indefinido".
    """
    prompt = (
        "Eres un clasificador de reseñas de manga y manhwa. "
        f"Responde EXCLUSIVAMENTE con una palabra de esta lista: {', '.join(MOODS)}. "
        "No agregues explicaciones, signos de puntuación ni texto adicional.\n\n"
        f'Reseña: "{text}"'
    )

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 10,
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(GROQ_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        raw = data["choices"][0]["message"]["content"].strip().lower()
        raw = raw.strip(" .,!?\"'")

        for mood in MOODS:
            if mood in raw:
                return mood

    except Exception:
        # Si la IA externa falla, la API no debe romperse: se guarda
        # la reseña igual con un mood por defecto.
        pass

    return "indefinido"
