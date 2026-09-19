# Public beta guide

Version 0.9.0 is the public beta for evaluation and integration feedback. Install Python 3.11–3.13, create an
isolated environment, install the package, and run `proofline doctor`. Add `[browser]` only for explicit
render fallback and `[reports]` only for PDF output.

The beta compatibility contract covers the documented CLI, JSON schemas, observation states, score scale, and
plugin skill names. Schema and scoring versions remain embedded in outputs. Pre-1.0 releases may still make
documented breaking changes; consumers should validate versions instead of silently accepting unknown ones.

When reporting a problem, include `proofline doctor --json`, the command used, the output status/reason,
and the smallest synthetic reproduction. Diagnostics contain no environment variables, credentials, filesystem
paths, URLs, or audit content. Never attach secrets or unredacted customer data.

The public examples use `.test` URLs and synthetic content. Skill-routing evaluation cases include both
should-invoke and should-not-invoke prompts, especially for actions that would publish, send, launch, or mutate
an external account.
