import json
import re
import config

class AnalysisAgent:
    def __init__(self, llm=None):
        self.llm = llm or config.get_llm()

    def run(self, user_query: str, merged_context: str) -> dict:
        max_chars = 12000
        if len(merged_context) > max_chars:
            merged_context = merged_context[:max_chars] + "\n\n[Content truncated due to length...]"

        prompt = f"""You are a research analysis agent. You are given information retrieved from multiple sources (PDF documents, an external API, and spreadsheet data).

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
        try:
            response = self.llm.invoke(prompt).content
        except Exception as e:
            return {
                "key_findings": [f"Error during analysis: {str(e)}"],
                "cross_source_agreement": "insufficient_data",
                "notes": f"LLM failed: {str(e)}",
                "confidence": "low",
                "raw_output": str(e),
            }
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
