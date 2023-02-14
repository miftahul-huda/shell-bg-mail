import sys, getopt
import argparse

import smtplib, ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import base64


from dotenv import load_dotenv
import os

def main():

   load_dotenv()

   parser = argparse.ArgumentParser(
                    prog = 'Py Mailer',
                    description = 'Send email using mailer API',
                    epilog = 'Devoteam')

   parser.add_argument('-t', '--to', help='Email address where the email is sent to. Multiple addresses are separated by ,')  
   parser.add_argument('-s', '--subject', help='The email subject')
   parser.add_argument('-b', '--body', help='The email body')
   parser.add_argument('-a', '--attachments', help='File(s) to attach. Separate multiple files by ,')

   args = parser.parse_args()
   attachments = args.attachments
   if(attachments != None):
      attachments = attachments.split(",")
   #print(attachments)
   sendmail(None, args.to, args.subject, args.body, attachments)


def sendmail(sfrom, to, subject, body, attachments):
   sender_email = sfrom
   receiver_email = to

   body2 = body.replace("\n", "<br>")
   #print(body)

   if(sender_email is None):
      sender_email = os.environ["smtp_user"]
   password = os.environ["smtp_password"]
   password = base64.b64decode(password).decode('utf-8')

   #print(password)

   message = MIMEMultipart("alternative")
   message["Subject"] = subject
   message["From"] = sender_email
   message["To"] = receiver_email

   # Create the plain-text and HTML version of your message
   
   html = """\
   <html>
   <head></head>
   <body>
   """ + body2 + """
   </body>
   </html>
   """

   # Turn these into plain/html MIMEText objects
   text = MIMEText(body, "plain")
   html = MIMEText(html, "html")

   # Add HTML/plain-text parts to MIMEMultipart message
   # The email client will try to render the last part first
   message.attach(text)
   message.attach(html)


   if(attachments != None):
      for path in attachments:
         #print("Attach " + path)
         part = MIMEBase('application', "octet-stream")
         with open(path, 'rb') as file:
            part.set_payload(file.read())
         encoders.encode_base64(part)
         part.add_header('Content-Disposition',
                           'attachment; filename={}'.format(Path(path).name))
         message.attach(part)

   # Create secure connection with server and send email
   context = ssl.create_default_context()
   try:
      with smtplib.SMTP_SSL(os.environ["smtp_server"], os.environ["smtp_port"], context=context) as server:
         server.login(sender_email, password)
         server.sendmail(
            sender_email, receiver_email.split(","), message.as_string()
         )
         print ("---SMTP_SSL-mail.py Email sent")
   except:   
      with smtplib.SMTP(os.environ["smtp_server"], os.environ["smtp_port"]) as server:
         server.starttls(context=context)
         server.login(sender_email, password)
         server.sendmail(
            sender_email, receiver_email.split(","), message.as_string()
         )
         print ("---SMTP-mail.py Email sent")

   


if __name__ == "__main__":
   main()



