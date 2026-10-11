from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import projects as project_routes
from app.services.user_services import get_current_user


def _user():
    return SimpleNamespace(payload={"sub": "user_test_123"})


def setup_function():
    app.dependency_overrides[get_current_user] = _user


def teardown_function():
    app.dependency_overrides.clear()


def test_create_project_returns_created_status_and_authenticated_owner(monkeypatch):
    project = {
        "id": "project-1",
        "title": "Sleep and memory",
        "question": "How does sleep affect memory?",
        "status": "draft",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }
    add_project = Mock(return_value=project)
    monkeypatch.setattr(project_routes, "add_project", add_project)

    response = TestClient(app).post(
        "/api/projects/",
        json={"title": " Sleep and memory ", "question": " How does sleep affect memory? "},
    )

    assert response.status_code == 201
    assert response.json()["id"] == "project-1"
    add_project.assert_called_once_with(
        "Sleep and memory", "How does sleep affect memory?", "user_test_123"
    )


def test_missing_project_returns_real_404(monkeypatch):
    monkeypatch.setattr(project_routes, "get_project_by_id", Mock(return_value=None))

    response = TestClient(app).get("/api/projects/not-found")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found."


def test_update_missing_project_returns_real_404(monkeypatch):
    update = Mock(return_value=None)
    monkeypatch.setattr(project_routes, "update_a_project", update)

    response = TestClient(app).patch(
        "/api/projects/not-found",
        json={"title": "Updated title", "question": "Updated question"},
    )

    assert response.status_code == 404
    update.assert_called_once_with(
        "Updated title", "Updated question", "not-found", "user_test_123"
    )


def test_project_database_failure_is_not_returned_as_success(monkeypatch):
    from fastapi import HTTPException

    monkeypatch.setattr(
        project_routes,
        "list_projects",
        Mock(side_effect=HTTPException(status_code=500, detail="Database unavailable.")),
    )

    response = TestClient(app).get("/api/projects/")

    assert response.status_code == 500
    assert response.json()["detail"] == "Database unavailable."


def test_cannot_list_papers_for_another_users_project(monkeypatch):
    monkeypatch.setattr(project_routes, "get_project_by_id", Mock(return_value=None))

    response = TestClient(app).get("/api/projects/foreign-project/papers")

    assert response.status_code == 404
