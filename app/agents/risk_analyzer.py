import google.generativeai as genai
import json
from typing import Dict, Any, List

class RiskAnalyzerAgent:
    """
    AI Agent that analyzes financial data using Gemini 1.5 Pro to detect potential tax risks and penalties.
    Tailored for Uzbekistan tax legislation.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={"response_mime_type": "application/json"}
        )

    async def analyze_tax_risk(self, company_data: Dict[str, Any], recent_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = f"""
        Siz O'zbekiston soliq qonunchiligi bo'yicha ekspert AI-buxgaltersiz. 
        Quyidagi kompaniya ma'lumotlarini tahlil qiling va yuzaga kelishi mumkin bo'lgan soliq risklarini aniqlang:
        
        Kompaniya ma'lumotlari: {company_data}
        Oxirgi hisobotlar/aylanmalar: {recent_reports}
        
        Tahlil quyidagilarni o'z ichiga olishi shart:
        1. QQS (VAT) hisoblashdagi tafovutlar.
        2. Yuqori riskli (at-risk) guruhiga tushish ehtimoli.
        3. O'tkazib yuborilgan muddatlar yoki hujjatlar.
        4. Bashorat qilinayotgan jarimalar miqdori (so'mda).
        
        Javobni FAQAT ushbu tuzilmada JSON formatida bering:
        {{
          "risk_level": "Low" | "Medium" | "High",
          "main_concerns": ["muammo 1", "muammo 2"],
          "suggested_actions": ["tavsiya 1", "tavsiya 2"],
          "estimated_penalty": "string (masalan: 15,000,000 so'm)",
          "uzbekistan_law_reference": "Tegishli soliq kodeksi moddalari"
        }}
        """
        
        response = self.model.generate_content(prompt)
        return json.loads(response.text)
