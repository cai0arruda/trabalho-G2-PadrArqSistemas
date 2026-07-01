from abc import ABC, abstractmethod
from src.domain.events.domain_events import DomainEvent


class IMessageBroker(ABC):
    @abstractmethod
    def publish(self, queue: str, event: DomainEvent) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
