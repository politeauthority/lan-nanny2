--- 
--- Migration 5
--- Lan Nanny Core tables
---
---
--- Create Device Kinds
---
CREATE TABLE IF NOT EXISTS device_kinds (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR UNIQUE,
    icon VARCHAR
);
