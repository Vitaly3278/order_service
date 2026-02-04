from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from app.database import Base

class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)  # остаток на складе
    price = Column(Numeric(10, 2), nullable=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)  # упрощённо
    created_at = Column(DateTime, default=func.now())

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    nomenclature_id = Column(Integer, ForeignKey("nomenclature.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
