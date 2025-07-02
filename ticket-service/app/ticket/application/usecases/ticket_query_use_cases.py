class CreateTicketsForShowtimesUseCase:
    def __init__(self) -> None:
        """ 
        - Init n number of tickets for an incoming showtime.
        - The number of tickets is based on theater seats. One ticket is created for each seat.
        - Tickets are mark as not sell it until somebody buys it or after expiration time occurs. 
        """
        pass
    
    
class BuyTicketUseCase:
    def __init__(self) -> None:
        """
        - Buys a Ticket. 
        - Could by a register customer of for anonimus customer.
        - Customers can buy tickets in 2 ways:
            -Physical buy: Sell it in ticket office for each cinema
            -Digital: buy: Sell it on web page an users can buy tickets in any selected cinema 
        """
        pass


class UseTicketUseCase:
    def __init__(self) -> None:
        pass
    
    
class CancelTicketCase:
    def __init__(self) -> None:
        pass