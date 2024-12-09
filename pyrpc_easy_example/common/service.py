from abc import ABC, abstractmethod
from .model import User


class UserService(ABC):
    @abstractmethod
    def get_user(self, user: User) -> User:
        pass
