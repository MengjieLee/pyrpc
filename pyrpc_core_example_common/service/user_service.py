from abc import ABC, abstractmethod
from ..model.user import User


class UserService(ABC):

    @abstractmethod
    def get_user(self, id: int) -> User:
        pass

    def create_user(self, user: User) -> bool:
        pass

