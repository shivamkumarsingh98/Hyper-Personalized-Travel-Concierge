from fastapi import APIRouter
from app.services.amadeus import AmadeusService

router = APIRouter()
router_prefix = "/vendors"

@router.get("/flights/search")
def search_flights(origin: str, destination: str, date: str):
    return AmadeusService.search_flights(origin, destination, date)

@router.get("/hotels/search")
def search_hotels(location: str, checkin: str, checkout: str):
    return AmadeusService.search_hotels(location, checkin, checkout)
