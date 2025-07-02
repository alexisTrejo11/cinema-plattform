
class TicketSearchUseCase:
    """
    -Retrieves tickets based on dynamic filters.
    -Used by admins for manual monitoring  
    """
    def __init__(self) -> None:
        pass


class ListTicketsByUserIdUseCase:
    """
    -Retrieves tickets based on user id.
    -Used by admins or registred users that want to see their ticket history  
    """
    def __init__(self) -> None:
        pass
    
    
class ListTicketsByShowtimeIdUseCase:
    """
    -Retrieves tickets based on showtime.
    -One ticket will be retrived for each seat to show availability 
    """
    def __init__(self) -> None:
        pass
