from fastapi import APIRouter, HTTPException

from database.supabase import supabase
from schemas.review_schema import (
    AnalyzeRequest,
    AnalyzeResponse,
    ReviewCreate,
    ReviewOut,
    ReviewUpdate,
)
from services.ai_service import analyze_mood

router = APIRouter(prefix="/reviews", tags=["Reviews"])

TABLE = "reviews"


@router.get("", response_model=list[ReviewOut])
async def listar_reviews():
    """Lista todas las reseñas, de la más reciente a la más antigua."""
    result = supabase.table(TABLE).select("*").order("id", desc=True).execute()
    return result.data


@router.get("/{review_id}", response_model=ReviewOut)
async def obtener_review(review_id: int):
    """Obtiene una reseña por su ID."""
    result = supabase.table(TABLE).select("*").eq("id", review_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    return result.data[0]


@router.post("", response_model=ReviewOut, status_code=201)
async def crear_review(review: ReviewCreate):
    """
    Crea una reseña nueva. El campo `mood` se calcula automáticamente
    enviando el contenido de la reseña a la IA (Groq).
    """
    if not review.author.strip() or not review.content.strip():
        raise HTTPException(
            status_code=422,
            detail="Los campos author y content son obligatorios",
        )

    mood = await analyze_mood(review.content)

    nuevo = {
        "manga_title": review.manga_title,
        "author": review.author,
        "content": review.content,
        "mood": mood,
    }

    result = supabase.table(TABLE).insert(nuevo).execute()
    return result.data[0]


@router.put("/{review_id}", response_model=ReviewOut)
async def actualizar_review(review_id: int, review: ReviewUpdate):
    """Actualiza una reseña existente. Si cambia el contenido, se vuelve a calcular el mood."""
    existente = supabase.table(TABLE).select("*").eq("id", review_id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    cambios = {k: v for k, v in review.model_dump().items() if v is not None}

    if not cambios:
        raise HTTPException(status_code=422, detail="No se enviaron campos para actualizar")

    if "content" in cambios:
        cambios["mood"] = await analyze_mood(cambios["content"])

    result = supabase.table(TABLE).update(cambios).eq("id", review_id).execute()
    return result.data[0]


@router.delete("/{review_id}", status_code=204)
async def eliminar_review(review_id: int):
    """Elimina una reseña por su ID."""
    existente = supabase.table(TABLE).select("*").eq("id", review_id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    supabase.table(TABLE).delete().eq("id", review_id).execute()
    return None


@router.post("/analyze", response_model=AnalyzeResponse)
async def analizar_review(payload: AnalyzeRequest):
    """
    Analiza cualquier texto con la IA y devuelve su mood,
    SIN guardarlo en la base de datos. Útil para probar el
    clasificador de forma aislada.
    """
    mood = await analyze_mood(payload.content)
    return {"content": payload.content, "mood": mood}
