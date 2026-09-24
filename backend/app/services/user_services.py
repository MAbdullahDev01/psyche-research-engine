from fastapi import Request, Header, HTTPException
from clerk_backend_api.security import AuthenticateRequestOptions, RequestState

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

        raise HTTPException(
            status_code=500,
            detail="Failed to add user"
        )

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
        # Error logging for debugging purposes
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )
        

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
        # Error logging for debugging purposes
        print(f"Error updating user: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to update user"
        )

def get_current_user(request: Request) -> RequestState:
    auth_state = clerk_client.authenticate_request(request, AuthenticateRequestOptions(
            authorized_parties=["http://localhost:3000"]
        ))

    if not auth_state.is_authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return auth_state