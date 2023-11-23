import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from templates import Template
from dotenv import load_dotenv


load_dotenv()

username =  os.environ.get('USERNAME_EMAIL')
password =  os.environ.get('PASSWORD_EMAIL')


print('username', username)
print('password', password)

class Emailer():
    to_emails = []
    subject = ''
    has_html = False
    test_send = False
    from_email = "flashio@patraz.online"
    template_html = None
    template_name = None
    context = {}

    def __init__(self, subject='', template_name= None, context = {}, template_html=None, to_emails=None, test_send = False):
        if template_name == None and template_html == None:
            raise Exception("You have to put template")
        assert isinstance(to_emails, list)

        self.to_emails = to_emails
        self.subject = subject
        if template_html != None:
            self.has_html = True
            self.template_html = template_html
            
        self.template_name = template_name
        self.test_send = test_send
        self.context = context

    def format_msg(self):
        
        msg = MIMEMultipart('alternative')
        msg['From'] = self.from_email
        msg['To'] = ', '.join(self.to_emails)
        msg['Subject'] = self.subject

        if self.template_name != None:
            tmpl_str = Template(template_name=self.template_name, context = self.context)
            txt_part = MIMEText(tmpl_str.render(), 'plain')
            msg.attach(txt_part)
            print(txt_part)
        if self.template_html != None:
            tmpl_html = Template(template_name=self.template_html, context = self.context)
            html_part = MIMEText(tmpl_html.render(), 'html')
            msg.attach(html_part)
            print(html_part)
        msg_str = msg.as_string()
        return msg_str

    def send(self):
        msg = self.format_msg()
        did_send = False
        if not self.test_send:
            with smtplib.SMTP(host='in-v3.mailjet.com', port=587) as server:
                server.ehlo()
                server.starttls()
                server.login(username, password)
                try:
                    server.sendmail(self.from_email, self.to_emails, msg)
                    did_send=True
                except:
                    did_send = False
                return did_send





