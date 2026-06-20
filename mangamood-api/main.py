from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import reviews

app = FastAPI(
    title="MangaMood API",
    description=(
        "API REST para registrar reseñas de manga/manhwa y analizar "
        "automáticamente su 'mood' (estado de ánimo) usando IA."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reviews.router)

# Frontend simple servido por la misma API en /app
app.mount("/app", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def root():
    return {
        "message": "MangaMood API funcionando 📖",
        "docs": "/docs",
        "frontend": "/app",
    }
