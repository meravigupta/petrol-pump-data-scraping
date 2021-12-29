import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from email.header import Header
from datetime import date
sender_address = ""
sender_password = ""
receivers = ["",""]
length = len(receivers)
to_day = date.today()
today = to_day.strftime("%Y-%m-%d")
attach_file_name = ["path/petrolpump_chayan/example"+ today +".xlsx"]
# for i in range(length): 
    
#     X = receivers[i]
#     reciver_mail = X

def send_mail(receiver_address,mail_content, subject, attach_file_name=[]):
    message = MIMEMultipart()
    message["From"] = sender_address
    #message["To"] = Header(receiver_address, "utf-8")
    message["Subject"] = subject
    message.attach(MIMEText(mail_content,'plain'))
    lengths = len(attach_file_name)
    for i in range(lengths):
        x = attach_file_name[i]
        attach_file = x
        if attach_file!='':
            with open(attach_file, 'rb') as fil:
                part = MIMEApplication(fil.read(),Name=basename(attach_file))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attach_file)
            message.attach(part)
        '''payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) 
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file)
        message.attach(payload)'''
        
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_address,sender_password)
        text = message.as_string()
        session.sendmail(sender_address,receiver_address,text)
        print("Mail Sent")
    
send_mail(receivers,"testing mail from function","test mail")