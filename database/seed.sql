-- Dev/test seed: one full Portfolio -> Building -> Floor -> Zone chain.
INSERT INTO portfolios (id, name, code)
VALUES ('11111111-1111-1111-1111-111111111111', 'Acme West Campus', 'ACME-WEST')
ON CONFLICT (id) DO NOTHING;

INSERT INTO buildings (id, portfolio_id, name, code, address)
VALUES ('22222222-2222-2222-2222-222222222222', '11111111-1111-1111-1111-111111111111', 'Tower 1', 'T1', '1 Main St')
ON CONFLICT (id) DO NOTHING;

INSERT INTO floors (id, building_id, name, code)
VALUES ('33333333-3333-3333-3333-333333333333', '22222222-2222-2222-2222-222222222222', 'Floor 3', 'T1-F3')
ON CONFLICT (id) DO NOTHING;

INSERT INTO zones (id, floor_id, name, code, area, occupancy)
VALUES ('44444444-4444-4444-4444-444444444444', '33333333-3333-3333-3333-333333333333', 'Conference Room A', 'Z-3F-01', 42.5, 12)
ON CONFLICT (id) DO NOTHING;
