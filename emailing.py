import smtplib
from email.message import EmailMessage
import mimetypes

password = 'miyi ljdx gykd hmbq '

def send_email(picture):
    email_message = EmailMessage()
    email_message["Subject"] = "The program detected some movement!"
    email_message["From"] = "adamidrissi177@gmail.com"
    email_message["To"] = "30443@ras.ma"
    email_message.set_content("Please check the image below.")

    # Read and attach the image
    with open(picture, 'rb') as file:
        content = file.read()

    # Guess the image type (e.g., 'image/png' or 'image/jpeg')
    mime_type, _ = mimetypes.guess_type(picture)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # fallback

    maintype, subtype = mime_type.split('/')
    email_message.add_attachment(content, maintype=maintype, subtype=subtype, filename=picture)

    # Send the email
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login('adamidrissi177@gmail.com', password)
    gmail.send_message(email_message)
    gmail.quit()