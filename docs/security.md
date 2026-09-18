# Security model

The primary threat is hostile third-party content crossing into model instructions. Retrieved data stays in an
explicit evidence boundary and may not change the audit task, invoke tools, request secrets, or override system
and plugin instructions.

Other controls include verified TLS, finite time and byte limits, explicit error states, no authenticated
crawling, ignored local outputs, and tool-free specialist agents. See the repository `SECURITY.md` for reporting.

