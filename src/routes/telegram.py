from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()

    print(data)

    return {"status": "ok"}


# бот должен отвечать сообщениями из фастапи. 

