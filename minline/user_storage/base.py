from abc import ABC, abstractmethod
from pathlib import Path


class UserStorage(ABC):
    @abstractmethod
    def user_dir(self, user_id: int) -> Path: ...

    @abstractmethod
    def get_config(self, user_id: int) -> dict: ...

    @abstractmethod
    def save_config(self, user_id: int, data: dict) -> None: ...

    @abstractmethod
    def files_dir(self, user_id: int) -> Path: ...

    @abstractmethod
    def images_dir(self, user_id: int) -> Path: ...
