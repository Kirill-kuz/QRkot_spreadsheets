from typing import (
    Generic,
    List,
    Optional,
    Type,
    TypeVar)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar(
    'CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar(
    'UpdateSchemaType', bound=BaseModel)


class CRUDBase(
    Generic[ModelType,
            CreateSchemaType,
            UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            session: AsyncSession,
            commit: bool = True
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_opens(
            self, session: AsyncSession) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == false()
            )
        )
        db_objs = db_objs.scalars().all()
        return db_objs

    async def get_not_invested(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        return (await session.scalars(
            select(self.model).where(
                self.model.fully_invested == 0
            )
        )).all()
