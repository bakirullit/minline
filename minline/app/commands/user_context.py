class UserContext:
    def __init__(self, storage, user_id: int):
        self._storage = storage
        self.user_id = user_id

    @property
    def config(self) -> dict:
        return self._storage.get_config(self.user_id)

    def save_config(self, data: dict):
        self._storage.save_config(self.user_id, data)

    @property
    def files_dir(self):
        return self._storage.files_dir(self.user_id)

    @property
    def images_dir(self):
        return self._storage.images_dir(self.user_id)
