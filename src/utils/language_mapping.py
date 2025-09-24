class LanguageMapping:
    lang_map = {"en": "English", "vi": "Vietnamese"}

    @classmethod
    def map(cls, symbol: str) -> str:
        return cls.lang_map.get(symbol, "English")
