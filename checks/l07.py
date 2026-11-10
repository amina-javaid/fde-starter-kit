"""L07 check: the capstone cycle (discovery, harness, app, evaluation, demo) for the Tidewell brief."""

import re
import sys

from _common import ROOT, Report, code_files, commits_on, filled, read_json, section, sections_written, student_agents, student_skills

LAB = ROOT / "labs" / "l07-capstone"


def golden_cases() -> int:
    data = read_json(LAB / "evals" / "golden.json", {})
    cases = data.get("cases", []) if isinstance(data, dict) else []
    return sum(1 for c in cases if isinstance(c, dict) and c.get("input") and c.get("expected"))


def demo_link() -> str:
    m = re.search(r"https://[^\s)>\]]+", section(LAB / "DEMO.md", "Recording"))
    return m.group(0) if m else ""


def main() -> int:
    r = Report("L07 · Capstone: First Field Deployment")

    if not sections_written(LAB / "DISCOVERY.md", ["The problem", "Who uses it", "The number we agreed", "What needs a person", "Risks", "Out of scope"], 60):
        r.ok("DISCOVERY.md is written")
    else:
        r.fail("DISCOVERY.md still has TODOs or is very short", "Work through the brief with Claude and answer each section in your own words")

    if filled(LAB / "CLAUDE.md", 300):
        r.ok("The capstone has its own CLAUDE.md")
    else:
        r.fail("No CLAUDE.md in labs/l07-capstone/ (or it still has TODOs)", "Ask Claude to draft one for this project, then edit it")

    skills, agents = student_skills(), student_agents()
    if skills and agents:
        r.ok(f"Skill /{skills[0]} and subagent {agents[0]} are in place")
    else:
        missing = " and ".join(x for x, have in (("a skill", skills), ("a subagent", agents)) if not have)
        r.fail(f"Missing {missing} of your own", "Reuse your L05 ones or ask Claude to create one for this project")

    code = code_files(LAB / "app")
    if code:
        r.ok(f"{len(code)} code file(s) in app/")
    else:
        r.fail("No code in labs/l07-capstone/app/", "Plan and build the app with Claude Code inside app/")

    n = golden_cases()
    if n >= 5:
        r.ok(f"Golden set: {n} cases")
    else:
        r.fail(f"Golden set has {n} case(s) with input and expected, need 5",
               "Add at least 5 tickets to evals/golden.json with the answer a team lead would give")

    todo = sections_written(LAB / "README.md", ["How to run", "How it works"])
    if not todo:
        r.ok("README explains how to run it and how it works")
    else:
        r.fail(f"README section(s) not written yet: {', '.join(todo)}", "Fill them in your own words")

    if demo_link() and not sections_written(LAB / "DEMO.md", ["Talk track"], 200):
        r.ok("DEMO.md has your recording and talk track")
    else:
        r.fail("DEMO.md has no https:// recording link, or still has TODOs", "Record your three-minute demo and fill in DEMO.md")

    commits = commits_on("labs/l07-capstone")
    if commits >= 3:
        r.ok(f"{commits} commits on the capstone")
    else:
        r.fail(f"{commits} commit(s) on the capstone, need 3", "Ask Claude to commit after each working step")

    return r.finish("l07")


if __name__ == "__main__":
    sys.exit(main())
