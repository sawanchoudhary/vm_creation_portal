__author__ = "Sawan Choudhary"
__copyright__ = "Copyright 2017, CalsoftInc"
__maintainer__ = "Calsoft IT"

#------------------------------------------------------------------------------------------------------------

from pexpect import pxssh
import getpass
from send_error_mail import send_error_mail_fn


print "Starting demo SSH"
f = open("/home/eng/vmcreationportal/WebPortal/VM_files/CSV/hosts1")
file_name = f.readline().strip()
file_name1 = file_name.split(" ")
f.close()
#print file_name1[0]
try:                                                            
    s = pxssh.pxssh()
    #hostname = raw_input('hostname: ')
    hostname = file_name1[0]
    username = 'xxxx'
    password = 'xxxxxxxx'
    #password = getpass.getpass('password: ')
    s.login (hostname, username, password)
    s.sendline ('uptime')   # run a command
    s.prompt()             # match the prompt
    #print s.before          # print everything before the prompt.
    s.sendline ('ls -l')
    s.prompt()
    #print s.before
    s.sendline ('df')
    s.prompt()
    #print s.before
    s.logout()
    print "Finished demo SSH"
except pxssh.ExceptionPxssh, e:
    print "pxssh failed on login."
    print str(e)
    error_ssh = "pxssh failed to login" + " " + str(e)
    send_error_mail_fn(error_ssh)
    raise SystemError("Error may be due already existing key of same IP")
  
