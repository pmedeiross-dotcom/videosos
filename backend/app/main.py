import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner

from .schemas import FilmBrief

load_dotenv()

app = FastAPI(
    title="AI Film Studio API",
    version="0.1.0",
    description="Agente de pré-produção cinematográfica com OpenAI.",
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
    return {"status": "ok", "service": "ai-film-studio-api"}


@app.post("/api/films/plan")
async def plan_film(brief: FilmBrief):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Configure OPENAI_API_KEY no ambiente do backend.",
        )

    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise HTTPException(
            status_code=503,
            detail="Configure OPENAI_MODEL com um modelo habilitado na sua conta API.",
        )

    director = Agent(
        name="Diretor de produção cinematográfica",
        model=model,
        instructions=(
            "Você é um diretor de cinema e produtor executivo. "
            "Transforme o briefing em um plano de pré-produção executável. "
            "Responda em português brasileiro. "
            "Entregue: logline, sinopse, direção criativa, personagens "
            "com descrição visual consistente, cenas numeradas com objetivo "
            "dramático, local, horário, personagens presentes, ação, diálogos, "
            "planos de câmera e duração estimada. Inclua notas de produção "
            "e riscos de custo. Não invente que vídeos foram gerados: esta etapa "
            "é somente planejamento. Preserve coerência histórica quando o tema "
            "for histórico ou bíblico e sinalize escolhas ficcionais."
        ),
    )

    prompt = (
        "Crie o plano de produção para este filme. "
        "Retorne uma estrutura clara em Markdown.\n\n"
        f"Título: {brief.title}\n"
        f"Premissa: {brief.premise}\n"
        f"Duração alvo: {brief.target_duration_minutes} minutos\n"
        f"Idioma: {brief.language}\n"
        f"Estilo visual: {brief.visual_style}\n"
        f"Público: {brief.audience}\n"
        f"Orçamento: {brief.budget_mode}\n"
    )

    try:
        result = await Runner.run(director, prompt)
        return {
            "status": "planned",
            "project": brief.model_dump(),
            "plan_markdown": str(result.final_output),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Falha ao gerar o plano: {type(exc).__name__}",
        ) from exc
