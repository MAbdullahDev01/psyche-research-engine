from fastapi import APIRouter, Request, status

from app.core.security import verify_clerk_webhook
from app.services.user_services import add_user, delete_user, update_user

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/clerk", status_code=status.HTTP_200_OK)
async def clerk_webhook(request: Request) -> dict[str, bool]:
    event = verify_clerk_webhook(await request.body(), request.headers)
    event_type = event.get("type")

    handlers = {
        "user.created": add_user,
        "user.updated": update_user,
        "user.deleted": delete_user,
    }
    handler = handlers.get(event_type)

    # Valid, signed events that this version does not consume are acknowledged.
    # Returning 2xx prevents Clerk from retrying events the app intentionally ignores.
    if handler is not None:
        handler(event)

    return {"received": True}
