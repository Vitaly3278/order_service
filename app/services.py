from app.models import Nomenclature, Order, OrderItem
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import AddItemRequest, AddItemResponse

def add_item_to_order(request: AddItemRequest):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == request.order_id).first()
        if not order:
            return AddItemResponse(
                success=False,
                message=f"Заказ с ID {request.order_id} не найден"
            )

        item = db.query(Nomenclature).filter(Nomenclature.id == request.nomenclature_id).first()
        if not item:
            return AddItemResponse(
                success=False,
                message=f"Товар с ID {request.nomenclature_id} не найден"
            )
        if item.quantity < request.quantity:
            return AddItemResponse(
                success=False,
                message=f"Недостаточно товара на складе. Доступно: {item.quantity}, запрошено: {request.quantity}"
            )

        existing_item = db.query(OrderItem).filter(
            OrderItem.order_id == request.order_id,
            OrderItem.nomenclature_id == request.nomenclature_id
        ).first()

        if existing_item:
            existing_item.quantity += request.quantity
            message = f"Количество товара обновлено (теперь {existing_item.quantity})"
        else:
            new_item = OrderItem(
                order_id=request.order_id,
                nomenclature_id=request.nomenclature_id,
                quantity=request.quantity
            )
            db.add(new_item)
            existing_item = new_item
            message = "Товар добавлен в заказ"

        item.quantity -= request.quantity

        db.commit()
        return AddItemResponse(
            success=True,
            message=message,
            order_item_id=existing_item.id
        )

    except SQLAlchemyError as e:
        db.rollback()
        return AddItemResponse(
            success=False,
            message=f"Ошибка базы данных: {str(e)}"
        )
    finally:
        db.close()
