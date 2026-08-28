"""
Report Agent: turns a VALIDATED analysis into a professional,
human-readable report.
"""

import config


class ReportAgent:
    def __init__(self, llm=None):
        self.llm = llm or config.get_llm()

    def run(self, user_query: str, analysis: dict) -> str:
        prompt = f"""
You are a professional research report writer.

Using ONLY the validated analysis below, write a clear, well-structured
report (4-6 sentences) answering the user's question.

User question: {user_query}

Validated analysis:
{analysis}

Report:
"""
        response = self.llm.invoke(prompt).content
        if "Report:" in response:
            response = response.split("Report:")[-1].strip()
        return response.strip()
