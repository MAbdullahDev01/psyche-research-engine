from fastapi import HTTPException

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
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to create project"
        )

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
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to get project"
        )

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
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to list projects"
        )

def update_a_project(title: str, question : str, project_id : str, user_id : str):
    try:
        response = (
            supabase.table("projects")
            .update(
                {
                "title": title,
                "question" : question,
                }
            )
            .eq("id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
    except Exception as e:
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to update project"
        )

def delete_a_project(project_id : str, user_id : str):
    try:
            response = (
                supabase.table("projects")
                .delete()
                .eq("id", project_id)
                .eq("user_id", user_id)
                .execute()
            )
    except Exception as e:
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to delete project"
        )