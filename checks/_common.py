"""Shared helpers for the level checks. Standard library only, so checks run
on a fresh machine before anything is pip-installed."""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from _gate import code_for, normalize_handle

ROOT = Path(__file__).resolve().parent.parent
FDE = ROOT / ".fde"
PROFILE = FDE / "profile.json"
PROGRESS = FDE / "progress.json"
SITE_URL = "https://fde-starter.vercel.app"  # TODO(owner): set to the deployed pre-work site

# Windows consoles default to cp1252; make sure our output never crashes.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def load_env() -> dict:
    """Parse .env (KEY=value lines) without needing python-dotenv."""
    env = {}
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def handle() -> str:
    return normalize_handle(read_json(PROFILE, {}).get("github_handle", ""))


def run(cmd: list) -> tuple:
    """Run a command; return (ok, stdout). Never raises."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=ROOT)
        return p.returncode == 0, (p.stdout or p.stderr).strip()
    except (OSError, subprocess.SubprocessError) as e:
        return False, str(e)


class Report:
    """Collects results and prints them in a format both students and Claude can read."""

    def __init__(self, title: str):
        self.title = title
        self.failed = 0
        print(f"\n== {title} ==\n")

    def ok(self, msg: str):
        print(f"  [PASS] {msg}")

    def fail(self, msg: str, fix: str):
        self.failed += 1
        print(f"  [FAIL] {msg}\n         fix: {fix}")

    def warn(self, msg: str, fix: str = ""):
        print(f"  [WARN] {msg}" + (f"\n         note: {fix}" if fix else ""))

    def finish(self, level: str) -> int:
        print()
        if self.failed:
            print(f"Not yet: {self.failed} item(s) to fix above. Fix them (ask Claude for help) and run the check again.")
            return 1
        h = handle()
        if not h:
            print("All checks passed, but no GitHub handle is set. Type /start in the Claude panel to set it.")
            return 1
        code = code_for(level, h)
        progress = read_json(PROGRESS, {})
        progress[level] = {"code": code, "passed_at": datetime.now(timezone.utc).isoformat()}
        write_json(PROGRESS, progress)
        print(f"PASSED. Your unlock code for {level.upper()} (GitHub @{h}):\n")
        print(f"    {code}\n")
        print(f"Paste it into the Check tab at {SITE_URL}/level/{level}/#check")
        return 0


# ---- Helpers shared by the L04–L07 checks ----

SHIPPED_SKILLS = {"start", "check", "preflight", "explain"}


def filled(path: Path, min_chars: int) -> bool:
    """True when a template file exists, has no TODO left and has some substance."""
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return "TODO" not in text and len(text.strip()) >= min_chars


def frontmatter(path: Path) -> dict:
    """Read the simple `key: value` frontmatter at the top of a skill or agent file."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return {}
    if not lines or lines[0].strip() != "---":
        return {}
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        if ":" in line and not line.startswith((" ", "\t")):
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return {}  # never closed


def student_skills() -> list:
    """Skills the student added (not the four the kit ships), with name + description."""
    found = []
    for p in sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md")):
        if p.parent.name in SHIPPED_SKILLS:
            continue
        meta = frontmatter(p)
        if meta.get("name") and meta.get("description"):
            found.append(p.parent.name)
    return found


def student_agents() -> list:
    """Subagents in .claude/agents/ with name + description."""
    found = []
    for p in sorted((ROOT / ".claude" / "agents").glob("*.md")):
        meta = frontmatter(p)
        if meta.get("name") and meta.get("description"):
            found.append(p.stem)
    return found


def commits_on(rel_path: str) -> int:
    """Commits after the template's initial commit that touched rel_path."""
    ok, out = run(["git", "rev-list", "--count", "--min-parents=1", "HEAD", "--", rel_path])
    return int(out) if ok and out.isdigit() else 0


def code_files(folder: Path, exts=frozenset({".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".mjs"})) -> list:
    if not folder.exists():
        return []
    skip = {"node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
    return [p for p in folder.rglob("*") if p.suffix in exts and not skip.intersection(p.parts)]


def section(path: Path, heading: str) -> str:
    """The text under a `## heading` in a Markdown file, up to the next `## `."""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    start = text.find(f"## {heading}")
    if start < 0:
        return ""
    body = text[start + len(heading) + 3:]
    end = body.find("\n## ")
    return (body if end < 0 else body[:end]).strip()


def sections_written(path: Path, headings: list, min_chars: int = 120) -> list:
    """Headings whose section is missing, still has a TODO, or is shorter than min_chars."""
    return [h for h in headings if (s := section(path, h)) == "" or "TODO" in s or len(s) < min_chars]
