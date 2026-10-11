import os

# Settings are loaded during app imports; use non-secret placeholders in tests.
os.environ.setdefault("PUBLIC_SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("PUBLIC_SUPABASE_PUBLISHABLE_KEY", "test-publishable-key")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")
os.environ.setdefault("PUBLIC_CLERK_PUBLISHABLE_KEY", "test-clerk-publishable-key")
os.environ.setdefault("CLERK_SECRET_KEY", "sk_test_placeholder")
os.environ.setdefault("CLERK_WEBHOOK_SIGNING_SECRET", "whsec_placeholder")
os.environ.setdefault("OPENALEX_API_KEY", "test-openalex-key")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", "http://localhost:3000")
os.environ.setdefault("CLERK_AUTHORIZED_PARTIES", "http://localhost:3000")
