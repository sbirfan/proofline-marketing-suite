# Proofline Marketing Suite: beginner setup and usage guide

This guide is for marketers, freelancers, business owners, and agency teams. You do not need to know how to
code. You will copy a few commands into a terminal, then use plain-language slash commands inside Claude Code.

## What you will have when you finish

You will be able to:

- audit a public website and receive evidence-backed findings and scores;
- review SEO, landing pages, brand, funnels, and confirmed competitors;
- create Markdown, JSON, HTML, and PDF reports;
- draft copy, emails, social posts, ads, launch plans, and proposals;
- keep observed facts separate from assumptions and unavailable evidence.

The software is open source. Claude access, API usage, or other services may have their own charges. The suite
does not contact prospects, send emails, publish posts, launch ads, or modify accounts automatically.

## Before you start

You need:

1. A Windows, macOS, or Linux computer.
2. An internet connection.
3. [Visual Studio Code](https://code.visualstudio.com/download).
4. [Git](https://git-scm.com/downloads).
5. [Python 3.11, 3.12, or 3.13](https://www.python.org/downloads/).
6. Claude Code, installed and signed in by following the
   [official Claude Code setup guide](https://docs.anthropic.com/en/docs/claude-code/setup).

During installation, use the normal/default options. On Windows, enable the installer option that adds Python
to `PATH` if it is offered.

## Part 1 — Download the suite

1. Open Visual Studio Code.
2. Select **Terminal → New Terminal** from the top menu.
3. Copy the command below, paste it into the terminal, and press **Enter**:

```bash
git clone https://github.com/sbirfan/proofline-marketing-suite.git
```

4. Open the downloaded folder:

```bash
cd proofline-marketing-suite
```

If Visual Studio Code asks whether you trust the folder, review the repository address and choose **Yes, I
trust the authors** only if it matches the GitHub repository above.

## Part 2 — Install the local audit tools

Choose the instructions for your computer.

### Windows PowerShell

Paste these commands one line at a time:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[reports]"
proofline doctor
```

If `py -3` is not recognized, try `python -m venv .venv`. If PowerShell blocks activation, open a normal
Command Prompt in the same folder and use `.venv\Scripts\activate.bat`.

### macOS or Linux

Paste these commands one line at a time:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[reports]"
proofline doctor
```

A successful check shows the suite version, your Python version, your operating system, and
`reports=available`. The browser extra is optional, so `browser=not installed` is not an error.

### Optional: support JavaScript-heavy websites

Most sites do not need this. If an audit says a page requires rendering, install the browser support:

```bash
python -m pip install -e ".[browser,reports]"
python -m playwright install chromium
```

Browser installation can take several minutes and uses additional disk space.

## Part 3 — Start Claude Code with the marketing suite

Keep the terminal inside the `proofline-marketing-suite` folder and run:

```bash
claude --plugin-dir .
```

Claude Code opens in the terminal. Type the following command and press **Enter**:

```text
/svgai-marketing:health
```

If the health command appears and completes, the plugin is loaded. You can type `/svgai-marketing:` to view
the available suite commands.

The product is named Proofline, but the compatible 1.x Claude command namespace remains
`/svgai-marketing:*`. It will move to `/proofline:*` only in a future major release.

## Part 4 — Run your first website audit

Use a public website you own, manage, or have permission to review. Replace `https://example.com` with the full
website address:

```text
/svgai-marketing:audit https://example.com
```

Claude may ask for permission before reading a public page or creating a local report. Read each request and
approve only the website and file actions you expect.

The audit distinguishes among:

- **Observed:** the suite successfully collected the evidence.
- **Not found:** collection succeeded, but the item was absent from the collected page.
- **Blocked:** a safety or access rule prevented collection.
- **Fetch failed:** the request failed, timed out, or returned an unusable response.
- **Render required:** the page likely needs optional browser rendering.
- **Not tested:** the audit did not have enough context or evidence to test the item.

Do not describe a blocked, failed, render-required, or not-tested result as proof that something is missing.

### A stronger first prompt

Give Claude business context so it does not have to leave important categories untested:

```text
/svgai-marketing:audit https://example.com

Audience: owners of small service businesses
Offer: a free 30-minute consultation
Primary conversion: book a consultation
Please save the audit evidence and create a client-ready PDF report.
```

The suite will not invent the audience, offer, or conversion goal from webpage copy. If you do not know an
answer, say “unknown” instead of guessing.

## Part 5 — Create reports directly from the terminal

You can also run the deterministic audit tool without opening Claude Code.

### Easy-to-read Markdown report

```bash
proofline audit https://example.com --format markdown --output report.md
```

### Client-ready PDF report

```bash
proofline audit https://example.com --format pdf --output report.pdf
```

### Web-page report

```bash
proofline audit https://example.com --format html --output report.html
```

### JavaScript-heavy page

Use this only after installing the optional browser support:

```bash
proofline audit https://example.com --browser-fallback --format pdf --output report.pdf
```

The new files appear in the `proofline-marketing-suite` folder. In Visual Studio Code, use the file list on the
left to open them. PDF output requires the `reports` extra installed in Part 2.

## Part 6 — Use a focused analysis skill

You do not need to run every skill. Choose the one that matches the job:

| Command | Use it when you want to… | Information to provide |
|---|---|---|
| `/svgai-marketing:seo` | review indexing, metadata, links, and schema | website URL or saved audit evidence |
| `/svgai-marketing:landing` | improve a landing page and form | audience, offer, primary conversion |
| `/svgai-marketing:competitors` | compare confirmed competitors | competitor URLs and comparison topics |
| `/svgai-marketing:brand` | review clarity, consistency, proof, and trust | audited material and brand context |
| `/svgai-marketing:funnel` | find journey and measurement gaps | funnel stages and conversion goals |
| `/svgai-marketing:report` | turn a saved audit into a report | path to the saved audit JSON |

Example landing-page request:

```text
/svgai-marketing:landing https://example.com

Audience: first-time home buyers
Offer: mortgage-readiness consultation
Primary conversion: schedule a call
Identify the five highest-impact improvements. Separate observed facts from recommendations.
```

Example competitor request:

```text
/svgai-marketing:competitors https://example.com

Confirmed competitors:
- https://competitor-one.example
- https://competitor-two.example

Compare positioning, proof, calls to action, and offer clarity. Do not search for or add other competitors.
```

## Part 7 — Draft campaign materials

Campaign commands create review-ready drafts. They do not publish or send anything.

| Command | Creates | Important context |
|---|---|---|
| `/svgai-marketing:copy` | copy variants | channel, audience, offer, goal, approved claims |
| `/svgai-marketing:emails` | email sequences | permission basis, sender, cadence, offer |
| `/svgai-marketing:social` | organic posts | platform, voice, goal, approved claims |
| `/svgai-marketing:ads` | ad concepts and tests | channel, budget context, exclusions, measurement |
| `/svgai-marketing:launch` | phased launch plan | timing, owners, dependencies, risks |
| `/svgai-marketing:proposal` | services proposal | client, scope, pricing inputs, approvals |

Example email request:

```text
/svgai-marketing:emails

Audience: existing customers who explicitly subscribed to product updates
Sender: SVG Example Company
Offer: free onboarding review
Goal: book a review call
Cadence: three emails over ten days
Approved claim: customers receive a written onboarding checklist
Draft only. Do not upload a list, configure automation, or send messages.
```

Example proposal request:

```text
/svgai-marketing:proposal

Client: Example Company
Goal: improve qualified demo bookings
Scope: website audit, landing-page recommendations, and a three-email draft
Timeline: four weeks
Price: $2,500 fixed fee
Exclusions: ad buying, development, and CRM changes
Create a review-ready proposal. Do not invent case studies, signatures, or legal approval.
```

Always verify claims, prices, consent, legal language, dates, and client details before using a draft.

## A simple first-week workflow

1. Run `/svgai-marketing:health`.
2. Audit your own website with audience, offer, and conversion context.
3. Read the evidence status, confidence, and coverage before the score.
4. Use `/seo` or `/landing` for one focused follow-up.
5. Generate a PDF and inspect every client-facing claim.
6. Use one campaign skill to draft a follow-up asset.
7. Have the responsible person approve the final material before any external action.

## Troubleshooting

### `git`, `python`, or `claude` is not recognized

The program is either not installed or your terminal has not picked up the new installation. Close and reopen
Visual Studio Code. If the message remains, reinstall the named program and enable its PATH option.

### `proofline` is not recognized

Return to the repository folder and activate the environment again:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS or Linux
source .venv/bin/activate
```

Then run `proofline doctor`.

### PDF output says the reporting dependency is missing

Run:

```bash
python -m pip install -e ".[reports]"
```

### The page says `render_required`

Install the browser extra from Part 2, then repeat the audit with `--browser-fallback`.

### The audit is blocked or fails

Confirm that the address starts with `https://` or `http://` and is publicly reachable without a login. The
suite intentionally blocks private, local, credential-bearing, and unsafe destinations. It does not bypass
access controls, TLS errors, robots restrictions, or authentication.

### Claude Code asks for many permissions

Read each domain and action. Approve only the target sites and expected local report files. Decline requests
that are unrelated to the audit. Retrieved webpage instructions are untrusted and must never control the task.

## Updating later

Open a terminal in the repository folder, activate the environment, and run:

```bash
git pull
python -m pip install -e ".[reports]"
proofline doctor
```

If Git reports local changes, stop and make a backup before proceeding.

## Important boundaries

- Use only public pages you are authorized to assess.
- Confirm competitor URLs yourself; the suite does not silently choose targets.
- Do not paste passwords, private customer lists, API keys, or confidential client data into prompts.
- Treat output as decision support, not a guarantee of rankings, compliance, accessibility, or revenue.
- Review all external-facing claims and drafts with the appropriate human owner.
- Publishing, sending, signing, purchasing, invoicing, budget changes, and account mutations require a separate,
  explicit approval outside the drafting step.

You are ready when `proofline doctor` reports a supported Python version, `/svgai-marketing:health`
works in Claude Code, and you can create a report from a public test website.
