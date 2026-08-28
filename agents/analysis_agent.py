"""
Analysis Agent: takes the merged context from the Retrieval Agent and uses
the LLM to analyze and cross-validate information across the different
sources (PDF, API, Sheet), producing structured JSON findings.
"""

import json
import re

import config


class AnalysisAgent:
    def __init__(self, llm=None):
        self.llm = llm or config.get_llm()

    def run(self, user_query: str, merged_context: str) -> dict:
        prompt = f"""
You are a research analysis agent. You are given information retrieved from
multiple sources (PDF documents, an external API, and spreadsheet data).

Your job:
1. Identify the key facts relevant to the user's question.
2. Cross-check whether the sources agree or contradict each other.
3. Note anything that seems missing or unclear.

Do NOT invent information that isn't present in the context below.

User question: {user_query}

Retrieved context:
{merged_context}

Return ONLY a JSON object in this exact format:
{{
  "key_findings": ["...", "..."],
  "cross_source_agreement": "agree" or "conflict" or "insufficient_data",
  "notes": "...",
  "confidence": "high" or "medium" or "low"
}}
"""
        response = self.llm.invoke(prompt).content
        return self._extract_json(response)

    @staticmethod
    def _extract_json(text: str) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {
                "key_findings": [],
                "cross_source_agreement": "insufficient_data",
                "notes": "Could not parse analysis output.",
                "confidence": "low",
                "raw_output": text,
            }
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {
                "key_findings": [],
                "cross_source_agreement": "insufficient_data",
                "notes": "Malformed JSON from analysis step.",
                "confidence": "low",
                "raw_output": text,
            }
