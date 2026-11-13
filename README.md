# Customer Success Copilot

An AI assistant for Customer Success and Technical Account Managers. Paste raw call notes, emails or meeting summaries, and it turns them into a clear account analysis you can act on right away.

![Customer Success Copilot screenshot](screenshot.png)

## What it does

- **Health score** from 0 to 100 with an At Risk / Healthy / Critical label
- **Churn risk with evidence.** Every risk reason is backed by a direct quote from the notes, so you can see exactly why
- **Stakeholder map** that tags each person as a champion, decision maker, neutral or detractor, and flags accounts that depend on a single contact
- **Commitments tracker** that catches every promise made, with an owner and due date
- **Prioritized next actions** a CSM could take this week
- **Follow-up email** drafted in the tone you choose
- **Internal escalation draft** for support, product or engineering, with urgency
- **Expansion signals and missing info**, such as an unknown renewal date or no executive sponsor

## Why I built it

I spent years managing client relationships while building websites and digital solutions. The hardest part was never the call itself. It was everything after: remembering what was promised, spotting early warning signs and following up fast. This tool handles that part.

## How it works

The app sends the notes to Google's Gemini model with a detailed system prompt that asks it to think like an experienced CSM, base everything only on the notes, quote evidence for every risk and return structured JSON. The app then turns that JSON into the dashboard.

**Built with** Python, Streamlit and the Google Gemini API (free tier).

**Try it instantly.** The three sample accounts load saved analyses, so anyone can explore the full output with no API key. Live analysis of your own notes uses the Gemini free tier, limited to a few runs per visit.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Load a sample account from the sidebar and click **Analyze account**. To analyze your own notes, add a free Gemini API key from [Google AI Studio](https://aistudio.google.com).

To avoid pasting the key each time, copy `secrets.toml.example` to `.streamlit/secrets.toml` and add your key there. That file is excluded from git so the key stays private.

## Project files

| File | Purpose |
|---|---|
| `app.py` | The app interface and logic |
| `prompts.py` | The instructions given to the AI |
| `sample_notes.py` | Three fictional accounts to try |
| `demo_results.py` | Saved analyses for the samples |
| `.streamlit/config.toml` | Theme colors |

All sample companies and people are fictional. AI can make mistakes, so always review the output before sending anything to a customer.

Built by Hadia Tahir.
