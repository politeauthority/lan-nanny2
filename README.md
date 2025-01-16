# Lan Nanny v0.0.0.43

![Build Main](https://github.com/politeauthority/lan-nanny2/actions/workflows/push-main.yaml/badge.svg)

Lan Nanny identifies, scans and helps organize devices on a single network, or many.
## Development
### CICD
#### Typical Process
 - Create a PR on the `stage` branch from a feature branch.
 - Once tests pass, merge to `stage`
 - When we've vetted items in the `stage` branch we will merge down to `main`.


## This Wave
Feature/ Port Scan
- [ ] Get API to return appopriate candidates for the Scanner to Map
- [ ] Parse port scan data as it applies to Lan Nanny
- [ ] Ensure `DevicePorts` get saved
- [ ] Ensure `ScanPorts` get saved