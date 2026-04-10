import json
from pathlib import Path
from .base import UserStorage


class FileSystemUserStorage(UserStorage):
    def __init__(self, base_dir: str = "users_data"):
        self.base = Path(base_dir)
        self.base.mkdir(exist_ok=True)

    def user_dir(self, user_id: int) -> Path:
        path = self.base / str(user_id)
        path.mkdir(exist_ok=True)
        return path

    def _config_path(self, user_id: int) -> Path:
        return self.user_dir(user_id) / "config.json"

    def get_config(self, user_id: int) -> dict:
        path = self._config_path(user_id)
        if not path.exists():
            return {}
        return json.loads(path.read_text())

    def save_config(self, user_id: int, data: dict) -> None:
        self._config_path(user_id).write_text(json.dumps(data, indent=2))

    def files_dir(self, user_id: int) -> Path:
        path = self.user_dir(user_id) / "files"
        path.mkdir(exist_ok=True)
        return path

    def images_dir(self, user_id: int) -> Path:
        path = self.user_dir(user_id) / "images"
        path.mkdir(exist_ok=True)
        return path
