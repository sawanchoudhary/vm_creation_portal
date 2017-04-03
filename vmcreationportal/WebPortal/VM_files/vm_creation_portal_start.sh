#!/bin/sh
#

# author = "Sawan Choudhary"
# copyright = "Copyright 2017, CalsoftInc"
# maintainer = "Calsoft IT"

python /home/eng/vmcreationportal/WebPortal/VM_files/CSV/create_dict_from_csv.py

python /home/eng/vmcreationportal/WebPortal/VM_files/CSV/createvm.py -s 172.17.xx.xx -u root -p xxxxxxxxxxx -v /home/eng/vmcreationportal/WebPortal/VM_files/CSV/VM_Creation_Portal_Template-disk1.vmdk -f /home/eng/vmcreationportal/WebPortal/VM_files/CSV/VM_Creation_Portal_Template.ovf

if [ $? = 0 ]; then

    ansible-playbook -i /home/eng/vmcreationportal/WebPortal/VM_files/CSV/hosts /home/eng/vmcreationportal/WebPortal/VM_files/CSV/main_change_vm_config.yml

    ansible-playbook -i /home/eng/vmcreationportal/WebPortal/VM_files/CSV/hosts /home/eng/vmcreationportal/WebPortal/VM_files/CSV/main_power_on_vm.yml

    python /home/eng/vmcreationportal/WebPortal/VM_files/CSV/parse_new_vm_ip1.py -s 172.17.xx.xx -u xxxx -p xxxxxxxxxx

    python /home/eng/vmcreationportal/WebPortal/VM_files/CSV/demo_ssh.py

    if [ $? = 0 ]; then

        ansible-playbook -i /home/eng/vmcreationportal/WebPortal/VM_files/CSV/hosts1 /home/eng/vmcreationportal/WebPortal/VM_files/CSV/main_install_pck.yml

        python /home/eng/vmcreationportal/WebPortal/VM_files/CSV/send_process_complete_mail.py

        python /home/eng/vmcreationportal/WebPortal/VM_files/CSV/finish_task.py

    else
        echo "Failure,to SSH to new VM"
    fi


else
    echo "Failure, could not create VM"
fi


