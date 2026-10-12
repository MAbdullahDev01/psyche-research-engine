import logging

from fastapi import APIRouter, Request, status

from app.core.security import verify_clerk_webhook
from app.services.user_services import (
    add_user,
    delete_user,
    has_processed_clerk_event,
    mark_clerk_event_processed,
    update_user,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/clerk", status_code=status.HTTP_200_OK)
async def clerk_webhook(request: Request) -> dict[str, bool]:
    try:
        event = verify_clerk_webhook(
            await request.body(),
            request.headers,
        )
        event_type = event.get("type")

        header_event_id = request.headers.get("svix-id")
        payload_event_id = event.get("id")

        event_id = header_event_id or (
            payload_event_id
            if isinstance(payload_event_id, str)
            else None
        )

        logger.info(
            "Verified Clerk webhook: type=%s, event_id=%s",
            event_type,
            event_id,
        )

        if event_id and has_processed_clerk_event(event_id):
            return {"received": True, "duplicate": True}

        handlers = {
            "user.created": add_user,
            "user.updated": update_user,
            "user.deleted": delete_user,
        }

        handler = handlers.get(event_type)

        if handler is not None:
            handler(event)

        if event_id:
            mark_clerk_event_processed(
                event_id,
                str(event_type or "unknown"),
            )

        return {"received": True}

    except Exception:
        logger.exception("Clerk webhook processing failed")
        raise
