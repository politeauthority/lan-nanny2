--- 
--- Migration 3
--- Lan Nanny Core tables
---
---
--- Create devices
---

ALTER TABLE device_macs
    ADD column port_scan_enabled BOOLEAN default True;