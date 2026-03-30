from abc import ABC, abstractmethod


class CinemaEventConsumer(ABC):
    """
    Consumer for cinema events.
    Cinema provides the theaters and seats.
    Any changes or creations on cinemas entities (cinema, theater, seat) should be consumed by this consumer.
    """

    @abstractmethod
    def consume_create(self, event) -> None:
        pass

    @abstractmethod
    def consume_update(self, event) -> None:
        pass

    @abstractmethod
    def consume_delete(self, event) -> None:
        pass


class ShowtimeEventConsumer(ABC):
    """
    Consumer for showtime events.
    Showtime provides the showtimes and tickets.
    Any changes or creations on showtimes entities should be consumed by this consumer.
    """

    @abstractmethod
    def consume_create(self, event) -> None:
        pass

    @abstractmethod
    def consume_update(self, event) -> None:
        pass

    @abstractmethod
    def consume_delete(self, event) -> None:
        pass
