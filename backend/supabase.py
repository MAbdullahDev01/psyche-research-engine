from supabase import create_client, Client
from backend.app.config import settings

supabase : Client = create_client(
    settings.PUBLIC_SUPABASE_URL,
    settings.PUBLIC_SUPABASE_PUBLISHABLE_KEY
    )