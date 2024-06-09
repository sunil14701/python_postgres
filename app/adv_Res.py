import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time 

# Configuration
url = 'https://results.jeeadv.ac.in/jeeadv2024/247003117060820069878142960'  # Replace with your endpoint
# url = 'https://www.google.com/'  # Replace with your endpoint
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use 587 for TLS
smtp_user = 'linuscodes56@gmail.com'  # Replace with your Gmail address
smtp_password = 'aalglokelodnxrzu' # Replace with your Gmail app password
sender_email = 'linuscodes@gmail.com'  # Replace with your Gmail address
recipient_emails = ['sunilkumar333221@gmail.com', 'sanjaykumar77788@gmail.com','sahilkumar060806@gmail.com', 'sahilkumar064738']  # Replace with the recipient's email address
INTERVAL = 180
cnt = 0

def check_endpoint():
    try:
        response = requests.get(url)
        if not (400 <= response.status_code < 600):
            send_email(response)
            return 1 
    except requests.RequestException as e:
        print(f"Error contacting the endpoint: {e}") 
    global cnt
    print("working", cnt)   
    cnt = cnt +1

def send_email(response):
    try:
        for recipient_email in recipient_emails:
        # Create the email content
            subject = "JEE ADV res 2024"
            body = f"The endpoint responded with status code: {response.status_code}.\nPlease find the response content attached."

            msg = MIMEMultipart("alternative")
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Attach the plain text body
            part1 = MIMEText(body, 'plain')
            msg.attach(part1)

            # Attach the HTML response as the email body
            html_part = MIMEText(response.text, 'html')
            msg.attach(html_part)

            # Attach the HTML response as a file
            filename = 'response.html'
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(response.text.encode('utf-8'))
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(attachment)

            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print(f"Email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    while(1):
        ret = check_endpoint()
        if ret == 1:
            break
        time.sleep(INTERVAL)
        print("3 min passed")
