# Agent design

Specialists consume collected evidence and deterministic findings. They may interpret, prioritize, and propose
tests; they may not crawl independently, convert missing data into facts, or calculate the canonical score.

Each agent states its accepted evidence, prohibited assumptions, output expectations, and the shared
prompt-injection boundary. Tool access is empty by default. Any future tool addition requires a threat-model
update and a least-privilege justification.

