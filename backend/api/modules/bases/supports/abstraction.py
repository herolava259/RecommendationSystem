from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel as DtoModel
from typing import Dict, Any, List, Generator, Tuple


class ISupportRepository(ABC):

	@abstractmethod
	async def exist_record(self, idx: UUID) -> bool:
		raise NotImplementedError()


	@abstractmethod
	def find_by_id(self, idx: UUID) -> DtoModel:
		raise NotImplementedError()


	@abstractmethod
	async def find_by_field(self, field_name: str, value: Any) -> List[DtoModel]:
		raise NotImplementedError()


	@abstractmethod
	async def find_all(self) -> List[DtoModel]:
		raise NotImplementedError()


	@abstractmethod
	async def find_all_by_condition(self, condition: Dict[str, Any]) -> List[DtoModel] | Generator[DtoModel, None, None]:
		raise NotImplementedError()

	@abstractmethod
	async def update(self, model: DtoModel) -> Tuple[bool, DtoModel]:
		raise NotImplementedError()

	@abstractmethod
	async def partial_update(self, model: DtoModel, update_properties: List[str]) -> Tuple[bool, DtoModel]:
		raise NotImplementedError()

	@abstractmethod
	async def query_raw(self, query_question: str, parameters: Dict[str, Any]) -> List[DtoModel]:
		raise NotImplementedError()

	@abstractmethod
	async def query_raw_take_first(self, query_question: str, parameters: Dict[str, Any]) -> DtoModel:
		raise NotImplementedError( )

	@abstractmethod
	async def delete(self, model: DtoModel, soft_delete: bool = False) -> bool:
		raise NotImplementedError()


	async def delete_by_id(self, idx: UUID) -> Tuple[bool, DtoModel]:
		raise NotImplementedError()

	"""mapping-fields from model to columns name of database"""
	mapping_fields: Dict[str, Any]


