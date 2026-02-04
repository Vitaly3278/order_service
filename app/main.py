from fastapi import FastAPI, HTTPException
from app.schemas import AddItemRequest, AddItemResponse
from app.services import add_item_to_order
from app.database import engine
from app.models import Base

try:
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы или уже существуют")
except Exception as e:
    print(f"Ошибка при создании таблиц: {e}")

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

@app.get("/")
def root():
    return {"message": "Order Service API"}

