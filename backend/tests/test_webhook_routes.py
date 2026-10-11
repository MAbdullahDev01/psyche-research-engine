from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.api.webhooks import clerk as webhook_routes


def test_user_created_event_is_dispatched(monkeypatch):
    monkeypatch.setattr(
        webhook_routes,
        "verify_clerk_webhook",
        Mock(return_value={"type": "user.created", "data": {"id": "user_123"}}),
    )
    add_user = Mock()
    monkeypatch.setattr(webhook_routes, "add_user", add_user)

    response = TestClient(app).post("/api/webhooks/clerk", content=b"{}")

    assert response.status_code == 200
    assert response.json() == {"received": True}
    add_user.assert_called_once()


def test_unknown_valid_event_is_acknowledged_without_mutation(monkeypatch):
    monkeypatch.setattr(
        webhook_routes,
        "verify_clerk_webhook",
        Mock(return_value={"type": "organization.created", "data": {"id": "org_123"}}),
    )
    add_user = Mock()
    update_user = Mock()
    delete_user = Mock()
    monkeypatch.setattr(webhook_routes, "add_user", add_user)
    monkeypatch.setattr(webhook_routes, "update_user", update_user)
    monkeypatch.setattr(webhook_routes, "delete_user", delete_user)

    response = TestClient(app).post("/api/webhooks/clerk", content=b"{}")

    assert response.status_code == 200
    assert response.json() == {"received": True}
    add_user.assert_not_called()
    update_user.assert_not_called()
    delete_user.assert_not_called()


def test_invalid_webhook_signature_error_is_propagated(monkeypatch):
    from fastapi import HTTPException

    monkeypatch.setattr(
        webhook_routes,
        "verify_clerk_webhook",
        Mock(side_effect=HTTPException(status_code=400, detail="Invalid signature.")),
    )

    response = TestClient(app).post("/api/webhooks/clerk", content=b"{}")

    assert response.status_code == 400
