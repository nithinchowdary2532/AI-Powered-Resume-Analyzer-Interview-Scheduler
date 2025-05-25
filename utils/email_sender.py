import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email, from_email, password):
    """
    Sends a properly formatted email using Gmail SMTP server
    
    Args:
        subject (str): Email subject
        body (str): Formatted email body content
        to_email (str): Recipient email address
        from_email (str): Sender email address (Gmail)
        password (str): Sender email password or app password
        
    Returns:
        str: Success or error message
    """
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the formatted body to the email
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        
        # Login to Gmail account
        server.login(from_email, password)
        
        # Send email
        server.send_message(msg)
        
        # Terminate the session
        server.quit()

        return "📧 Email sent successfully!"
    
    except smtplib.SMTPAuthenticationError:
        return "⚠️ Authentication failed. Please check your email and password."
    
    except smtplib.SMTPException as e:
        return f"⚠️ SMTP error occurred: {str(e)}"
    
    except Exception as e:
        return f"⚠️ Error sending email: {str(e)}"