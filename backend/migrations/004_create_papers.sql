CREATE TABLE papers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    openalex_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT,
    authors JSONB,
    publication_year INTEGER,
    landing_page_url TEXT,
    doi TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);