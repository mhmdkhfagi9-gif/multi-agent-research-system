"""
Critic Agent: reviews the Analysis Agent's output and decides whether it is
VALID (proceed to the Report Agent) or an ERROR (send the flow back to the
Retrieval Agent for another attempt), matching the ERROR/VALID branch in
the architecture diagram.
"""

import json
import re

import config


class CriticAgent:
    def __init__(self, llm=None):
        self.llm = llm or config.get_llm()

    def run(self, user_query: str, analysis: dict) -> dict:
        prompt = f"""
You are a quality-control critic reviewing an AI research analysis.

User question: {user_query}

Analysis to review:
{json.dumps(analysis, indent=2)}

Check for:
- Low confidence
- Conflicting sources with no explanation
- Empty or missing key findings

Return ONLY a JSON object:
{{"status": "VALID" or "ERROR", "reason": "..."}}
"""
        response = self.llm.invoke(prompt).content
        result = self._extract_json(response)

        # Defensive default: if the critic's own output is unparseable,
        # fail safe by treating it as VALID rather than looping forever.
        if "status" not in result:
            result = {"status": "VALID", "reason": "Critic output unparseable; defaulting to VALID."}
        return result

    @staticmethod
    def _extract_json(text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {}
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {}
