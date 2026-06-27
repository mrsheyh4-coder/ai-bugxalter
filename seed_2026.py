import sys
import os
from datetime import datetime

# Add the backend directory to the path so we can import modules reliably
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.database import DATABASE_URL, SessionLocal
from app.models.models import TaxRule

def seed_2026_taxes():
    db = SessionLocal()
    try:
        rules = [
            # 1. Special Rent Tax (Mining) - 2026 Updates
            TaxRule(tax_type="renta", meta_data={"resource": "oltin"}, rate=10, taxpayer_type="tog-kon", effective_from=datetime(2026, 1, 1)),
            TaxRule(tax_type="renta", meta_data={"resource": "kumush"}, rate=15, taxpayer_type="tog-kon", effective_from=datetime(2026, 1, 1)),
            TaxRule(tax_type="renta", meta_data={"resource": "uran"}, rate=16, taxpayer_type="tog-kon", effective_from=datetime(2026, 1, 1)),
            
            # 2. Jewelry Tax
            TaxRule(tax_type="zargarlik", fixed_amount=2000, unit="gramm", taxpayer_type="retail", effective_from=datetime(2026, 1, 1)),
            
            # 3. E-commerce Tax (Digital Economy)
            TaxRule(tax_type="ecommerce_profit", rate=10, taxpayer_type="online-store", effective_from=datetime(2026, 1, 1)),
            TaxRule(tax_type="ecommerce_turnover", rate=3, taxpayer_type="online-store", effective_from=datetime(2026, 1, 1)),
            
            # 4. Sugary Drinks & Harmful Goods
            TaxRule(tax_type="sugar_drink", fixed_amount=500, unit="litr", effective_from=datetime(2026, 1, 1)),
            TaxRule(tax_type="energy_drink", fixed_amount=2000, unit="litr", effective_from=datetime(2026, 1, 1)),
            
            # 5. Property Tax for Legal Entities
            TaxRule(tax_type="property_tax", rate=2, taxpayer_type="legal_entity", effective_from=datetime(2026, 1, 1)),
            
            # 6. Land Tax (Agriculture vs Industrial)
            TaxRule(tax_type="land_tax_agri", rate=0.95, unit="ga", taxpayer_type="farmer", effective_from=datetime(2026, 1, 1)),
            
            # 7. Self-Employed (Mustaqil Band)
            TaxRule(tax_type="self_employed_income", rate=1, taxpayer_type="self-employed", effective_from=datetime(2026, 1, 1)),
            TaxRule(tax_type="self_employed_rent", rate=12, taxpayer_type="self-employed", effective_from=datetime(2026, 1, 1)),

            # 8. New VAT (QQS) Thresholds
            TaxRule(tax_type="qqs_mandatory", meta_data={"threshold": 1000000000}, rate=12, effective_from=datetime(2026, 1, 1))
        ]
        
        db.add_all(rules)
        db.commit()
        print("2026 Tax Rules seeded successfully.")
    except Exception as e:
        print(f"Error seeding taxes: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print(f"Using database: {DATABASE_URL}")
    seed_2026_taxes()
