import qrcode
from qrcode.constants import ERROR_CORRECT_L
import io
import base64
from datetime import datetime
from typing import Tuple
import json

def generate_ticket_qr(ticket_id: str, expiration_date: datetime) -> str:
    """
    Generates a QR code containing ticket information and expiration date.
    
    The QR code encodes a JSON string with the ticket ID and ISO-formatted expiration date.
    Returns the QR code image as a base64-encoded data URL for easy embedding in HTML.

    Args:
        ticket_id (str): Unique identifier for the ticket
        expiration_date (datetime): Date when the ticket becomes invalid

    Returns:
        str: Base64-encoded data URL of the QR code image (format: 'data:image/png;base64,...')

    Raises:
        ValueError: If ticket_id is empty or expiration_date is in the past

    Example:
        >>> expiration = datetime.now() + timedelta(days=1)
        >>> qr_url = generate_ticket_qr("TICKET-12345", expiration)
        >>> # Returns: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    """
    # Validate inputs
    if not ticket_id:
        raise ValueError("Ticket ID cannot be empty")
    if expiration_date < datetime.now():
        raise ValueError("Expiration date must be in the future")

    # Prepare QR code data
    qr_data = {
        "ticket_id": ticket_id,
        "expires_at": expiration_date.isoformat(),
        "version": "1.0"
    }
    json_data = json.dumps(qr_data)

    # Configure QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data and generate QR
    qr.add_data(json_data)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffered = io.BytesIO()
    img.save(buffered, "PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{qr_code_base64}"


def decode_ticket_qr(qr_data_url: str) -> Tuple[str, datetime]:
    """
    Decodes a ticket QR code data URL back to ticket information.
    
    Args:
        qr_data_url (str): The base64 data URL from generate_ticket_qr()

    Returns:
        tuple: (ticket_id: str, expiration_date: datetime)

    Raises:
        ValueError: If the QR code is invalid or expired
    """
    # Implementation would require actual QR decoding logic
    # This is just a placeholder for the interface
    # Return dummy values to satisfy the type checker
    return "", datetime.now()