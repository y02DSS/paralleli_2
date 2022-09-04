import sqlite3
import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import formataddr
from email.message import EmailMessage
from urllib.parse import quote


def all1(mailr, wordr):
    data = 'АА'
    smtp_addr = 'smtp.mail.ru', 25
    fromaddr = "zakupki2.0@mail.ru"
    toaddr = str(mailr)
    password = "DSS2002DSS"
    subject = "Здравствуйте!"
    sender = "Сайт Калининградского ПЕН-центра"
    text = f'Ваше произведение {wordr}. При возникновении вопросов, ответьте на это сообщение'


    def send_mail(smtp_addr,
                  fromaddr,
                  password,
                  toaddr,
                  sender=None,
                  subject=None,
                  text=None,
                  data=None,
                  ):

        from_addr = formataddr((sender, fromaddr))
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = toaddr
        msg['Subject'] = subject or ''

        if text:
            msg.attach(MIMEText(*text))

        if data:
            attachment = MIMEBase('application', "octet-stream")
            attachment.set_payload(data)
            encoders.encode_base64(attachment)
            #attachment.add_header('Content-Disposition', 'attachment', filename=("output.xlsx"))
            #msg.attach(attachment)

            server = smtplib.SMTP(*smtp_addr)
            server.starttls()
            server.login(fromaddr, password)
        # mail = msg.as_string()

        try:
            server.send_message(msg)
        # except (smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused) as err:
        #   sys.stderr.write("Проблема с отправкой письма. Причина: %s" % err)
        # finally:
        #    server.quit()
        except:
            server.quit()

    send_mail(smtp_addr,
              fromaddr,
              password,
              toaddr,
              sender=sender,
              subject=subject,
              text=(text, 'plain', '1251'),
              data=data)




