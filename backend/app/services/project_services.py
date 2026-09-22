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
        print(f"Error adding project: {e}")

def get_project_by_id(project_id: str, user_id: str):
    try:
        response = (
            supabase.table("projects")
            .select("*")
            .eq("id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        if response.data:
            return response.data[0]
        else:
            return None
    except Exception as e:
        print(f"Error retrieving project: {e}")
        return None

def list_projects(user_id: str):
    try:
        response = (
            supabase.table("projects")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return response.data
    except Exception as e:
            print(f"Error retrieving projects: {e}")
            return {"error": "Failed to retrieve projects."}