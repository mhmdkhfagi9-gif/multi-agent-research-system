"""
Retrieval Agent: coordinates the three source-specific sub-agents shown as
parallel branches in the architecture diagram (PDF Agent, API Agent, Sheet
Agent), runs them concurrently since they don't depend on each other, and
merges their results into one combined context for the Analysis Agent.
"""

from concurrent.futures import ThreadPoolExecutor

import config
from tools.pdf_reader import read_all_pdfs
from tools.api_client import fetch_from_api
from tools.sheet_reader import read_all_sheets


class PDFAgent:
    """Reads every PDF under data/documents/."""

    def run(self) -> str:
        results = read_all_pdfs(config.DOCUMENTS_DIR)
        if not results:
            return "[PDF Agent] No PDF documents found in data/documents/."
        return "\n\n".join(f"--- {name} ---\n{text}" for name, text in results.items())


class APIAgent:
    """Fetches data from the configured external API."""

    def run(self, url: str = None) -> str:
        url = url or config.DEFAULT_API_URL
        result = fetch_from_api(url)
        if not result["success"]:
            return f"[API Agent] Failed to fetch from {url}: {result['error']}"
        return f"[API Agent] Data from {url}:\n{result['data']}"


class SheetAgent:
    """Reads every spreadsheet under data/datasets/."""

    def run(self) -> str:
        results = read_all_sheets(config.DATASETS_DIR)
        if not results:
            return "[Sheet Agent] No datasets found in data/datasets/."
        return "\n\n".join(f"--- {name} ---\n{text}" for name, text in results.items())


class RetrievalAgent:
    """
    Runs PDFAgent, APIAgent, and SheetAgent IN PARALLEL (matching the
    diagram's simultaneous branches), then merges everything into one
    combined context string for the Analysis Agent.
    """

    def __init__(self):
        self.pdf_agent = PDFAgent()
        self.api_agent = APIAgent()
        self.sheet_agent = SheetAgent()

    def run(self, api_url: str = None) -> dict:
        with ThreadPoolExecutor(max_workers=3) as executor:
            pdf_future = executor.submit(self.pdf_agent.run)
            api_future = executor.submit(self.api_agent.run, api_url)
            sheet_future = executor.submit(self.sheet_agent.run)

            pdf_result = pdf_future.result()
            api_result = api_future.result()
            sheet_result = sheet_future.result()

        merged_context = "\n\n".join([pdf_result, api_result, sheet_result])

        return {
            "pdf": pdf_result,
            "api": api_result,
            "sheet": sheet_result,
            "merged_context": merged_context,
        }
