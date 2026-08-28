"""
Orchestrator Agent: the coordinator for the entire pipeline shown across
both architecture diagrams:

USER -> Orchestrator -> [PDF Agent, API Agent, Sheet Agent] (parallel)
     -> merge -> Analysis Agent -> Critic Agent
     -> ERROR: retry Retrieval  |  VALID: Report Agent
     -> Action Agent -> [PDF Report, Dashboard, Email]
"""

import config
from agents.retrieval_agent import RetrievalAgent
from agents.analysis_agent import AnalysisAgent
from agents.critic_agent import CriticAgent
from agents.report_agent import ReportAgent
from agents.action_agent import ActionAgent


class OrchestratorAgent:
    def __init__(self):
        llm = config.get_llm()
        self.retrieval_agent = RetrievalAgent()
        self.analysis_agent = AnalysisAgent(llm)
        self.critic_agent = CriticAgent(llm)
        self.report_agent = ReportAgent(llm)
        self.action_agent = ActionAgent()

    def run(self, user_query: str, api_url: str = None) -> dict:
        print("=" * 70)
        print(f"USER QUERY: {user_query}")
        print("=" * 70)

        analysis = None
        attempt = 0

        while attempt <= config.MAX_RETRIEVAL_RETRIES:
            attempt += 1
            print(f"\n[Orchestrator] Retrieval attempt {attempt}...")

            retrieval_result = self.retrieval_agent.run(api_url)
            print("[Orchestrator] Retrieval complete (PDF + API + Sheet agents merged).")

            print("[Orchestrator] Running Analysis Agent...")
            analysis = self.analysis_agent.run(user_query, retrieval_result["merged_context"])

            print("[Orchestrator] Running Critic Agent...")
            verdict = self.critic_agent.run(user_query, analysis)
            print(f"[Orchestrator] Critic verdict: {verdict}")

            if verdict.get("status") == "VALID":
                break

            print("[Orchestrator] Critic flagged an ERROR -- retrying retrieval...")
        else:
            print("\n[Orchestrator] Max retries reached; proceeding with best available analysis.")

        print("\n[Orchestrator] Running Report Agent...")
        report = self.report_agent.run(user_query, analysis)

        print("[Orchestrator] Running Action Agent (distributing report)...")
        action_results = self.action_agent.run(user_query, report, analysis)

        print("\n" + "=" * 70)
        print("FINAL REPORT")
        print("=" * 70)
        print(report)

        return {
            "query": user_query,
            "analysis": analysis,
            "report": report,
            "actions": action_results,
        }
