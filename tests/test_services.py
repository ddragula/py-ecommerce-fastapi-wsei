import pytest
from api.services import get_password_hash, verify_password, create_access_token, order_to_xml
from datetime import timedelta
from unittest.mock import MagicMock

# Password hashing tests
def test_get_password_hash():
    password = "supersecret"
    hashed_password = get_password_hash(password)
    assert password != hashed_password
    assert len(hashed_password) > len(password)

# Password verification tests
def test_verify_password():
    password = "supersecret"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

# JWT token creation test
def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    assert isinstance(token, str)
    assert "." in token

# Order to XML conversion test
def test_order_to_xml():
    mock_order = MagicMock()
    mock_order.id = 1
    mock_order.created_at.isoformat.return_value = "2024-01-01T12:00:00"
    
    mock_product = MagicMock()
    mock_product.id = 101
    mock_product.name = "Test Product"
    
    mock_item = MagicMock()
    mock_item.product = mock_product
    mock_item.price = 10.0
    mock_item.quantity = 2

    mock_order.items = [mock_item]

    xml_output = order_to_xml(mock_order)
    
    assert "<order id=\"1\"" in xml_output
    assert "<name>Test Product</name>" in xml_output
    assert "<quantity>2</quantity>" in xml_output

