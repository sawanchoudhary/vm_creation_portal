__author__ = "Sawan Choudhary"
__copyright__ = "Copyright 2017, CalsoftInc"
__maintainer__ = "Calsoft IT"

#------------------------------------------------------------------------------------------------------------

import csv
from change_vm_name import replace
from store_last_vm_name import last_vm_name

print "---------------------------------------------------------------------------------------------------------------"

# Read new csv file name from new_info.txt

f = open("/home/eng/vmcreationportal/WebPortal/VM_files/CSV/new_vm_info.txt")
file_name = f.readline().strip()
print " Started VM Creation Process for" + " " + str(file_name)
print "Read new CSV file name successfully"
f.close()
#-------------------------------------------------------------------------------------

# Read new CSV file to get the user data.

file_name_path = "/home/eng/vmcreationportal/WebPortal/VM_files/CSV/"+file_name

with open(file_name_path,'rb') as f:
    reader = csv.reader(f)
    row1 = next(reader)
    row2 = next(f)
l = row2.split(',')
gen_info = []
vm_info = []
pckg_info = []

for i in range(0,8):
    gen_info.append(l[i])


for i in range(8,11):
    vm_info.append(l[i])

if len(l)==12:
    x = l[11][3:-3]
    pckg_info.append(x)

else:    
    for i in range(11,len(l)):
        if i == 11:
            x = l[i][3:-1]
            pckg_info.append(x)
    
        elif i == len(l)-1:
            x = l[i][1:-3]
            pckg_info.append(x)
        else:
            x = l[i][1:-1]
            pckg_info.append(x)


# Write the csv data to dict_from_csv.py file so that ansible reads it.
print "Started writing dict_from_csv.py"

f = open('/home/eng/vmcreationportal/WebPortal/VM_files/CSV/dict_from_csv.py','w')
f.write('gen_info: [')
for i in range(0,len(gen_info)):
    if i!=len(gen_info)-1:
        f.write(gen_info[i]+",")
    else:
        f.write(gen_info[i])

f.write(']')
f.write('\n')
f.write('vm_info: [')
for i in range(0,len(vm_info)):
    if i!=len(vm_info)-1:
        f.write(vm_info[i]+",")
    else:
        f.write(vm_info[i])

f.write(']')

f.write('\n')
f.write('pckg_info: [')
for i in range(0,len(pckg_info)):
    if i!=len(pckg_info)-1:
        f.write(pckg_info[i]+",")
    else:
        f.write(pckg_info[i])

f.write(']')

f.close()
print "Fininshed writing dict_from_csv.py"
#-------------------------------------------------------------------------------------------
# Write the csv data to dict_from_csv_py.py file so that python file reads it.

print "Started writing dict_from_csv_py.py"
f = open('/home/eng/vmcreationportal/WebPortal/VM_files/CSV/dict_from_csv_py.py','w')
f.write('gen_info= [')
for i in range(0,len(gen_info)):
    if i!=len(gen_info)-1:
        f.write(gen_info[i]+",")
    else:
        f.write(gen_info[i])

f.write(']')
f.write('\n')
f.write('vm_info= [')
for i in range(0,len(vm_info)):
    if i!=len(vm_info)-1:
        f.write(vm_info[i]+",")
    else:
        f.write(vm_info[i])

f.write(']')

f.write('\n')
f.write('pckg_info= [')
for i in range(0,len(pckg_info)):
    if i!=len(pckg_info)-1:
        f.write(pckg_info[i]+",")
    else:
        f.write(pckg_info[i])

f.write(']')

f.close()


print "Finished writing dict_from_csv_py.py"
#------------------------------------------------------------------------------------------
# Change VM name from OVF file.

print "Started changing VM Name into OVF"
file_path = "/home/eng/vmcreationportal/WebPortal/VM_files/CSV/VM_Creation_Portal_Template.ovf"
pattern = last_vm_name
file_name1 = file_name.split('.')
replace(file_path, pattern, file_name1[0])

print "Finished changing VM Name into OVF"

#-------------------------------------------------------------------------------------------
# Writing current VM Name into store_last_vm_name.py.

print "Started writing current VM Name into store_last_vm_name.py"

f = open('/home/eng/vmcreationportal/WebPortal/VM_files/CSV/store_last_vm_name.py','w')
f.write('last_vm_name = "')
f.write(file_name1[0])
f.write('"')
f.close()
print "Finished writing current VM Name into store_last_vm_name.py"

#------------------------------------------------------------------------------------------
    
    

