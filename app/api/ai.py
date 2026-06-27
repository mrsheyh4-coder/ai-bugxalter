from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..agents.orchestrator import BossAgent
import os
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Consultation"])

class ConsultationRequest(BaseModel):
    query: str
    company_id: int = None

@router.post("/consult")
async def get_ai_consultation(request: ConsultationRequest, db: Session = Depends(get_db)):
    # Initialize BossAgent (In a real app, this would be a singleton)
    boss = BossAgent(
        gemini_key=os.getenv("GEMINI_API_KEY"),
        groq_key=os.getenv("GROQ_API_KEY")
    )
    
    try:
        # For now, we assume all queries are tax-related and route to Gemini
        response = await boss.get_tax_consultation(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
