__author__ = "Sawan Choudhary"
__copyright__ = "Copyright 2017, CalsoftInc"
__maintainer__ = "Calsoft IT"

#------------------------------------------------------------------------------------------------------------

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime
from dict_from_csv_py import gen_info
# Function to send mail with vm and its authentication details

def send_error_mail_fn(error):


    # Python date and time library is used to get the date and time to be placed on the subject line.

    now = datetime.datetime.now()

    # Sender and receiver mail address with the subject line containing date and time.


    fromaddr = "monitor@calsoftinc.com"
    toaddr = gen_info[1]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "VM Creation Portal - [ Creating VM Failed ]"

    # Initialization of the body of html part.

    body = """Sorry """+ gen_info[0]+""",<br><br>VM Creation Failed."""


    body = body +  """<br>VM could not be created: """
    body = body + str(error)
    body = body + """<br><br>Kindly wait, we are working to fix the issue and resume service."""
    body = body + """<br><br><br><br><br><br><br><i>- Regards,<br>Calsoft IT Team.</i>"""

    # The body is attached to the html part.

    msg.attach(MIMEText(body, 'html'))

    # Calsoft server, port, sender and receiver details.
    # Start and end of session with the Calsoft server by startls() and quit.

    server = smtplib.SMTP('csom2.calsoft.org', 587)
    server.starttls()
    server.login(fromaddr, "xxxxxx")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
