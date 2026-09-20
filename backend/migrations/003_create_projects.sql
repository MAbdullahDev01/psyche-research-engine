create table projects (
    id uuid primary key default gen_random_uuid(),

    user_id TEXT not null references users(clerk_id) on delete cascade,

    title text not null,
    question text not null,

    status text not null default 'draft'
        check (status in ('draft', 'active', 'completed')),

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);