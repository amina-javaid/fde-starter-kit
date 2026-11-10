"""L06 check: a three-tier app (frontend, backend, AI backend) set up for Docker, with the key kept off the frontend."""

import re
import shutil
import sys
import urllib.request

from _common import ROOT, Report, code_files, commits_on, run, section, sections_written

LAB = ROOT / "labs" / "l06-three-tier"
TIERS = {"frontend": "the screen", "backend": "the API", "ai": "the AI backend"}
COMPOSE_NAMES = ["compose.yaml", "compose.yml", "docker-compose.yml", "docker-compose.yaml"]
KEY_PATTERN = re.compile(r"sk-or-|OPENROUTER_API_KEY")
TEXT_SKIP = {"node_modules", "dist", "build", ".venv", "venv", "__pycache__", ".vercel"}


def key_leaks() -> list:
    folder = LAB / "frontend"
    hits = []
    if not folder.exists():
        return hits
    for p in folder.rglob("*"):
        if not p.is_file() or TEXT_SKIP.intersection(p.parts) or p.stat().st_size > 2_000_000:
            continue
        try:
            if KEY_PATTERN.search(p.read_text(encoding="utf-8", errors="ignore")):
                hits.append(p.relative_to(LAB).as_posix())
        except OSError:
            pass
    return hits


def live_url() -> str:
    found = re.search(r"https://[^\s)>\]]+", section(LAB / "README.md", "Live URL"))
    return found.group(0) if found else ""


def reachable(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fde-starter-check"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status < 400
    except Exception:
        return False


def main() -> int:
    r = Report("L06 · Full-stack architecture")

    for tier, what in TIERS.items():
        folder = LAB / tier
        code = code_files(folder)
        has_docker = (folder / "Dockerfile").exists()
        if code and has_docker:
            r.ok(f"{tier}/ ({what}): {len(code)} code file(s) and a Dockerfile")
        elif not code:
            r.fail(f"No code in labs/l06-three-tier/{tier}/ ({what})", "Ask Claude to build this layer, in plan mode first")
        else:
            r.fail(f"No Dockerfile in labs/l06-three-tier/{tier}/", "Ask Claude to add a Dockerfile for this layer")

    compose = next((LAB / n for n in COMPOSE_NAMES if (LAB / n).exists()), None)
    if not compose:
        r.fail("No compose.yaml in labs/l06-three-tier/", "Ask Claude to add a compose.yaml that runs all three layers")
    elif not shutil.which("docker"):
        r.fail("Docker isn't installed, so the compose file can't be checked",
               "Install Docker Desktop from docker.com, then close and reopen VS Code")
    else:
        ok, out = run(["docker", "compose", "-f", str(compose), "config", "--quiet"])
        if ok:
            r.ok(f"{compose.name} is valid and defines the app's services")
        else:
            first = out.splitlines()[0] if out else "docker compose config failed"
            r.fail(f"{compose.name} has a problem: {first}", "Ask Claude to read this error and fix the compose file")

    leaks = key_leaks()
    if leaks:
        r.fail(f"The frontend mentions the API key: {', '.join(leaks[:3])}",
               "Ask Claude to move every model call into ai/, so the key never reaches the browser")
    else:
        r.ok("No API key in the frontend")

    todo = sections_written(LAB / "README.md", ["How a request travels", "Where the key lives"])
    if not todo:
        r.ok("README explains the request path and where the key lives")
    else:
        r.fail(f"README section(s) not written yet: {', '.join(todo)}", "Write them in your own words, a few sentences each")

    url = live_url()
    if not url:
        r.fail("No https:// address under 'Live URL' in the README", "Deploy the frontend with Claude's help and paste its address there")
    elif reachable(url):
        r.ok(f"{url} is live")
    else:
        r.warn(f"Couldn't open {url} just now", "Open it in your browser. If it's down, ask Claude to check the deploy")

    commits = commits_on("labs/l06-three-tier")
    if commits >= 3:
        r.ok(f"{commits} commits on this lab")
    else:
        r.fail(f"{commits} commit(s) on this lab, need 3", "Ask Claude to commit after each layer works")

    return r.finish("l06")


if __name__ == "__main__":
    sys.exit(main())
