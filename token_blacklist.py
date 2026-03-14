from typing import Set, List

from data_store import DataStore


class TokenBlacklist:
    def __init__(self, data_dir: str = "data"):
        self.tokens: Set[str] = set()
        self.store = DataStore(data_dir)

    def load(self, filename: str = "token_blacklist.json"):
        data = self.store.load_list(filename)
        self.tokens = set(data)
        return list(self.tokens)

    def save(self, filename: str = "token_blacklist.json"):
        self.store.save_list(filename, list(self.tokens))

    def add(self, token: str):
        self.tokens.add(token)

    def contains(self, token: str) -> bool:
        return token in self.tokens
