from datetime import datetime
from typing import List, Optional
from uuid import UUID

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundExcepition, BaseException


class ProductUsecase:
    def __init__(self):
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            product_model = ProductModel(**body.model_dump())
            await self.collection.insert_one(product_model.model_dump())

            return ProductOut(**product_model.model_dump())
        except Exception as e:
            raise BaseException(message="Error inserting product: " + str(e))

    async def get(self, id=UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundExcepition(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(
        self, min_price: Optional[float] = None, max_price: Optional[float] = None
    ) -> List[ProductOut]:
        filters = {}
        if min_price is not None:
            filters["price"] = {"$gt": min_price}
        if max_price is not None:
            if "price" in filters:
                filters["price"]["$lt"] = max_price
            else:
                filters["price"] = {"$lt": max_price}

        return [ProductOut(**item) async for item in self.collection.find(filters)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        body_dicty = body.model_dump(exclude_none=True)
        body_dicty["updated_at"] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body_dicty},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundExcepition(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundExcepition(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
