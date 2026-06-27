import os
from groq import Groq
from typing import Dict, Any, List
import json

class ComplianceGuardAgent:
    """
    Tax Compliance Agent powered by Groq (Llama 3).
    Acts as a second-layer auditor to verify tax reports for errors and law compliance.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama3-70b-8192" # Using the large Llama 3 model for high reasoning

    async def audit_report(self, report_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Audits a generated report for mathematical and legal inconsistencies.
        """
        prompt = f"""
        Siz O'zbekiston soliq auditi bo'yicha mustaqil nazoratchisiz. 
        Quyidagi hisobot ma'lumotlarini tekshiring va har qanday xatolik yoki riskni aniqlang:
        
        Hisobot ma'lumotlari: {json.dumps(report_data, indent=2)}
        Kontekst (Qonunchilik/Tarix): {json.dumps(context, indent=2) if context else "Standard 2026 Rules"}
        
        Sizning vazifangiz:
        1. Matematik hisob-kitoblar to'g'riligini tekshirish (QQS 12%, aylanma stavkalari va h.k.).
        2. O'zbekiston Soliq Kodeksi (2026) bo'yicha cheklovlar buzilmaganini tasdiqlash.
        3. Hisobotda "shubhali" ko'ringan joylarni belgilash.
        
        Javobni FAQAT ushbu JSON formatida bering:
        {{
          "audit_status": "Pass" | "Warning" | "Fail",
          "detected_errors": ["xato 1", "xato 2"],
          "legal_risks": ["risk 1", "risk 2"],
          "audit_score": number (0-100),
          "comments": "Auditorning yakuniy xulosasi"
        }}
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Siz qattiqqo'l va aniq ishlaydigan soliq auditorisiz. Faqat JSON formatida javob berasiz."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
            response_format={"type": "json_object"}
        )
        
        return json.loads(chat_completion.choices[0].message.content)
