from typing import Any, Dict

class ContentstackService:
    @staticmethod
    def get_personalized_content(loyalty_tier: str, destination: str) -> Dict[str, Any]:
        offers = {
            "VIP": {
                "banner_title": "Welcome to your Premium London Getaway",
                "offer_description": "Enjoy complimentary access to the Marriott executive lounge and free airport pick-up.",
                "promo_code": "VIPLDN26",
                "badge": "Elite Member Benefit"
            },
            "Standard": {
                "banner_title": "Explore London on Your Terms",
                "offer_description": "Get 10% off your next booking at Marriott locations.",
                "promo_code": "LDN10",
                "badge": "Special Offer"
            }
        }
        return offers.get(loyalty_tier, offers["Standard"])
