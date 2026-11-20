# RailOps AI — Agentic Inspection Scheduling Prototype

A working portfolio demonstration using **synthetic railcar records**, Python, Pandas, Streamlit, and optional **Gemini function calling**. Not affiliated with Trinity Industries or TrinityRail. Inspection scheduling flags are **not mechanical safety assessments**.

## Features
- Upload and validate a CSV of railcar inspection records
- Compute overdue / due soon / on-track inspection scheduling indicators
- Dashboard, filters, and downloadable CSV
- Deterministic, downloadable priority report (works without AI)
- Optional LLM assistant that calls Python tools to get real counts and priority records

## Run locally (Windows PowerShell)
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
No key is needed for the dashboard or automated report.

## Enable AI (optional)
1. Create a Gemini API key through [Google AI Studio](https://aistudio.google.com/apikey). Check free-tier eligibility, quotas and billing before using.
2. Copy `.env.example` to `.env` in this folder.
3. Replace `replace_with_your_key` with your key in `.env` (never share or commit it).
4. Restart Streamlit, then try: **How many railcars are overdue?** or **Which five are most overdue?**

The agent has two read-only tools: `get_inspection_summary()` and `get_priority_railcars(limit)`. The model calls tools to retrieve actual values. The reporting module performs deterministic Python calculations, not LLM-generated counts. If your account doesn't have access to the default model, change `GEMINI_MODEL` in `.env` to an available model supporting function calling.

## Test
```powershell
python -m unittest discover -s tests -v
```

## CSV format
Required: `railcar_id`, `last_inspection`, `inspection_interval_days`. Sample: `data/railcars.csv`.

## Limitations
Synthetic records only; no production rail operations integration, maintenance work-order submission, or safety evaluation. The AI component requires an eligible Gemini API key and network access; it may be subject to free-tier limits.
