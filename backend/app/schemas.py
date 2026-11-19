from pydantic import BaseModel, Field


class FilmBrief(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    premise: str = Field(min_length=10, max_length=6000)
    target_duration_minutes: int = Field(default=3, ge=1, le=30)
    language: str = Field(default="pt-BR", max_length=20)
    visual_style: str = Field(
        default="cinematográfico realista",
        max_length=160,
    )
    audience: str = Field(default="público geral", max_length=160)
    budget_mode: str = Field(default="baixo custo", max_length=40)


class FilmPlan(BaseModel):
    project_title: str
    logline: str
    synopsis: str
    creative_direction: str
    characters: list[dict]
    scenes: list[dict]
    production_notes: list[str]
    estimated_cost_notes: list[str]
