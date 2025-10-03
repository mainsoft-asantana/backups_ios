inventory_insert = """
INSERT INTO inventory (number_ip, state)
VALUES (%s, %s)
ON CONFLICT (number_ip) DO UPDATE SET state = EXCLUDED.state
RETURNING id;
"""

system_insert = """
INSERT INTO system (name, state)
VALUES (%s, %s)
ON CONFLICT (name) DO UPDATE
SET state = EXCLUDED.state
RETURNING id;
"""

version_insert = """
INSERT INTO version (name, state)
VALUES (%s, %s)
ON CONFLICT (name) DO UPDATE
SET state = EXCLUDED.state
RETURNING id;
"""

model_insert = """
INSERT INTO model (name, state)
VALUES (%s, %s)
ON CONFLICT (name) DO UPDATE
SET state = EXCLUDED.state
RETURNING id;
"""

type_insert = """
INSERT INTO type (name, state)
VALUES (%s, %s)
ON CONFLICT (name) DO UPDATE
SET state = EXCLUDED.state
RETURNING id;
"""

hostname_insert = """
INSERT INTO hostname (name, state)
VALUES (%s, %s)
ON CONFLICT (name) DO UPDATE
SET state = EXCLUDED.state
RETURNING id;
"""


backups_insert = """
INSERT INTO backups (
    system_id,
    inventory_id,
    version_id,
    model_id,
    type_id,
    hostname_id,

    created_at,
    state,
    backups
) VALUES %s
ON CONFLICT (system_id, inventory_id, version_id, model_id, type_id, hostname_id, created_at) DO UPDATE
SET
    state = EXCLUDED.state,
    backups = EXCLUDED.backups

"""