from abc import ABC, abstractmethod
from typing import BinaryIO, Tuple, Dict


class StorageProvider(ABC):

    @abstractmethod
    def get_files(self, file_path: str) -> str:
        pass

    @abstractmethod
    def upload_file(self, file: BinaryIO, filename: str, tags: Dict[str, str]) -> Tuple[bytes, str]:
        pass

    @abstractmethod
    def delete_file(self, file_path: str):
        pass

    @abstractmethod
    def delete_all_files(self) -> None:
        pass
    
