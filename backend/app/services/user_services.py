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