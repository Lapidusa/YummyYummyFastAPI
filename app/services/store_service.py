from uuid import UUID
from typing import Sequence, List

from asyncpg import Polygon
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Store
from app.db.models import Store as StoreModel
from app.schemas.store import CreateStore, UpdateStore

class StoreService:
  @staticmethod
  async def get_store_by_id(db: AsyncSession, store_id: UUID) -> StoreModel:
    query = select(StoreModel).where(StoreModel.id == store_id)
    result = await db.execute(query)
    store = result.scalar_one_or_none()
    if not store:
      raise NoResultFound(f"Store with ID {store_id} not found")
    return store

  @staticmethod
  async def get_all_stores(db: AsyncSession) -> List[Store]:
    query = select(StoreModel)
    result = await db.execute(query)
    stores = list(result.scalars().all())
    return stores

  @staticmethod
  async def create_store(db: AsyncSession, store_data: CreateStore) -> Store:
    new_store = StoreModel(
      address=store_data.address,
      start_working_hours=store_data.start_working_hours,
      end_working_hours=store_data.end_working_hours,
      start_delivery_time=store_data.start_delivery_time,
      end_delivery_time=store_data.end_delivery_time,
      phone_number=store_data.phone_number,
      min_order_price= store_data.min_order_price
    )
    db.add(new_store)
    await db.commit()
    await db.refresh(new_store)

    for zone_data in store_data.delivery_zones:
      # Преобразуем координаты в полигон
      polygon = Polygon(zone_data.coordinates)
      delivery_zone = DeliveryZone(
        name=zone_data.name,
        area=from_shape(polygon, srid=4326),  # Преобразуем в формат GeoAlchemy
        store_id=store.id,
      )
      db.add(delivery_zone)
    await db.commit()
    return new_store

  @staticmethod
  async def update_store(db: AsyncSession, store_data: UpdateStore) -> StoreModel:
    store = await StoreService.get_store_by_id(db, store_data.id)
    store.address = store_data.address
    store.start_working_hours = store_data.start_working_hours
    store.end_working_hours = store_data.end_working_hours
    store.start_delivery_time = store_data.start_delivery_time
    store.end_delivery_time = store_data.end_delivery_time
    store.phone_number = store_data.phone_number

    await db.commit()
    await db.refresh(store)
    return store

  @staticmethod
  async def delete_store(db: AsyncSession, store_id: UUID) -> None:
    store = await StoreService.get_store_by_id(db, store_id)
    await db.delete(store)
    await db.commit()

