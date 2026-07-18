import pytest
from unittest.mock import patch
from app.services.payment import create_order, verify_payment
from app.core.exceptions import PaymentError

def test_create_order_success():
    mock_order = {"id": "order_mock123"}
    with patch("app.services.payment.client") as mock_client:
        mock_client.order.create.return_value = mock_order
        order_id = create_order(1500.0, "INR")
        
        assert order_id == "order_mock123"
        mock_client.order.create.assert_called_once_with(data={
            "amount": 150000,
            "currency": "INR",
            "payment_capture": 1
        })

def test_create_order_failure():
    with patch("app.services.payment.client") as mock_client:
        mock_client.order.create.side_effect = Exception("API error")
        with pytest.raises(PaymentError):
            create_order(1500.0, "INR")

def test_verify_payment_success():
    with patch("app.services.payment.client") as mock_client:
        mock_client.utility.verify_payment_signature.return_value = True
        result = verify_payment("order_123", "pay_123", "sig_123")
        assert result is True
        mock_client.utility.verify_payment_signature.assert_called_once_with({
            'razorpay_order_id': 'order_123',
            'razorpay_payment_id': 'pay_123',
            'razorpay_signature': 'sig_123'
        })

def test_verify_payment_failure():
    with patch("app.services.payment.client") as mock_client:
        mock_client.utility.verify_payment_signature.side_effect = Exception("Invalid signature")
        with pytest.raises(PaymentError):
            verify_payment("order_123", "pay_123", "sig_123")
