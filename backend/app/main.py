import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import FilmBrief

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

app = FastAPI(
    title="AI Film Studio API",
    version="0.2.0",
    description="Estúdio particular de pré-produção com modelo local via Ollama.",
)

origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ai-film-studio-api",
        "ai_provider": "ollama-local",
        "model": OLLAMA_MODEL,
    }


@app.post("/api/films/plan")
async def plan_film(brief: FilmBrief):
    system_prompt = (
        "Você é um diretor de cinema, roteirista e produtor executivo. "
        "Transforme o briefing em um plano de pré-produção claro e executável. "
        "Responda sempre em português brasileiro. "
        "Entregue: logline, sinopse, direção criativa, personagens com descrições "
        "visuais consistentes, cenas numeradas, objetivo dramático, local, horário, "
        "personagens presentes, ação, diálogos, planos de câmera e duração estimada. "
        "Inclua notas de produção e alternativas econômicas. "
        "Não afirme que imagens ou vídeos foram gerados: esta etapa é somente planejamento. "
        "Em temas históricos ou bíblicos, preserve a coerência dos fatos conhecidos "
        "e identifique claramente qualquer licença ficcional."
    )
    user_prompt = (
        "Crie o plano de produção para este filme em Markdown.\n\n"
        f"Título: {brief.title}\n"
        f"Premissa: {brief.premise}\n"
        f"Duração alvo: {brief.target_duration_minutes} minutos\n"
        f"Idioma: {brief.language}\n"
        f"Estilo visual: {brief.visual_style}\n"
        f"Público: {brief.audience}\n"
        f"Orçamento: {brief.budget_mode}\n"
    )

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0)) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "options": {"temperature": 0.7},
                },
            )
            response.raise_for_status()
            result = response.json()
        answer = result.get("message", {}).get("content", "").strip()
        if not answer:
            raise HTTPException(status_code=502, detail="O modelo local retornou uma resposta vazia.")
        return {
            "status": "planned",
            "provider": "ollama-local",
            "model": OLLAMA_MODEL,
            "project": brief.model_dump(),
            "plan_markdown": answer,
        }
    except httpx.ConnectError as exc:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao Ollama. Instale-o e inicie o serviço local.",
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"O Ollama retornou HTTP {exc.response.status_code}. Confira se o modelo foi baixado.",
        ) from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=504,
            detail="O modelo local demorou demais para responder. Tente um briefing menor.",
        ) from exc
