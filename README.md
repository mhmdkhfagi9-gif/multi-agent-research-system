# Multi-Agent AI Research System

A multi-agent AI research system that autonomously retrieves information
from PDFs, structured datasets, and APIs, analyzes and cross-validates the
information using specialized AI agents, orchestrates the complete
workflow, and automatically generates and distributes a professional
report.

## Architecture

```
                    USER
                     |
                     v
             ORCHESTRATOR AGENT
                     |
       -----------------------------
       |             |             |
       v             v             v
   PDF Agent      API Agent    Sheet Agent      <- run in PARALLEL, then merged
       |             |             |
       -----------------------------
                     |
                     v
             ANALYSIS AGENT
                     |
                     v
              CRITIC AGENT
                     |
          -----------------------
          |                     |
        ERROR                 VALID
          |                     |
   Retrieve Again          Report Agent
   (loop back, up to               |
    MAX_RETRIEVAL_RETRIES)         v
                              ACTION AGENT
                                    |
                  ---------------------------------
                  |               |                |
                  v               v                v
             PDF Report      Dashboard           Email
```

## Project Structure

```
project/
│
├── agents/
│   ├── orchestrator.py       # Coordinates the whole pipeline above
│   ├── retrieval_agent.py    # Contains PDFAgent, APIAgent, SheetAgent + the RetrievalAgent that runs them in parallel
│   ├── analysis_agent.py     # Cross-validates retrieved info via the LLM, outputs structured JSON
│   ├── critic_agent.py       # Reviews the analysis -> VALID or ERROR
│   ├── report_agent.py       # Turns a validated analysis into a human-readable report
│   └── action_agent.py       # Distributes the report: file, dashboard.json, email
│
├── data/
│   ├── documents/            # Put your source PDFs here
│   └── datasets/             # Put your source CSV/Excel files here
│
├── tools/
│   ├── pdf_reader.py         # Real PDF text extraction (pypdf)
│   ├── api_client.py         # Real HTTP GET requests, fails gracefully
│   ├── sheet_reader.py       # Converts spreadsheet rows to text records
│   └── email_sender.py       # Real SMTP send, defaults to a safe DRY-RUN mode
│
├── outputs/
│   └── reports/              # Saved report files land here
│   └── dashboard.json        # Auto-created; append-only run history for a dashboard UI
│
├── tests/
│   └── test_cases.json       # Predefined test queries for evaluation
│
├── app.py                    # Entry point
├── config.py                 # All settings: LLM, paths, retry limits, email config
├── requirements.txt
└── README.md
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Groq API key (get one at console.groq.com):
   ```bash
   export GROQ_API_KEY="your-real-key-here"
   ```
   (Or edit the default in `config.py` directly, though an environment
   variable is safer than committing a key to a file.)

3. Add your knowledge base:
   - Drop PDF files into `data/documents/`
   - Drop CSV/Excel files into `data/datasets/`
   - Optionally change `DEFAULT_API_URL` in `config.py` to point at your
     real API

4. (Optional) Enable real email sending:
   - Set `EMAIL_DRY_RUN = False` in `config.py`
   - Provide `SMTP_USERNAME` / `SMTP_PASSWORD` / `EMAIL_RECIPIENT` as
     environment variables
   - By default (`EMAIL_DRY_RUN = True`), the Action Agent just prints what
     it *would* send -- so the full pipeline works end-to-end with zero
     email setup.

## Running

```bash
python app.py "What are the key findings across our documents and data sources?"
```

Or run it interactively (it will prompt you for a question):
```bash
python app.py
```

Or use it programmatically:
```python
from agents.orchestrator import OrchestratorAgent

orchestrator = OrchestratorAgent()
result = orchestrator.run("your question here")

print(result["report"])
```

## How the Pipeline Works

1. **Retrieval Agent** runs `PDFAgent`, `APIAgent`, and `SheetAgent`
   concurrently (via `ThreadPoolExecutor`, since they don't depend on each
   other) and merges their outputs into one context string.
2. **Analysis Agent** sends that merged context to the LLM, asking it to
   identify key findings and flag whether the sources agree, conflict, or
   are insufficient -- returned as structured JSON.
3. **Critic Agent** reviews the analysis independently and returns
   `VALID` or `ERROR`. On `ERROR`, the Orchestrator loops back to Step 1,
   up to `MAX_RETRIEVAL_RETRIES` times (in `config.py`), before giving up
   and proceeding anyway with the best available analysis.
4. **Report Agent** turns a validated analysis into a clear, 4-6 sentence
   human-readable report.
5. **Action Agent** distributes that report three ways: saved to a file
   under `outputs/reports/`, appended to `outputs/dashboard.json` (which a
   real dashboard UI could read from), and emailed (or dry-run printed).

## Testing & Evaluation

`tests/test_cases.json` lists sample queries covering: general cross-source
retrieval, spreadsheet-focused questions, cross-source agreement/conflict
detection, and a case designed to check the system doesn't hallucinate when
data is genuinely missing. Run each query through `app.py` and compare the
resulting report and `analysis["confidence"]` against `expected_sources_used`
and `notes` to evaluate accuracy and relevance.

## One-Sentence Summary

> We developed a multi-agent AI research system that autonomously retrieves
> information from PDFs, structured datasets, and APIs, analyzes and
> cross-validates the information using specialized AI agents, orchestrates
> the complete workflow, and automatically generates and distributes a
> professional report.
