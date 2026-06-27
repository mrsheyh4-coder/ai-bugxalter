from .risk_analyzer import RiskAnalyzerAgent
from .compliance_agent import ComplianceGuardAgent
from typing import Dict, Any, List

class BossAgent:
    """
    The Supervisor Agent that coordinates all other specialized agents.
    Dual-AI Setup: Powered by Gemini 1.5 Pro and Groq (Llama 3).
    """
    def __init__(self, gemini_key: str, groq_key: str = None):
        self.risk_analyzer = RiskAnalyzerAgent(api_key=gemini_key)
        self.compliance_guard = ComplianceGuardAgent(api_key=groq_key)
        self.agents = {
            "preparer": "Gemini 1.5 Pro - Generates reports and analyzes complex data.",
            "auditor": "Groq (Llama 3) - Performs ultra-fast compliance audits."
        }

    async def get_tax_consultation(self, query: str, context: Dict[str, Any] = None):
        # 1. Preparation & Analysis by Gemini
        analysis = await self.risk_analyzer.analyze_tax_risk(
            company_data={"query": query}, 
            recent_reports=context or []
        )
        
        # 2. Independent Audit by Groq (Llama 3)
        audit_result = await self.compliance_guard.audit_report(analysis)
        
        return {
            "analysis": analysis,
            "audit": audit_result
        }

class AccountantAgent:
    """
    Agent specialized in financial data processing.
    """
    async def process_ehf(self, ehf_data: Dict[str, Any]):
        # AI logic to categorize invoice
        pass
