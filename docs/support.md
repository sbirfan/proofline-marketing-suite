# Support policy

Proofline Marketing Suite 2.x supports CPython 3.11, 3.12, and 3.13 on Linux, macOS, and Windows. The core package
uses the Python standard library. The `browser` and `reports` extras are optional; their upstream system
requirements also apply.

Patch releases receive compatible bug and security fixes. Minor 2.x releases may add functionality without
intentionally breaking the documented CLI, skill names, or versioned output contracts. A deprecation is
documented in the changelog for at least one minor release before removal. Breaking contract changes require a
new major package version, except when an urgent security fix cannot safely preserve the old behavior.

Schemas and score algorithms have independent embedded versions. Consumers must reject unsupported major
schema versions and must not compare scores across score versions without an explicit migration. Additive
optional fields may appear in minor releases; consumers should validate with the published schema.

Use GitHub issues for reproducible bugs and feature requests and private security advisories for vulnerabilities.
Include `proofline doctor --json`, a synthetic reproduction, expected and actual behavior, and output
schema/score versions. Never submit credentials, private client content, or unredacted audit data.
