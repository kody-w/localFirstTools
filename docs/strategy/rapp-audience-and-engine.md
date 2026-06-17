# RAPP — Audience Definition & Owned Audience Engine

*Derived from the RAPP ecosystem (brainstem / RACon / .egg / kited layer / neighborhood protocol) and Kody's positioning. The funnel implements the engine from the "Funded R&D" 90-day plan and the Authority Ascension method.*

---

## What RAPP provides (the value, in the user's terms)

RAPP is **an operating system for on-device AI agent swarms.** The PC analogy:

| Layer | RAPP |
|---|---|
| Operating system | `brainstem.py` — runs single-file Python agents on your own device |
| Desktop / console | **RACon** — the user-facing console |
| Apps | **rapplications**, shipped as **`.egg` cartridges** that hatch into twins |
| Identity + runtime | your **GitHub account** — the only account you need |
| Network | the **kited layer** — links your devices + twins, sealed end-to-end; MCP is the second on-ramp |

The throughline: **you own it.** Agents are single files that "just run" — no framework, no deploy, no servers, no API keys, no data leaving the machine unless you *kite* it on purpose.

---

## The audience tension (and the resolution)

RAPP implies two audiences:

- **(A) Builders / early adopters** — developers who write single-file agents, kite twins, wire MCP. Reachable **today** via search and content.
- **(B) Operators** — non-technical people who just run rapplications via RACon. The **long-term mass vision**, but not who you reach first with discoverable content.

**Primary near-term lead-gen audience → (A) Builders.** Why: they feel the pain *now*, they can adopt RAPP *today* with zero hand-holding, and they type the exact searches RAPP answers. They are also the people who *create the rapplications* that eventually serve audience B — so winning builders seeds the whole ecosystem. Operators are the destination; builders are the on-ramp.

### The primary ICP, specifically

> Experienced developers deep in the AI-agent space, **burned out on cloud-locked, framework-heavy, vendor-dependent stacks** — people who wired up hosted agent frameworks and realized they don't actually *own* any of it. Their agents, data, and identity all live on someone else's servers and break the moment an API, model, or pricing page changes.

**Secondary:** Microsoft/M365 & Copilot teams who need agentic systems but can't send data to third-party clouds (Kody's day-job adjacency — a warm, credible enterprise lane).
**Long-term:** non-technical operators running preloaded rapplications via RACon.

---

## The signal (one sentence)

> **RAPP lets you build and run autonomous AI agents on your own device and your own GitHub account — single-file, no servers, no lock-in — that you can fork, share, and keep.**

Who it's **for:** builders who want to *own* their agent stack.
Who it's **not for:** people who want a managed, hosted, click-to-deploy cloud agent product.

The enemy is **rented intelligence.** The promise is **ownership.**

---

## The Owned Audience Engine (mapped to RAPP)

**Content → Bridge → Owned Audience → Offer.** Content is the front door; the owned audience is the house.

| Piece | RAPP asset | File |
|---|---|---|
| **Content** (discoverable) | *Anatomy of a single-file agent* — a useful, search-findable interactive that teaches the agent shape and shows RAPP's "it just runs" value | `rapp-agent-anatomy.html` |
| **Bridge** (lead magnet) | *The Local-First Agent Starter Kit* — generate your first real single-file agent + the one-line install, in the browser, in 10 minutes; earns the email | `rapp-starter-kit.html` |
| **Owned audience** | email captured **local-first / no-backend** (localStorage + a prefilled GitHub Issue + mailto, JSON export) — never a keyed POST | (inside the bridge) |
| **Offer** (destination) | the recommended offer below | `rapp-engine.html` (front door + offer hub) |

**Authority keywords** (what the ICP types): `local-first AI agents`, `run AI agents on your own device`, `single-file python agent`, `AI agents without the cloud`, `self-hosted agent swarm`, `own your AI agents`, `local MCP server`, `agent framework alternative`, `brainstem agent runtime`.

**Real surfaces the funnel points to:** the install one-liner (`curl … rapp-installer`), RAR (`kody-w.github.io/RAR/`), the RAPP Bible (`kody-w.github.io/RAPP-Bible/`), the kited demo (`kody-w.github.io/vbrainstem/kited-demo.html`).

---

## The recommended offer (steerable — Kody's call)

**Recommended:** a **live cohort / build-along** — *The Local-First Agent Lab* — 6 weekly sessions where each builder ships one real owned artifact (brainstem running → first single-file agent → kited across two devices → an `.egg` published → an MCP host calling it). Pre-sold POP-style at ~$1,500/seat before recording anything. *Why:* it's the fastest path to revenue + social proof, it produces the case studies that pull in the next cohort, and it directly converts the builder audience.

**Alternatives:**
- **Adoption-first (open-source flywheel):** the "offer" is *install RAPP + publish an egg to the registry*; monetize later via a pro tier, hosting, or support. Best if the goal is ecosystem scale over near-term revenue.
- **Enterprise lead-gen:** the funnel books a *local-first agent architecture* consult with the M365/Copilot lane. Highest deal size, lowest volume.

The **bridge and content assets are offer-agnostic** — they capture and warm the right builders regardless. Only `rapp-engine.html`'s call-to-action changes with the offer choice.

---

## The funnel flow

1. A builder searches an authority keyword → lands on **`rapp-agent-anatomy.html`** (content), learns something useful, sees that a real agent is *one file that just runs*.
2. Wants to do it themselves → **`rapp-starter-kit.html`** (bridge): generates their first agent + the install path, and earns their email into the owned audience.
3. **`rapp-engine.html`** (front door + offer) states the signal and routes warmed builders to the offer + the real RAPP get-started surfaces.
4. Email list compounds; every new piece of content has a built-in audience.

---

*Status: strategy + bridge asset shipped inline (API-overload-resilient). Content (`rapp-agent-anatomy.html`) and front-door (`rapp-engine.html`) to follow.*
