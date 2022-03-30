"""
email: eex_old.error.reporting@gmail.com
password: eex_old@1234
"""
import smtplib
from eex.conf.config import conf
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



class EmailReport():
    def __init__(self, report_name):
        self.report_name = report_name
        self.send_email()


    def send_email(self):

        subject = "Error Report"
        content = 'Please find attached the error report'

        msg = MIMEMultipart()
        msg['From'] = conf.from_addr
        msg['To'] = ', '.join(conf.to_addr)
        msg['Subject'] = subject
        body = MIMEText(content, 'plain')
        msg.attach(body)


        filename = self.report_name
        with open(filename, 'r') as f:
            part = MIMEApplication(f.read(), Name=basename(filename))
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
        msg.attach(part)

        server = smtplib.SMTP_SSL(conf.smtp_server, conf.smtp_server_port)
        server.login(conf.from_addr, conf.password)
        server.send_message(msg, from_addr=conf.from_addr, to_addrs=conf.to_addr)

        server.quit()





