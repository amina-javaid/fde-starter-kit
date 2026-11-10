---
name: preflight
description: L01 environment check. Verifies Git, Python, Claude Code, the OpenRouter key and the GitHub repo, explains any failures, fixes what it can, and prints the L01 unlock code when everything passes. Use when the student types /preflight or asks if their setup is ready.
---

# /preflight: is this machine ready?

1. Run `python checks/preflight.py` (use `python3` if `python` isn't found or opens the Microsoft Store).

2. If there are `[FAIL]` lines, go through them **one at a time**, starting with the first:
   - Explain in one plain sentence what's missing and why the bootcamp needs it.
   - **If you can fix it, offer to, and do it when they say yes.** For example, a missing Git name or email: ask for the name and email they use on GitHub, then set them yourself with `git config --global user.name` / `user.email`. A missing `.env`: copy `.env.example` to `.env`.
   - **If only they can fix it** (downloading and running an installer, signing in, pasting their key), give the steps as clicks for *their* OS (check the platform; Windows and macOS differ). Never ask them to type a command.
   - After they install anything, ask them to **close every VS Code window and reopen it**, so VS Code finds the new tool. Then run the check again yourself.

3. Never open, print or `cat` the `.env` file. If the key is the problem, ask them to open `.env` in the editor and check it's one line: `OPENROUTER_API_KEY=sk-or-...` with no quotes or spaces.

4. `[WARN]` lines don't block. Mention them briefly (Node and Docker are only needed from L06).

5. When the script prints `PASSED`, show the unlock code exactly as printed and say where to paste it. Then the second half of L01: ask them to fill in `ME.md` and tell you when it's saved. When they do, offer to commit it ("Introduce myself") and push it. After the push, tell them to open the commit on GitHub and paste its URL on the site's L01 Check tab. If the push fails on sign-in, ask them to click **Sync Changes** in VS Code's Source Control view.
