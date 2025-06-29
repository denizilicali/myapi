from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from stdnum import iban

router = APIRouter()

class IbanRequest(BaseModel):
    iban_number: str

@router.post("/")
async def validate_iban(request: IbanRequest):
    iban_number = request.iban_number.replace(" ", "").upper()
    try:
        if iban.is_valid(iban_number):
            return {"iban": iban_number, "valid": True}
        else:
            return {"iban": iban_number, "valid": False}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
