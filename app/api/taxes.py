from fastapi import APIRouter, Depends, HTTPException
from ..services.soliq_service import soliq_service

router = APIRouter(prefix="/taxes", tags=["Taxes"])

@router.get("/sync/{tin}")
async def sync_taxes(tin: str):
    """
    Sync tax data from soliq.uz for a specific TIN.
    """
    result = await soliq_service.get_balance(tin)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result
@router.post("/submit-vat")
async def submit_vat(data: dict):
    """
    Submit VAT report.
    """
    tin = data.get("tin")
    report_data = data.get("report_data")
    if not tin or not report_data:
        raise HTTPException(status_code=400, detail="TIN and report_data required")
        
    result = await soliq_service.submit_vat_report(tin, report_data)
    return result
