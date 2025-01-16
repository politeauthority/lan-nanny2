--- 
--- Migration 3
--- Lan Nanny Scan Tables
---
---
--- Create scan_hosts
---

DROP TABLE IF EXISTS scans;

CREATE TABLE IF NOT EXISTS scan_hosts (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scan_agent VARCHAR NOT NULL,
    scan_type VARCHAR NOT NULL,
    hosts_found INTEGER NOT NULL,
    scan_command VARCHAR,
    scan_time INTEGER,
    raw_data TEXT
);


-- End file: politeauthority/lan-nanny/src/lan_nanny/migrations/data/sql/up/3.sql
