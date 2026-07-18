from typing import Any, Dict, List

class AmadeusService:
    @staticmethod
    def search_flights(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        return [
            {
                "airline": "British Airways",
                "flight_number": "BA123",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{date}T08:00:00",
                "arrival_time": f"{date}T11:30:00",
                "price": 450.00,
                "stops": 0,
                "class": "Economy"
            },
            {
                "airline": "Air India",
                "flight_number": "AI456",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{date}T14:15:00",
                "arrival_time": f"{date}T18:00:00",
                "price": 510.00,
                "stops": 0,
                "class": "Economy"
            }
        ]

    @staticmethod
    def search_hotels(location: str, checkin: str, checkout: str) -> List[Dict[str, Any]]:
        return [
            {
                "hotel_name": "London Marriott Hotel County Hall",
                "location": location,
                "checkin": checkin,
                "checkout": checkout,
                "price_per_night": 250.00,
                "total_price": 750.00,
                "stars": 5,
                "amenities": ["Free WiFi", "Pool", "Gym"]
            },
            {
                "hotel_name": "Sheraton Grand Park Lane",
                "location": location,
                "checkin": checkin,
                "checkout": checkout,
                "price_per_night": 200.00,
                "total_price": 600.00,
                "stars": 5,
                "amenities": ["Spa", "Bar", "Free WiFi"]
            }
        ]
