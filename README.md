# success-bud-oral

LiveKit Agents app for **Success bud**, a duplex voice mock-interview coach for Jabba.

The agent speaks first (French, *vous*), asks **one** MarTech or STAR question, waits, then gives a short spoken scorecard and the next question. Stack: **Gemini Live** speech-to-speech (`GOOGLE_API_KEY` only). No ElevenLabs. No Google Cloud STT/TTS service account.

This repo started as a seed README. The agent entrypoint is [`agent.py`](agent.py); the oral persona lives in [`instructions.py`](instructions.py) as `SUCCESS_BUD_INSTRUCTIONS`.

## What it coaches

- **Default language:** French, vouvoiement. English only if you ask.
- **Topics:** MarTech tracking/analytics (GTM, sGTM, GA4, Piano, consent/TCF) and culture/STAR.
- **Loop:** short greeting + one question → wait → 2–4 sentence spoken feedback with Correctness / Depth / Structure / Role fit / Evidence (0–5) → next question on the weakest dimension.
- **Facts:** allowlist only (Google GA4/GTM docs, Piano docs, IAB TCF, Simo Ahava, employer official public pages). Below ~70% confidence: *je ne sais pas* or marked provisional.
- **Out of scope:** contacting employers, trades/finance, invented APIs or UI click-paths, multi-question batteries, long markdown spoken aloud.

CV anchors used for role-fit (not recited as a bio dump): Tracking specialist at Fifty-five (Paris) since Jul 2023; legal/DPO background (Cnam); Adobe Analytics Developer (Mar 2025); Ironhack fullstack; native FR, TOEIC 810.

## Requirements

- Python 3.10–3.13 and [uv](https://docs.astral.sh/uv/)
- [LiveKit CLI](https://docs.livekit.io/agents/integrations/google/) (`lk`)
- A [LiveKit Cloud](https://cloud.livekit.io) project (free Build tier is enough to start)
- A [Gemini API key](https://aistudio.google.com/apikey) (`GOOGLE_API_KEY`)

Install the CLI if needed:

```bash
# Linux
curl -sSL https://get.livekit.io/cli | bash
# macOS: brew install livekit-cli
# Windows: winget install LiveKit.LiveKitCLI
```

## Setup

```bash
uv sync --extra dev
cp .env.example .env.local
```

Fill `.env.local`:

| Variable | Where |
| --- | --- |
| `LIVEKIT_URL` | LiveKit Cloud project settings (wss URL) |
| `LIVEKIT_API_KEY` | LiveKit Cloud API key |
| `LIVEKIT_API_SECRET` | LiveKit Cloud API secret |
| `GOOGLE_API_KEY` | Google AI Studio |

Shortcut for the three LiveKit values after `lk cloud auth`:

```bash
lk app env -w
```

Then add `GOOGLE_API_KEY` by hand. Do not set `GOOGLE_APPLICATION_CREDENTIALS`; that is the Google Cloud STT/TTS path this agent does not use.

## Run locally

From the repo root, with `.env.local` populated:

**Terminal duplex (mic in the console):**

```bash
lk agent console
# equivalent: uv run agent.py console
```

**Dev worker on LiveKit Cloud (talk from the Agents playground / console in the browser):**

```bash
lk agent dev
# equivalent: uv run agent.py dev
```

In the Cloud Agents console, the agent name is `success-bud-oral`. Use a headset if you can; speak in short turns and wait for the coach to finish before answering.

Smoke check without a live session (no keys required):

```bash
uv run pytest
```

## Deploy to LiveKit Cloud Build

Free-tier path (~1000 agent session minutes/month on LiveKit Cloud Build, subject to current plan limits):

1. Create a LiveKit Cloud project and copy URL / API key / secret.
2. Authenticate the CLI and create the agent (first deploy generates `livekit.toml` locally; that file is gitignored because it is project-specific):

```bash
lk cloud auth
lk agent create
```

3. When the CLI asks for secrets, set **`GOOGLE_API_KEY`**. Do not put LiveKit keys in the Dockerfile; Cloud injects `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET`.
4. Later updates:

```bash
lk agent deploy
```

This repo already includes a `Dockerfile` and `.dockerignore` matching the [Cloud Build Python/uv template](https://docs.livekit.io/deploy/agents/builds/). If `lk agent create` offers to write a Dockerfile, keep the one in the repo.

After deploy, open the project Agents dashboard, start a session, and speak in French. The coach should greet you and ask a single question.

## French voice notes

- Gemini Live **native audio** chooses language from the conversation. French is pinned in `SUCCESS_BUD_INSTRUCTIONS`; do not rely on a `language_code` (unsupported on native-audio Live models).
- Default voice is **Kore** (firm interviewer). Change `GEMINI_LIVE_VOICE` in `agent.py` to `Charon`, `Aoede`, or `Puck` if you want a different timbre. All of these are Gemini Live prebuilt voices; no paid TTS vendor.
- Keep answers short. The agent is instructed to score out loud in a speakable way (`exactitude 4 sur 5`), not as a markdown table.
- English is opt-in: ask, in the session, to switch.

Optional noise-cancellation plugins (`livekit-plugins-ai-coustics`, etc.) are **not** included so `uv sync` stays minimal. Add them later if a room needs enhancement.

## Free-tier caveats

- **Gemini API (AI Studio / unpaid):** Google may use prompts and audio to improve products unless you are on a plan that turns that off. Do not put confidential employer data or real candidate PII in sessions on the free key. See [Gemini API terms](https://ai.google.dev/gemini-api/terms).
- **LiveKit Cloud Build:** session minutes are metered. The free tier is on the order of **~1000 agent session minutes/month**; confirm the current quota in the Cloud dashboard. Console/dev sessions count.
- **No paid voice vendors** are required. Stay on Gemini Live + LiveKit.
- **Secrets:** never commit `.env`, `.env.local`, or `livekit.toml`. Rotate a key if it leaks.

## Layout

```
agent.py            # AgentServer + Gemini Live RealtimeModel entrypoint
instructions.py     # SUCCESS_BUD_INSTRUCTIONS
tests/              # persona smoke tests (no API keys)
pyproject.toml
.env.example
Dockerfile          # LiveKit Cloud Build
```

Pinned Live model: `gemini-2.5-flash-native-audio-preview-12-2025` (Developer API). Avoid `gemini-3.1-flash-live-preview` for this greeting flow: `generate_reply()` is not compatible with 3.1 in LiveKit Agents 1.5.

## License / product boundary

Interview **prep** only. The agent must not contact employers, invent product UI, or give financial advice.
