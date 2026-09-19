from app.db.supabase import supabase

def add_user(event):
    
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