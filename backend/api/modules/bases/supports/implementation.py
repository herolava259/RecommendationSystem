from abc import ABC
from typing import Generic, Tuple, Optional, Dict, Any, List, Sequence, Generator
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from modules.bases.supports.abstraction import ISupportRepository, TEntity, TModel

import sqlalchemy.dialects.postgresql as pg

from sqlmodel import select, exists, update, delete

from sqlalchemy.orm import contains_eager, joinedload


class SupportRepository(ISupportRepository, Generic[TEntity, TModel]):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(self, model: TModel, refresh_data=False) -> Tuple[bool, Optional[TModel]]:
        pass

    async def exist_record(self, idx: UUID) -> bool:
        pass

    def find_by_id(self, idx: UUID) -> TModel:
        pass

    async def find_by_field(self, field_name: str, value: Any) -> List[TModel]:
        pass

    async def find_all(self) -> List[TModel]:
        pass

    async def find_all_by_condition(self, condition: Dict[str, Any]) -> Sequence[TModel] | Generator[
        TModel, None, None]:
        pass

    async def partial_update(self, model: TModel, update_properties: List[str], refresh_data: bool = False) -> Tuple[
        bool, Optional[TModel]]:
        pass

    async def delete_by_id(self, idx: UUID) -> TModel:
        pass

    async def delete(self, model: TModel) -> bool:
        pass

    async def query_raw_take_first(self, query_question: str, parameters: Dict[str, Any]) -> TModel:
        pass

    async def query_raw(self, query_question: str, parameters: Dict[str, Any]) -> List[TModel]:
        pass


async def update(self, model: TModel, refresh_data=False) -> Tuple[bool, Optional[TModel]]:
    pass