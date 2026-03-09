import os
from dotenv import load_dotenv # أضف هذا السطر
from email.message import EmailMessage
import smtplib

load_dotenv() # وأضف هذا السطر لتفعيل قراءة الملف

EMAIL_USER=os.getenv("EMAIL_USER")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
# SMTP Configuration
SMTP_SERVER=os.getenv("EMAIL_HOST", "smtp.gmail.com")
SMTP_PORT=int(os.getenv("EMAIL_PORT", "587"))
def send_email(Name,SENDER_EMAIL, Subject, Content):
    # 1. جلب وتنظيف البيانات بدقة
    user = os.getenv("EMAIL_USER").strip()
    password = os.getenv("EMAIL_PASSWORD").replace(" ", "").strip()
    host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    port = 587 # سنثبته على 587 للتجربة

    msg = EmailMessage()
    msg["Subject"] = Subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = os.getenv("PORTFOLIO_EMAIL")
    msg.set_content(Content)

    try:
        # 2. إنشاء الاتصال
        server = smtplib.SMTP(host, port, timeout=20) # أضفنا مهلة زمنية 20 ثانية
        server.set_debuglevel(1) # هذا السطر سيطبع تفاصيل الاتصال في التيرمينال لنعرف أين يتوقف بالضبط
        
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        server.login(user, password)
        server.send_message(msg)
        server.quit()

        print("تم إرسال البريد الإلكتروني بنجاح!")
        return True

    except Exception as e:
        print(f"فشل الإرسال بسبب: {e}")
        return None
# لا تطبع كلمة المرور أبداً، فقط تأكد أن المتغير ليس None
print(f"Password length: {(EMAIL_PASSWORD)}")