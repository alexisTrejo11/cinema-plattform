import qrcode
from qrcode.constants import ERROR_CORRECT_L
import io
import base64
from urllib.parse import quote

def generate_QR(otp_uri: str):
    """
    Generate QR for 2FA.

    Args:
        otp_uri (str):

    Returns:
        str: (qr_code_base64_image_data) -> qr_code_base64_image_data es la imagen QR en formato base64 para mostrar en el frontend.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(otp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = io.BytesIO()
    img.save(buffered)
    qr_code_base64_data = base64.b64encode(buffered.getvalue()).decode("utf-8")


    return f"data:image/png;base64,{qr_code_base64_data}"
