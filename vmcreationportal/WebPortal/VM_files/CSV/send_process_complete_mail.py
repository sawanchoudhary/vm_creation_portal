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

def send_email():

    print "Start to send process completion mail"
    # Python date and time library is used to get the date and time to be placed on the subject line.

    now = datetime.datetime.now()

    # Sender and receiver mail address with the subject line containing date and time.
    # Open hosts1 file to get new VM IP

    print "Open hosts1 file to read new IP"
    f = open("/home/eng/vmcreationportal/WebPortal/VM_files/CSV/hosts1")
    vm_ip = f.readline()
    vm_ip1 = vm_ip.split(' ')
    f.close()
    print "Closed hosts1 file, successful reading new IP"


    fromaddr = "monitor@calsoftinc.com"
    toaddr = gen_info[1]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "VM Creation Portal - [ Successfully Created VM - " + gen_info[5] + "]"

    # Initialization of the body of html part.

    body = """Congratulations """+ gen_info[0]+""",<br><br>Your VM has been successfully created and all selected packages have been installed successfully.<br><br>Please find it's details below:"""


    body = body +  """
    <html>
            <head></head>
            <body>
                <br><br>
                <table style="border: 1px solid black;">
                    <tr><td style="border: 1px solid black;"><b>ESXi IP</b></td><td style="border: 1px solid black;">172.17.75.51</td></tr>
                    <tr><td style="border: 1px solid black;"><b>VM IP</b></td><td style="border: 1px solid black;">"""+vm_ip1[0]+"""</td></tr>
                    <tr><td style="border: 1px solid black;"><b>VM Name</b></td><td style="border: 1px solid black;">"""+gen_info[5]+"""</td></tr>
                    <tr><td style="border: 1px solid black;"><b>User Name</b></td><td style="border: 1px solid black;">ituser</td></tr>
                    <tr><td style="border: 1px solid black;"><b>Password</b></td><td style="border: 1px solid black;">Calsoft@123</td></tr>
                </table>
                <br><br>
                <i>- Regards,<br>Calsoft IT Team.</i>
            </body>
    </html>  """



   # The body is attached to the html part.

    msg.attach(MIMEText(body, 'html'))

    # Calsoft server, port, sender and receiver details.
    # Start and end of session with the Calsoft server by startls() and quit.

    server = smtplib.SMTP('csom2.calsoft.org', 587)
    server.starttls()
    server.login(fromaddr, "monitor")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    print "Finished sending process completion mail"

def main():
    send_email()

# Start program
if __name__ == "__main__":
   main()
