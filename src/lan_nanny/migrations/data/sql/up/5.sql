--- 
--- Migration 5
--- Lan Nanny Scan Tables
---
---
--- Create scan_host_results
---


CREATE TABLE IF NOT EXISTS scan_host_results (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scan_host_id INTEGER NOT NULL,
    device_mac_id INTEGER NOT NULL,
    device_id INTEGER
);

-- End file: politeauthority/lan-nanny/src/lan_nanny/migrations/data/sql/up/5.sql
