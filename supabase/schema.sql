-- Supabase schema for Food Help Crawler

create table if not exists public.posts (
  id bigint generated always as identity primary key,
  platform text not null,
  external_id text not null,
  author text,
  url text,
  content text,
  lang text default 'en',
  created_at timestamptz default now(),
  posted_at timestamptz,
  raw jsonb
);

create unique index if not exists posts_unique_platform_external_id
  on public.posts(platform, external_id);

create table if not exists public.events (
  id bigint generated always as identity primary key,
  post_id bigint references public.posts(id) on delete cascade,
  title text,
  description text,
  organizer text,
  source_type text default 'social', -- social | rss | directory | submission
  event_date_start timestamptz,
  event_date_end timestamptz,
  tz text,
  address text,
  city text,
  state text,
  postal_code text,
  latitude double precision,
  longitude double precision,
  verified boolean default false,
  verification_note text,
  region text, -- e.g., 'GA', 'Grand Rapids, MI', 'West Michigan'
  created_at timestamptz default now()
);

create index if not exists events_date_idx on public.events(event_date_start);
create index if not exists events_geo_idx on public.events(latitude, longitude);
create index if not exists events_region_idx on public.events(region);

-- Public submissions for the web form
create table if not exists public.submissions (
  id bigint generated always as identity primary key,
  created_at timestamptz default now(),
  title text,
  description text,
  organizer text,
  event_date_start timestamptz,
  event_date_end timestamptz,
  address text,
  city text,
  state text,
  postal_code text,
  latitude double precision,
  longitude double precision,
  contact_url text,
  submitted_by text, -- optional email/handle
  verified boolean default false
);

-- Enable RLS
alter table public.posts enable row level security;
alter table public.events enable row level security;
alter table public.submissions enable row level security;

-- Read policies (public read)
create policy "read_all_events" on public.events
  for select using (true);
create policy "read_all_posts" on public.posts
  for select using (true);

-- Allow anonymous inserts on submissions (for /submit form)
create policy "anon_submit" on public.submissions
  for insert to anon with check (true);

-- Optional: public can read only verified submissions (keep private otherwise)
create policy "read_verified_only" on public.submissions
  for select using (verified = true);

