# L05 · Extending the harness

You extend your **L04 app** with the four ways to shape Claude Code: a CLAUDE.md, a skill, an MCP server and a subagent. Claude Code writes the files with you; you decide what goes in them and try each one.
The full walkthrough is in the **Lab** tab of L05 on the pre-work site.

1. **CLAUDE.md for your app.** Ask Claude to draft `labs/l04-first-app/CLAUDE.md`: what the app is, who it's for, how it's organised, how to run it, and the rules that must never break. Read it, cut what you don't need, keep it to one page.
2. **A skill.** Pick a job you'll repeat on this app (for example, "try my app on three sample inputs and summarise the results"). Ask Claude to make it a skill in `.claude/skills/<name>/SKILL.md`, then use it with `/<name>`.
3. **An MCP server.** Ask Claude to add the Context7 docs server to `.mcp.json` (it runs remotely, so nothing to install). Approve it when Claude Code asks, then ask a question that uses it.
4. **A subagent.** Ask Claude to create a reviewer subagent in `.claude/agents/` that reads your app and reports problems. Ask Claude to hand it a review.
5. Fill in `NOTES.md` **in your own words**, ask Claude to commit, then type `/check l05`.
