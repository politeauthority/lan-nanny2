--- 
--- Migration 4
--- Lan Nanny Scan Tables
---
---
--- Create scan_ports
---


CREATE TABLE IF NOT EXISTS scan_ports (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scan_agent VARCHAR NOT NULL,
    scan_type VARCHAR NOT NULL,
    device_id INTEGER NOT NULL,
    ports_found INTEGER NOT NULL,
    scan_command VARCHAR,
    scan_time INTEGER,
    raw_data TEXT
);


-- End file: politeauthority/lan-nanny/src/lan_nanny/migrations/data/sql/up/4.sql
