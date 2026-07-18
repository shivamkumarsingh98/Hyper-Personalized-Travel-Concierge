import razorpay
from app.core.config import settings
from app.core.exceptions import PaymentError

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(amount: float, currency: str = "INR") -> str:
    """
    Creates a Razorpay order.
    Amount in input is in INR, which is converted to paise.
    """
    try:
        # Amount in paise
        amount_in_paise = int(amount * 100)
        data = {
            "amount": amount_in_paise,
            "currency": currency,
            "payment_capture": 1
        }
        order = client.order.create(data=data)
        return order["id"]
    except Exception as e:
        raise PaymentError(f"Razorpay order creation failed: {str(e)}")

def verify_payment(razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> bool:
    """
    Verifies Razorpay payment signature.
    """
    try:
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)
        return True
    except Exception as e:
        raise PaymentError(f"Razorpay signature verification failed: {str(e)}")
