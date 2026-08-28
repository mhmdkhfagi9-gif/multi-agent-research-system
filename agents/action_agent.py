"""
Action Agent: distributes the final report to its three destinations shown
in the architecture diagram -- a saved report file, a dashboard data file,
and email.
"""

import os
import json
import datetime

import config
from tools.email_sender import send_email


class ActionAgent:
    def run(self, user_query: str, report: str, analysis: dict) -> dict:
        os.makedirs(config.REPORTS_DIR, exist_ok=True)

        results = {}
        results["pdf_report"] = self._save_report_file(user_query, report)
        results["dashboard"] = self._update_dashboard(user_query, report, analysis)
        results["email"] = send_email(
            subject=f"Research Report: {user_query[:60]}",
            body=report,
        )
        return results

    def _save_report_file(self, user_query: str, report: str) -> dict:
        """
        NOTE: saves a .txt report (not a real .pdf) to keep the project
        dependency-light. Swap in a PDF library (e.g. the 'pdf' skill's
        approach with reportlab/fpdf) here if a literal PDF file is required.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.txt"
        filepath = os.path.join(config.REPORTS_DIR, filename)

        try:
            with open(filepath, "w") as f:
                f.write(f"Query: {user_query}\n")
                f.write(f"Generated: {timestamp}\n")
                f.write("-" * 40 + "\n")
                f.write(report)
            return {"success": True, "file": filepath}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _update_dashboard(self, user_query: str, report: str, analysis: dict) -> dict:
        """Appends this run's summary to a JSON file a real dashboard UI
        could read from and render."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "query": user_query,
            "report": report,
            "confidence": analysis.get("confidence", "unknown"),
        }

        dashboard_data = []
        if os.path.exists(config.DASHBOARD_PATH):
            try:
                with open(config.DASHBOARD_PATH, "r") as f:
                    dashboard_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                dashboard_data = []

        dashboard_data.append(entry)

        try:
            with open(config.DASHBOARD_PATH, "w") as f:
                json.dump(dashboard_data, f, indent=2)
            return {"success": True, "file": config.DASHBOARD_PATH}
        except Exception as e:
            return {"success": False, "error": str(e)}
