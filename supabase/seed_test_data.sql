-- Minimal seed: one GA and one GR point for UI smoke tests
insert into public.events (title, description, organizer, source_type, event_date_start, city, state, latitude, longitude, verified, region)
values
('Mobile Pantry - SW Atlanta', 'Free produce. Bring ID if you have one. First come, first served.', 'Test Org', 'submission', now() + interval '1 day', 'Atlanta', 'GA', 33.73, -84.50, true, 'GA'),
('Mobile Pantry - Grand Rapids', 'Free food distribution. Drive-thru.', 'Test Org', 'submission', now() + interval '2 days', 'Grand Rapids', 'MI', 42.963, -85.668, true, 'Grand Rapids, MI');

-- Optional: clear seed
-- delete from public.events where organizer='Test Org';
