# Migration guide

For the product rename introduced in 1.1, see [Renaming to Proofline](renaming-to-proofline.md).

## Public beta 0.9 to stable 1.0

No audit, evidence, finding, score, agent, skill, or campaign schema major version changes are required for this
migration. The score algorithm remains version 5.0. Existing 0.9 commands and namespaced plugin skills continue
to work.

Upgrade in an isolated environment, run `proofline doctor --json`, validate stored payloads against the
schemas shipped with 1.0, and rerun representative synthetic audits before adopting the release. Integrations
should branch on `schema_version` and `score_version`, preserve non-observed collection states, and avoid
deserializing unknown fields into executable behavior.

Version 1.0 changes the package classifier from Alpha to Production/Stable and introduces the 1.x compatibility
and deprecation policy. It does not add publishing adapters, authenticated crawling, automatic live-account
mutation, or guarantees about rankings, compliance, or revenue.
