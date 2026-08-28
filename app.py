"""
Entry point for the Multi-Agent AI Research System.

Usage:
    python app.py "your research question here"

Or with no arguments, it will prompt for a question interactively:
    python app.py

Or import and use programmatically:
    from agents.orchestrator import OrchestratorAgent
    orchestrator = OrchestratorAgent()
    result = orchestrator.run("your question")
"""

import sys

from agents.orchestrator import OrchestratorAgent


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your research question: ")

    orchestrator = OrchestratorAgent()
    orchestrator.run(query)


if __name__ == "__main__":
    main()
