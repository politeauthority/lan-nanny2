--- 
--- Migration 2
--- Lan Nanny Core tables
---
---
--- Create devices
---
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    vendor VARCHAR,
    ip VARCHAR,
    last_seen TIMESTAMP,
    first_seen TIMESTAMP,
    hide BOOLEAN DEFAULT False,
    favorite BOOLEAN DEFAULT False,
    icon VARCHAR,
    favorite BOOLEAN,
    last_port_scan TIMESTAMP,
    last_port_scan_id INTEGER,
    first_port_scan_id INTEGER,
    port_scan_lock BOOLEAN,
    host_names VARCHAR
    kind VARCHAR
    identified BOOLEAN,
    deleted BOOLEAN DEFAULT False
);



-- End file: politeauthority/lan-nanny/src/lan_nanny/migrations/data/sql/up/2.sql
