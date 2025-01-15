--- 
--- Migration 4
--- Lan Nanny Core tables
---
---
--- Create Device  
---
CREATE TABLE IF NOT EXISTS device_ports (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    device_id INTEGER,
    device_mac_id INTEGER NOT NULL,
    status VARCHAR,
    last_seen TIMESTAMP,
    first_seen TIMESTAMP,
    protocol VARCHAR,
    port_id INTEGER NOT NULL,
    services TEXT,
    reason VARCHAR,
    current_state VARCHAR,
    UNIQUE (device_mac_id, protocol, port_id)
);
