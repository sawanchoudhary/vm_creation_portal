__author__ = "Sawan Choudhary"
__copyright__ = "Copyright 2017, CalsoftInc"
__maintainer__ = "Calsoft IT"

#------------------------------------------------------------------------------------------------------------
import subprocess

print("Start removing key from known_hosts")
with open('/home/eng/vmcreationportal/WebPortal/VM_files/CSV/hosts1') as f:
    content = f.readline()

content = content.strip()
new_ip = content.split(" ")

subprocess.call(['ssh-keygen', '-f', '/home/eng/.ssh/known_hosts', '-R', new_ip[0]])
print("Finished removing key from known_hosts")

#--------------------------------------------------------------------------------------

print "Start to clear hosts1 file"
f = open('/home/eng/vmcreationportal/WebPortal/VM_files/CSV/hosts1','w')
f.write('')
f.close()
print "Finished clearing hosts1 file"

#----------------------------------------------------------------------------------------

print "Start to write to busy.txt to start taking new request"
f = open('/home/eng/vmcreationportal/WebPortal/VM_files/CSV/busy.txt','w')
f.write('0')
f.close()
print "Finished writing to busy.txt to start taking new request"
	
print "Task finished"
print "----------------------------------------------------------------------------------"

