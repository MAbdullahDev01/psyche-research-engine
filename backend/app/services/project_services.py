from app.db.supabase import supabase

def add_project(title : str, question : str, user_id : str):
    try:
        response = (
            supabase.table("projects")
            .insert(
                {
                    "user_id": user_id,
                    "title": title,
                    "question": question,
                }
            )
            .execute()
        )
    except Exception as e:
        print(f"Error adding user: {e}")