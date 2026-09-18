# Technical Audit

Version 0.3.0 expands the deterministic layer that runs before specialist interpretation. Checks are stable,
source-backed facts or bounded observations. The analyzer does not infer rankings, conversion lift, business
quality, or search-engine access from an audit crawler's blocked request.

## Scored inputs

Scoring uses explicit finding IDs rather than a generic severity formula. Adding a new finding does not alter
a score until its penalty is registered and tested. Coverage varies by category and by the evidence sources that
were successfully observed.

## Technical-agent hand-off

The orchestrator produces a brief containing finding IDs, evidence URLs, collection status, render mode,
limitations, prohibited actions, and the central untrusted-content policy. Raw page text is deliberately absent.
The repository defines input and result schemas, but the Python CLI does not call an external model.

## Report behavior

Markdown findings are sorted by severity and stable ID. Reports display score version, evidence availability,
confidence, coverage, and methodology so a partial technical result cannot appear to be a full marketing audit.
