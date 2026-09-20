create table users (
  clerk_id text primary key,
  first_name text,
  last_name text,
  image_url text,
  created_at timestamptz default now()
);