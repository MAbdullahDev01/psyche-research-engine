from fastapi import Request, Header, HTTPException
from clerk_backend_api.security import AuthenticateRequestOptions, authenticate_request

from app.core.clerk import clerk_client
from app.db.supabase import supabase

def add_user(event):
    try:
        response = (
            supabase.table("users")
            .insert(
                {
                    "clerk_id": event.get("data", {}).get("id"),
                    "first_name": event.get("data", {}).get("first_name"),
                    "last_name": event.get("data", {}).get("last_name"),
                    "image_url" : event.get("data", {}).get("image_url"),
                }
            )
            .execute()
        )
    except Exception as e:
        print(f"Error adding user: {e}")

def delete_user(event):
    try:
        response = (
            supabase.table("users")
            .delete()
            .eq("clerk_id", event.get("data", {}).get("id"))
            .execute()
        )
    except Exception as e:
        print(f"Error deleting user: {e}")

def update_user(event):
    try:
        response = (
            supabase.table("users")
            .update(
                {
                    "first_name": event.get("data", {}).get("first_name"),
                    "last_name": event.get("data", {}).get("last_name"),
                    "image_url" : event.get("data", {}).get("image_url"),
                }
            )
            .eq("clerk_id", event.get("data", {}).get("id"))
            .execute()
        )
    except Exception as e:
        print(f"Error updating user: {e}")

def get_current_user(request: Request):
    auth_state = clerk_client.authenticate_request(request, AuthenticateRequestOptions(
            authorized_parties=["http://localhost:3000"]
        ))

    if not auth_state.is_authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return auth_state