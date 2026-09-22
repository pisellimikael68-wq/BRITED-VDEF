from abc import ABC, abstractmethod

from v2.core.context import BritedContext


class BaseChecker(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def check(self, context: BritedContext):
        ...
        