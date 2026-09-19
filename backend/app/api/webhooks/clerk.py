from fastapi import APIRouter, Request, status

from app.core.security import verify_clerk_webhook
from app.services.user_services import add_user, delete_user

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

@router.post("/clerk")
async def clerk_webhook(request: Request, status_code=status.HTTP_200_OK):

    payload = await request.body()
    headers = request.headers

    # for debugging purposes
    # print(headers)
    # print(payload)

    # Verify the Clerk webhook
    event = verify_clerk_webhook(payload, headers) # type: ignore

    match event.get("type"):
        # Add the user to the database
        case "user.created":
            add_user(event)
        case "user.updated":
            ...
        case "user.deleted":
            delete_user(event)
        case _:
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
            return {status_code : f"Unhandled webhook event type: {event.get('type')}"}
    

    return {status_code : "Webhook received successfully."}