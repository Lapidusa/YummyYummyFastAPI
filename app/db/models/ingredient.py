import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Table, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

# Промежуточная таблица для связи "многие ко многим" между продуктами и ингредиентами
pizza_ingredients = Table(
    'pizza_ingredients',
    Base.metadata,
    Column('pizza_id', UUID(as_uuid=True), ForeignKey('pizzas.id'), primary_key=True),
    Column('ingredient_id', UUID(as_uuid=True), ForeignKey('ingredients.id'), primary_key=True)
)

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    is_removable = Column(Boolean, nullable=False, default=True)
    img = Column(String(255), nullable=True)
    price = Column(Float, nullable=True)
    count = Column(Integer, nullable=False, default=1)
    # Удаляем связь с продуктами, чтобы ингредиенты были только у пиццы
    # products = relationship("Pizza", secondary=pizza_ingredients, back_populates="ingredients")  # Убрано