from fastapi import APIRouter
from pydantic import BaseModel
import qrcode
import io
import base64

router = APIRouter()

class QrRequest(BaseModel):
    data: str

@router.post("/")
async def generate_qr(request: QrRequest):
    qr_data = request.data
    qr_img = qrcode.make(qr_data)
    buffered = io.BytesIO()
    qr_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return {"qr_code_base64": img_str}

