from fastapi import HTTPException, Request, status
from clerk_backend_api.security import AuthenticateRequestOptions, RequestState

from app.core.clerk import clerk_client
from app.core.config import settings
from app.db.supabase import supabase


def _user_data(event: dict) -> dict:
    data = event.get("data")
    clerk_id = data.get("id") if isinstance(data, dict) else None
    if not isinstance(clerk_id, str) or not clerk_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Clerk webhook event is missing data.id.",
        )
    return {
        "clerk_id": clerk_id,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "image_url": data.get("image_url"),
    }


def add_user(event: dict) -> None:
    try:
        supabase.table("users").upsert(_user_data(event), on_conflict="clerk_id").execute()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add user.",
        ) from exc


def delete_user(event: dict) -> None:
    user = _user_data(event)
    try:
        supabase.table("users").delete().eq("clerk_id", user["clerk_id"]).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user.",
        ) from exc


def update_user(event: dict) -> None:
    # Upsert makes webhook retries and out-of-order user.updated events safe when
    # the initial user.created delivery was missed.
    try:
        supabase.table("users").upsert(_user_data(event), on_conflict="clerk_id").execute()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user.",
        ) from exc


def get_current_user(request: Request) -> RequestState:
    auth_state = clerk_client.authenticate_request(
        request,
        AuthenticateRequestOptions(authorized_parties=settings.clerk_authorized_parties),
    )

    if not auth_state.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return auth_state


def has_processed_clerk_event(event_id: str) -> bool:
    try:
        response = (
            supabase.table("clerk_webhook_events")
            .select("event_id")
            .eq("event_id", event_id)
            .maybe_single()
            .execute()
        )
        return bool(response.data)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check Clerk webhook idempotency.",
        ) from exc


def mark_clerk_event_processed(event_id: str, event_type: str) -> None:
    try:
        supabase.table("clerk_webhook_events").insert(
            {"event_id": event_id, "event_type": event_type}
        ).execute()
    except Exception as exc:
        # Concurrent deliveries can both pass the initial lookup. A duplicate
        # insert is safe only if the unique event row now exists.
        try:
            response = (
                supabase.table("clerk_webhook_events")
                .select("event_id")
                .eq("event_id", event_id)
                .maybe_single()
                .execute()
            )
            if response.data:
                return
        except Exception:
            pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record Clerk webhook processing.",
        ) from exc
