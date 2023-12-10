import qrcode

otp_url = "otpauth://totp/google:vishal?secret=EWLRLPNJRANDIHDTNP3TNM3MMV2WV2J2&issuer=google"

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add the data to the QR code
qr.add_data(otp_url)
qr.make(fit=True)

# Create an image from the QR code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save or display the image as needed
img.save("otp_qr_code.png")
