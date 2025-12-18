from abc import ABC
from datetime import datetime
from typing import Generic, Tuple, Optional, Dict, Any, List, Sequence, Generator, Type, Mapping
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from modules.bases.supports.abstraction import ISupportRepository, TEntity, TModel

import sqlalchemy.dialects.postgresql as pg

from sqlmodel import select, exists, update, delete, text, bindparam, Integer, String, UUID as SqlUID, Date as SQLDate, Boolean, Float

from sqlalchemy.orm import contains_eager, joinedload

from modules.bases.supports.errors import RecordNotFound


data_type_mapping = {
    int: Integer,
    str: String,
    bool: Boolean,
    datetime: SQLDate,
    UUID: SqlUID,
    float: Float,
}


class SupportRepository(ISupportRepository, Generic[TEntity, TModel]):

    def __init__(self, entity_type: Type[TEntity], dto_type: Type[TModel], session: AsyncSession,):
        self.session = session
        self.entity_cls = entity_type
        self.dto_cls = dto_type

    async def update(self, model: TModel, refresh_data=False) -> Tuple[bool, Optional[TModel]]:

        query = select(self.entity_cls).where(self.entity_cls.id == model.id)

        record = (await self.session.exec(query)).first()

        if record is None:
            return False, None

        for k, v in model.model_dump().items():
            if v is None:
                continue
            setattr(record, k, v)
        await self.session.commit()

        if refresh_data:
            await self.session.refresh(record)

        return True, model.__class__(**record.model_dump())


    async def exist_record(self, idx: UUID) -> bool:
        query = exists(self.entity_cls).where(self.entity_cls.id == idx)
        result = await self.session.exec(query)

        return result.scalar()

    async def find_by_id(self, idx: UUID) -> Optional[TModel]:
        query = select(self.entity_cls).where(self.entity_cls.id == idx)

        result = await self.session.exec(query)

        record = result.first()

        if record is None:
            return None

        return self.dto_cls(**record.model_dump())


    async def find_by_field(self, field_name: str, value: Any) -> Sequence[TModel]:
        if field_name not in self.entity_cls.model_fields.keys():
            raise KeyError(f"Field {field_name} is not defined")
        query = select(self.entity_cls).where(getattr(self.entity_cls, field_name) == value)

        result = await self.session.exec(query)
        records = result.all()
        return [self.dto_cls(**record.model_dump()) for record in records ]


    async def find_all(self) -> List[TModel]:
        query = select(self.entity_cls)

        result = await self.session.exec(query)
        records = result.all()
        return [self.dto_cls(**record.model_dump()) for record in records]

    async def find_all_by_condition(self, condition: Dict[str, Any]) -> Sequence[TModel] | Generator[
        TModel, None, None]:

        field_names = condition.keys()

        if not (set(self.entity_cls.model_fields.keys()) >= set(field_names)):
            raise KeyError(f"Field condition {list(condition.keys())} is not defined")
        query = select(self.entity_cls).where(*[getattr(self.entity_cls, fn) == value for fn, value in condition.items()])
        result = await self.session.exec(query)

        records = result.all()

        return [self.dto_cls(**record.model_dump()) for record in records]



    async def partial_update(self, model: TModel, update_properties: List[str], refresh_data: bool = False) -> Tuple[
        bool, Optional[TModel]]:

        if not set(self.entity_cls.model_fields.keys()) >= set(update_properties):
            raise KeyError(f"Field {update_properties} is not defined")

        query = select(self.entity_cls).where(self.entity_cls.id == model.id)

        result = await self.session.exec(query)
        record = result.first()

        if not record:
            raise RecordNotFound(f"Record {model.id} is not found")
        for field in update_properties:
            setattr(record, field, getattr(model, field))

        await self.session.commit()

        if refresh_data:
            await self.session.refresh(record)
            model = model.__class__(**record.model_dump())
        return True, model


    async def delete_by_id(self, idx: UUID) -> bool:
        record = await self.session.get_one(self.entity_cls, idx)

        if not record:
            return False
        await self.session.delete(record)
        await self.session.commit()

        return True

    async def delete(self, model: TModel) -> bool:
        return await self.delete_by_id(model.id)

    async def query_raw_take_first(self, query_question: str, **kwargs) -> TModel:
        query = (
            text(query_question)
            .bindparams(
                *[bindparam(name, type_=data_type_mapping[type(value)]) for name, value in kwargs.items()]
            )
        )

        result = await self.session.execute(query, kwargs)

        record = result.first()

        return self.dto_cls(**record.model_dump())

    async def query_raw(self, query_question: str, parameters: Dict[str, Any]) -> List[TModel]:
        query = (
            text(query_question)
            .bindparams(
                *[bindparam(name, type_=data_type_mapping[type(value)]) for name, value in parameters.items()]
            )
        )

        result = await self.session.execute(query, parameters)

        record = result.first()

        return self.dto_cls(**record.model_dump())


    async def bulk_update(self, models: Sequence[TModel], update_fields: Sequence[str] | None = None) -> bool:

        if not update_fields:
            update_fields = set(self.entity_cls.model_fields.keys())
        else:
            update_fields = set(update_fields)
        if len(set(map(lambda model: model.id, models))) != len(models):
            return False

        if not set(self.entity_cls.model_fields.keys()) >= update_fields:
            return False

        ids = map(lambda x: x.id, models)
        query = select(self.entity_cls).where(self.entity_cls.id.in_(ids))

        result = await self.session.exec(query)

        records = result.all()

        if len(records) != len(models):
            return False
        models_lookup = {model.id: model for model in models}

        for record in records:
            model = models_lookup[record.id]

            for field_name in update_fields:
                setattr(model, field_name, getattr(model, field_name))

        await self.session.commit()

        return True

    async def bulk_update_with_condition(self, condition: Dict[str, Any], mapping_fields: Mapping[str, Any]) -> bool:

        if not mapping_fields:
            return False
        valid_fields = set(mapping_fields.keys()) & set(self.entity_cls.model_fields.keys())
        mapping_fields = {field: mapping_fields[field] for field in valid_fields}

        stmt = update(self.entity_cls).where(*[getattr(self.entity_cls, fn) == value for fn, value in condition.items()]).values(**mapping_fields)

        result = await self.session.exec(stmt)

        await self.session.commit()

        return True






