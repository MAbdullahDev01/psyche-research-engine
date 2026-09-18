import json

from fastapi import HTTPException, status
from svix.webhooks import Webhook, WebhookVerificationError

from app.core.config import settings

# Verifies incoming Clerk webhooks using the signing secret from the Clerk dashboard.
def verify_clerk_webhook(payload: bytes, headers: dict) -> dict:

    signing_secret = settings.CLERK_WEBHOOK_SIGNING_SECRET

    if not signing_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clerk webhook signing secret is not configured.",
        )

    webhook = Webhook(signing_secret)

    try:
        # Verify the raw payload against the Svix signature.
        webhook.verify(payload, headers)
    except WebhookVerificationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid webhook signature: {exc}",
        )

    try:
        event = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid webhook payload: {exc}",
        )

    if not isinstance(event, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook payload must be a JSON object.",
        )

    return event