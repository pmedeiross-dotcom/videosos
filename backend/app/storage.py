import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def database_path() -> Path:
    configured = os.getenv("FILM_STUDIO_DB_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(__file__).resolve().parents[1] / "data" / "films.db"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Path | None = None) -> None:
    with connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS film_projects (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                brief_json TEXT NOT NULL,
                plan_markdown TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_project(
    brief: dict[str, Any],
    plan_markdown: str,
    provider: str = "ollama-local",
    model: str = "qwen2.5:3b",
    db_path: Path | None = None,
) -> dict[str, Any]:
    project = {
        "id": str(uuid.uuid4()),
        "title": brief["title"],
        "brief": brief,
        "plan_markdown": plan_markdown,
        "provider": provider,
        "model": model,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with connect(db_path) as connection:
        connection.execute(
            """INSERT INTO film_projects
               (id, title, brief_json, plan_markdown, provider, model, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                project["id"],
                project["title"],
                json.dumps(brief, ensure_ascii=False),
                plan_markdown,
                provider,
                model,
                project["created_at"],
            ),
        )
    return project


def list_projects(limit: int = 50, db_path: Path | None = None) -> list[dict[str, Any]]:
    with connect(db_path) as connection:
        rows = connection.execute(
            """SELECT id, title, provider, model, created_at
               FROM film_projects ORDER BY created_at DESC LIMIT ?""",
            (max(1, min(limit, 100)),),
        ).fetchall()
    return [dict(row) for row in rows]


def get_project(project_id: str, db_path: Path | None = None) -> dict[str, Any] | None:
    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT * FROM film_projects WHERE id = ?", (project_id,)
        ).fetchone()
    if row is None:
        return None
    project = dict(row)
    project["brief"] = json.loads(project.pop("brief_json"))
    return project
