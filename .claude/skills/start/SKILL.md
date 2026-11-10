---
name: start
description: Start or resume the FDE pre-work. Sets the student's GitHub handle, shows which levels have passed, and says exactly what to do next. Use when the student types /start or asks "where am I" / "what's next".
---

# /start: where am I, what's next

1. Run `python checks/profile.py show` (use `python3` if `python` isn't found).

2. **No handle yet** (`profile` is empty): welcome the student in two sentences: this repo is their tutor for the pre-work, and each level's check prints an unlock code for the site. Then ask for their **GitHub handle**, the same one they saved on the pre-work site. When they answer, run `python checks/profile.py set <handle>`.

3. **Tell them where they are**, using `passed` and `next` from the output:

   | next | Say |
   |---|---|
   | `l01` | If there's no `.env` yet, create it yourself by copying `.env.example` (say you're doing it). Then: open `.env` in the editor, paste the OpenRouter key after `OPENROUTER_API_KEY=` and save; type `/preflight`; fill in `ME.md` and ask you to commit and push it; paste the commit URL on the site. |
   | `l02` | Read L02 on the site, then open `labs/l02-hello-llm/hello_llm.py` and do the 3 TODOs. Ask you to run it with model A and model B, then type `/check l02`. |
   | `l03` | Step through the loop in L03's Demo tab, then do the 3 TODOs in `labs/l03-agent-by-hand/agent.py`. Ask you to run the agent with a question, then type `/check l03`. |
   | `l04` | Fill in `labs/l04-first-app/SPEC.md`, then build the app with you in plan mode, committing after each working step. Then type `/check l04`. |
   | `l05` | Read L05 on the site. Then, with you: a CLAUDE.md for their L04 app, a skill, the Context7 MCP server and a reviewer subagent (see `labs/l05-extend/README.md`). They write `NOTES.md` in their own words, then type `/check l05`. |
   | `l06` | Install Docker Desktop (clicks, then reopen VS Code). Then build the three-tier app with you in `labs/l06-three-tier/`, run it in Docker, deploy it, and write the README sections. Then type `/check l06`. |
   | `l07` | Read `labs/l07-capstone/BRIEF.md` together, fill in `DISCOVERY.md`, then build, evaluate and demo (see the lab README). Then type `/check l07`. |
   | `null` (all passed) | All levels passed. Congratulate them in one line and suggest they re-watch their L07 demo with the brief open: what would the client ask first? |

4. Keep it to one short message: a status line (e.g. "Passed: L01, L02"), then the next step as numbered actions. Every action is something they click, edit, type in this panel, or ask you to do: never a terminal command. Offer `/explain <term>` for anything unfamiliar.
