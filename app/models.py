from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from database import Base


class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(255))
    quantity = mapped_column(Integer)
    price = mapped_column(Numeric(10, 2))

    order_items = relationship("OrderItem", back_populates="nomenclature")


class Order(Base):
    __tablename__ = "orders"

    id = mapped_column(Integer, primary_key=True, index=True)
    client_id = mapped_column(Integer)
    created_at = mapped_column(DateTime, server_default=func.now())

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = mapped_column(Integer, primary_key=True, index=True)
    order_id = mapped_column(Integer, ForeignKey('orders.id'))
    nomenclature_id = mapped_column(Integer, ForeignKey('nomenclature.id'))
    quantity = mapped_column(Integer)

    order = relationship("Order", back_populates="items")
    nomenclature = relationship("Nomenclature", back_populates="order_items")

