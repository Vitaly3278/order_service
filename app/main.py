from fastapi import FastAPI, Depends, HTTPException
from app.schemas import AddItemRequest, AddItemResponse
from app.services import add_item_to_order
from app.database import get_db

app = FastAPI(title="Order Service", description="API для добавления товаров в заказ")

@app.post("/add-item", response_model=AddItemResponse)
def add_item(request: AddItemRequest):
    response = add_item_to_order(request)
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}
