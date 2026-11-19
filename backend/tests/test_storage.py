import json

from app.storage import get_project, initialize_database, list_projects, save_project


def test_project_round_trip(tmp_path):
    database = tmp_path / "test.db"
    initialize_database(database)
    brief = {"title": "Filme de teste", "premise": "Uma história de teste."}

    saved = save_project(brief, "# Plano\nCena 1", db_path=database)

    loaded = get_project(saved["id"], db_path=database)
    assert loaded is not None
    assert loaded["title"] == "Filme de teste"
    assert loaded["brief"] == brief
    assert loaded["plan_markdown"] == "# Plano\nCena 1"
    assert len(list_projects(db_path=database)) == 1


def test_missing_project_returns_none(tmp_path):
    database = tmp_path / "test.db"
    initialize_database(database)
    assert get_project("inexistente", db_path=database) is None
