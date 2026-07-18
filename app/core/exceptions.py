from fastapi import HTTPException, status

class TravelConciergeException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class PaymentError(TravelConciergeException):
    pass

class BookingError(TravelConciergeException):
    pass

class AgentError(TravelConciergeException):
    pass
