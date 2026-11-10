# L07 · Capstone: a first field deployment

Your client is **Tidewell Parcel Co.** Read `BRIEF.md` first. This is one small FDE cycle: discovery, a project CLAUDE.md, a skill and a subagent, a working app, an evaluation, and a three-minute demo to the client.
The full walkthrough is in the **Lab** tab of L07 on the pre-work site.

1. **Discovery.** Read the brief and the data with Claude, then fill in `DISCOVERY.md` in your own words. Agree the number you'll be judged on.
2. **Set up the harness.** Ask Claude to draft a `CLAUDE.md` in this folder for the project. Reuse or add a skill (for example, "run the golden set and summarise the results") and a subagent (for example, a reviewer that checks a draft reply against the policy).
3. **Build** the app in `app/` with plan mode, in small steps, committing after each one that works. A person approves every refund over $100 and every legal or injury ticket.
4. **Evaluate.** Put at least 5 tickets in `evals/golden.json` with the answer a team lead would give, run the app on them, and record the results. Fix what fails.
5. **Demo.** Record three minutes for the client, and fill in `DEMO.md`.
6. Fill in the two sections below **in your own words**, ask Claude to commit and push, then type `/check l07`.

## How to run

TODO: what someone needs (keys, installs) and what to ask Claude Code to start the app.

## How it works

TODO: 5–8 sentences. Where a ticket goes, where the model is called, how the order lookup works, how approvals are enforced, and what your golden set showed.
