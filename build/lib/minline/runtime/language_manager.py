import os
import json

class LanguageManager:
    _languages: dict[str, dict[str, str]] = {}

    def __init__(self, directory: str = "languages"):
        self.directory = directory
        self.load_languages(directory)

    @classmethod
    def load_languages(cls, folder_path: str = "languages"):
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                lang_code = filename.split(".")[0]
                full_path = os.path.join(folder_path, filename)
                with open(full_path, "r", encoding="utf-8") as f:
                    cls._languages[lang_code] = json.load(f)

    @classmethod
    def get(cls, lang: str, key: str) -> str:
        return cls._languages.get(lang, {}).get(key, key)


# Load on import
LanguageManager.load_languages()
