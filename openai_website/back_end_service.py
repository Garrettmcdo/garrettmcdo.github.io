from flask import Flask, request, redirect, render_template
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    project_type = request.form.get('type')
    details = request.form.get('details')
    user_email = request.form.get('email')

    message = EmailMessage()
    message['Subject'] = 'New Project Consultation Request'
    message['From'] = os.environ.get('EMAIL_SENDER')
    message['To'] = os.environ.get('EMAIL_RECEIVER')

    message.set_content(f"""
New consultation request received.

Project Type: {project_type}
From: {user_email}

Details:
{details}
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ.get('EMAIL_SENDER'), os.environ.get('EMAIL_PASSWORD'))
            smtp.send_message(message)
        return redirect('/thankyou.html')
    except Exception as e:
        return f\"Error sending email: {e}\", 500
