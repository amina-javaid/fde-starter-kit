# L06 · Full-stack architecture

You rebuild your L04 idea as a three-tier app, run it in Docker, and put it on a live URL. Claude Code writes the code, the Docker files and the deploy settings; you direct it and check each layer works.
The full walkthrough is in the **Lab** tab of L06 on the pre-work site.

1. Install **Docker Desktop** (docker.com, an ordinary installer), then close and reopen VS Code.
2. In plan mode, ask Claude to plan a three-tier version of your app in this folder: `frontend/` (the screen), `backend/` (the API the screen calls) and `ai/` (the AI backend that calls the model and streams the answer). The key lives only in `ai/`, read from an environment variable.
3. Ask Claude to add a `Dockerfile` to each folder and a `compose.yaml` that runs all three, then to start it and open the app. Commit after each layer works.
4. Deploy with Claude's help: the frontend on **Vercel**, the backend and AI backend on **Render** (both sign in with GitHub). Claude writes the settings; you click through the import screens and paste your key into Render's environment settings.
5. Fill in the three sections below **in your own words**, ask Claude to commit, then type `/check l06`.

## Live URL

TODO: the https:// address of your deployed frontend.

## How a request travels

TODO: 4–6 sentences. Follow one click from the browser to the model and back. Which layer does what, and where does streaming happen?

## Where the key lives

TODO: Where is your OpenRouter key stored in Docker and in the deployed app, and why can't it go in the frontend?
