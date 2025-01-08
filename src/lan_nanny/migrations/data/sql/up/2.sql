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
    vendor_id INTEGER,
    ip VARCHAR,
    last_seen TIMESTAMP,
    first_seen TIMESTAMP,
    hide BOOLEAN DEFAULT False,
    icon VARCHAR,
    last_port_scan TIMESTAMP,
    port_scan_lock BOOLEAN,
    host_names VARCHAR,
    kind_id INTEGER,
    identified BOOLEAN,
    deleted BOOLEAN DEFAULT False
);

CREATE TABLE IF NOT EXISTS device_macs (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    device_id INTEGER,
    vendor_id INTEGER,
    ip VARCHAR,
    last_seen TIMESTAMP,
    first_seen TIMESTAMP,
    hide BOOLEAN DEFAULT False,
    icon VARCHAR,
    last_port_scan TIMESTAMP,
    port_scan_lock BOOLEAN,
    host_names VARCHAR,
    kind_id INTEGER,
    identified BOOLEAN,
    deleted BOOLEAN DEFAULT False
);

CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    names text,
);



-- End file: politeauthority/lan-nanny/src/lan_nanny/migrations/data/sql/up/2.sql
