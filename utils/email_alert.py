import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

GMAIL_USER = os.getenv('EMAIL') 
GMAIL_PASS = os.getenv('PASSWORD') 

def send_budget_alert_email(to_email: str, category: str, remaining: float):
    try:
        print(to_email, category, remaining,GMAIL_PASS,GMAIL_USER)
        subject = f'⚠️ Budget Alert for {category}'
        html_content = f"""
        <html>
            <body>
                <h3>Heads up!</h3>
                <p>You have only ₹{remaining:.2f} left in your <strong>{category}</strong> budget for this month.</p>
                <p>Consider reviewing your expenses to stay on track.</p>
            </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())

        print('✅ Budget alert email sent.')

    except Exception as e:
        print(f'❌ Failed to send email: {e}')
