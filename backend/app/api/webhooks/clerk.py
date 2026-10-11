from fastapi import APIRouter, Request, status

from app.core.security import verify_clerk_webhook
from app.services.user_services import (
    add_user,
    delete_user,
    has_processed_clerk_event,
    mark_clerk_event_processed,
    update_user,
)

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/clerk", status_code=status.HTTP_200_OK)
async def clerk_webhook(request: Request) -> dict[str, bool]:
    event = verify_clerk_webhook(await request.body(), request.headers)
    event_type = event.get("type")
    header_event_id = request.headers.get("svix-id")
    payload_event_id = event.get("id")
    event_id = header_event_id or (payload_event_id if isinstance(payload_event_id, str) else None)

    if event_id and has_processed_clerk_event(event_id):
        return {"received": True, "duplicate": True}

    handlers = {
        "user.created": add_user,
        "user.updated": update_user,
        "user.deleted": delete_user,
    }
    handler = handlers.get(event_type)

    # Valid, signed events this version does not consume are acknowledged and
    # recorded, preventing pointless retries for unsupported event types.
    if handler is not None:
        handler(event)

    if event_id:
        mark_clerk_event_processed(event_id, str(event_type or "unknown"))

    return {"received": True}
