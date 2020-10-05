import random
import base64
from datetime import datetime

from email.mime.text import MIMEText
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from registration.models import User
from booking.models import Booking
from proclamation.models import Proclamation

strAccount = "cga.easter.branch@gmail.com"      # 備援信箱：tryitnotareal1997@gmail.com
strPassword = "Cga00000"


def booking_notification_mail(proprietor: User, booking: Booking):
    # strSmtp = "smtp.gmail.com:587"
    # 主機

    # encode the verified email
    email = proprietor.email
    email_bytes = email.encode('ascii')
    base64_bytes = base64.b64encode(email_bytes)
    base64_email = base64_bytes.decode('ascii')

    content = "Dear " + proprietor.username + ":\n" + \
              "Your " + booking.booked_room.hotel.name + " - " + booking.booked_room.name + "had been booked.\n" + \
              "Date : " + booking.check_in_time.strftime("%Y/%m/%d, %H:%M") + " to " + booking.check_out_time.strftime("%Y/%m/%d, %H:%M") + "\n" + \
              "Applicant Unit : " + booking.unit_of_applicant + "\n" + \
              "Applicant : " + booking.applicant.get_full_name() + "\n" + \
              "Please check out your booking index.\n\n" + \
              "Thanks for your watching." + "\n" + \
              "By DW, Su, " + datetime.now().strftime("%Y/%m/%d, %H:%M")

    msg = MIMEText(content)
    # 郵件標題
    msg["Subject"] = "Booking"
    mail_to = proprietor.email

    server = SMTP("smtp.gmail.com:587")
    # server = SMTP(strSmtp)
    # 建立連線
    server.ehlo()
    # 跟主機溝通
    server.starttls()
    # TTLS安全驗證

    try:
        server.login(strAccount, strPassword)
        server.sendmail(strAccount, mail_to, msg.as_string())
        hint = "郵件已發送"
    except SMTPAuthenticationError:
        hint = "無法登入"
    except:
        hint = "郵件發送產生錯誤"
    server.quit()
    # 關閉連線
