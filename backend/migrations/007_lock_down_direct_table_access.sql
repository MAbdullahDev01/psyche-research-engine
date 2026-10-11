-- Psyche uses the FastAPI backend with the Supabase service-role key.
-- Clerk users are not Supabase Auth users, so do not create permissive
-- authenticated policies based on auth.uid(). The service role bypasses RLS;
-- browser/anon/authenticated clients should not access these tables directly.
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.papers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.project_papers ENABLE ROW LEVEL SECURITY;

REVOKE ALL ON TABLE
    public.users,
    public.projects,
    public.papers,
    public.project_papers
FROM anon, authenticated;
