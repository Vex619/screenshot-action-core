# Security Policy

## Reporting a vulnerability

Please do not open a public issue for a suspected security vulnerability. Contact the maintainer privately through the security contact configured for this repository.

When reporting, include the affected version, a minimal reproduction, impact, and any suggested mitigation. Please redact secrets and personal information.

## Scope

The core library is designed to analyze text locally and does not transmit input over the network. Optional adapters may introduce external services; those adapters must document what data is sent and require explicit configuration.
