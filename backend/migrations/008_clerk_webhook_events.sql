CREATE TABLE public.clerk_webhook_events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE public.clerk_webhook_events ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.clerk_webhook_events FROM anon, authenticated;
