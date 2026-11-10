"""L05 check: the four extension points (CLAUDE.md, a skill, an MCP server, a subagent)."""

import json
import sys

from _common import ROOT, Report, filled, run, sections_written, student_agents, student_skills

APP_MEMORY = ROOT / "labs" / "l04-first-app" / "CLAUDE.md"
NOTES = ROOT / "labs" / "l05-extend" / "NOTES.md"


def mcp_servers() -> tuple:
    """(servers with a command or url, error message or '')."""
    path = ROOT / ".mcp.json"
    if not path.exists():
        return [], "no .mcp.json in the repo root"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        return [], f".mcp.json isn't valid JSON ({e})"
    servers = data.get("mcpServers") if isinstance(data, dict) else None
    if not isinstance(servers, dict) or not servers:
        return [], ".mcp.json has no servers under mcpServers"
    good = [name for name, cfg in servers.items() if isinstance(cfg, dict) and (cfg.get("command") or cfg.get("url"))]
    return good, "" if good else "no server in .mcp.json has a command or url"


def main() -> int:
    r = Report("L05 · Extending the harness")

    if filled(APP_MEMORY, 300):
        r.ok("Your app has its own CLAUDE.md")
    else:
        r.fail("labs/l04-first-app/CLAUDE.md is missing, very short or still has TODOs",
               "Ask Claude to draft a one-page CLAUDE.md for your L04 app, then edit it")

    skills = student_skills()
    if skills:
        r.ok(f"Skill: /{', /'.join(skills)}")
    else:
        r.fail("No skill of your own in .claude/skills/ (with a name and description)",
               "Pick a job you repeat on your app and ask Claude to turn it into a skill")

    servers, err = mcp_servers()
    if servers:
        r.ok(f"MCP server: {', '.join(servers)}")
    else:
        r.fail(err, "Ask Claude to add the Context7 MCP server to .mcp.json")

    agents = student_agents()
    if agents:
        r.ok(f"Subagent: {', '.join(agents)}")
    else:
        r.fail("No subagent in .claude/agents/ (with a name and description)",
               "Ask Claude to create a reviewer subagent for your app")

    if not sections_written(NOTES, ["CLAUDE.md", "My skill", "My MCP server", "My subagent"], 80):
        r.ok("NOTES.md is written")
    else:
        r.fail("labs/l05-extend/NOTES.md still has TODOs or is very short",
               "Write each section in your own words after you've tried that piece")

    ok, out = run(["git", "status", "--porcelain", "--", ".claude", ".mcp.json", "labs/l04-first-app/CLAUDE.md", "labs/l05-extend"])
    if ok and out:
        r.warn("Some of this work isn't committed yet", "Ask Claude to commit it so it's saved in your repo")

    return r.finish("l05")


if __name__ == "__main__":
    sys.exit(main())
