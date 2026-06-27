import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class GeminiTaxAgent:
    """
    Advanced Tax Analyzer Agent powered by Google Gemini 1.5 Pro.
    Specialized in Uzbekistan Tax Code (Soliq Kodeksi).
    """
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # System instructions define the agent's "training" and persona
        self.system_instruction = """
        Siz "AI BUXGALTER" tizimining bosh soliq tahlilchisisiz. 
        Sizning asosiy vazifangiz O'zbekiston Respublikasi Soliq Kodeksi (yangi tahriri) va 2026-yilgi yangi o'zgarishlar asosida buxgalterlarga maslahat berish.
        
        Siz quyidagi yangi (2026) sohalarda ekspertsiz:
        1. Maxsus renta solig'i (Oltin 10%, Mis/Kumush 15%, Uran 16%).
        2. Zargarlik buyumlari (Oltin uchun 2000 so'm/gramm).
        3. Elektron tijorat (Foyda 10%, Aylanma 3%).
        4. Shakarli ichimliklar (500-535 so'm/litr).
        5. Eksport daromadlari (4% umumiy, 3% e-commerce).
        6. O'zini o'zi band qilganlar (1% soliq, 12% ijara).
        7. Aksiz solig'i 2026 yangi stavkalari.
        8. Mol-mulk (1.5%) va Yer soliqlari.
        
        Tizimda barcha stavkalar 'tax_rules' jadvalida saqlanadi. Agar foydalanuvchi stavka haqida so'rasa, yangi 2026 qoidalariga tayaning.
        Javoblaringiz aniq, professional va qonun moddalariga havola berilgan holda bo'lishi kerak.
        Faqat O'zbekiston qonunchiligi haqida gapiring.
        """
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=self.system_instruction
        )

    async def get_tax_advice(self, query: str, company_context: Dict[str, Any] = None) -> str:
        prompt = f"Foydalanuvchi savoli: {query}\n"
        if company_context:
            prompt += f"Kompaniya konteksti: {company_context}"
            
        chat = self.model.start_chat(history=[])
        response = chat.send_message(prompt)
        return response.text

    async def analyze_report(self, report_data: Dict[str, Any]) -> str:
        prompt = f"Quyidagi hisobot ma'lumotlarini tahlil qiling va xatoliklarni toping: {report_data}"
        response = self.model.generate_content(prompt)
        return response.text
    async def prepare_vat_report(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        AI agent prepares a VAT report structure based on transactions.
        """
        prompt = f"""
        Quyidagi tranzaksiyalar asosida QQS (VAT) hisoboti shaklini tayyorlang:
        Tranzaksiyalar: {transactions}
        
        Natijani FAQAT ushbu JSON formatida bering:
        {{
          "year": 2026,
          "month": 1,
          "total_sales": number,
          "exempt_sales": number,
          "total_purchases": number,
          "taxable_purchases": number,
          "calculated_vat": number,
          "explanation": "Qisqacha izoh"
        }}
        """
        response = self.model.generate_content(prompt)
        import json
        return json.loads(response.text)

    async def extract_data_from_document(self, file_path: str) -> Dict[str, Any]:
        """
        Uses Gemini Vision to extract structured data from an image or PDF document.
        """
        # Load the file
        with open(file_path, "rb") as f:
            file_data = f.read()
            
        # Use a specialized prompt for OCR
        prompt = """
        Ushbu hujjatni (invoice, shartnoma yoki kvitansiya) tahlil qiling va undagi barcha 
        muhim ma'lumotlarni (STIR, summa, sana, mahsulot nomi, yetkazib beruvchi) JSON formatida chiqaring.
        Faqat JSON natijasini qaytaring.
        """
        
        # Prepare content for Gemini
        response = self.model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": file_data}
        ])
        
        import json
        try:
            return json.loads(response.text)
        except:
            return {"error": "Ma'lumotlarni o'qib bo'lmadi", "raw": response.text}

    async def categorize_transactions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        AI agent categorizes bank transactions into accounting expense types.
        """
        prompt = f"""
        Quyidagi bank tranzaksiyalarini tahlil qiling va har biriga tegishli buxgalteriya 
        kategoriyasini (masalan: Ish haqi, Ijara, Kanselyariya, Soliq, Tovar xaridi) biriktiring:
        Tranzaksiyalar: {transactions}
        
        Natijani JSON formatida qaytaring.
        """
        response = self.model.generate_content(prompt)
        import json
        return json.loads(response.text)

    async def simulate_tax_scenario(self, current_data: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates how specific business changes affect tax liabilities in Uzbekistan.
        """
        prompt = f"""
        Hozirgi holat: {current_data}
        Kutilayotgan o'zgarishlar: {changes}
        
        Ushbu o'zgarishlar soliq yukiga (QQS, Foyda solig'i, Ijtimoiy soliq) qanday ta'sir qilishini hisoblab bering.
        O'zbekistonning 2026-yilgi soliq stavkalarini hisobga oling.
        
        Natijani JSON formatida qaytaring:
        {{
          "old_tax_total": number,
          "new_tax_total": number,
          "difference": number,
          "advice": "Kompaniya uchun foydali yoki zararli ekanligi bo'yicha tavsiya"
        }}
        """
        response = self.model.generate_content(prompt)
        import json
        return json.loads(response.text)
