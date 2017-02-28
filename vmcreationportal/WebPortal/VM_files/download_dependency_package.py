__author__ = "Sawan Choudhary"
__copyright__ = "Copyright 2017, CalsoftInc"
__maintainer__ = "Calsoft IT"

#------------------------------------------------------------------------------------------------------------
# First create a file <pckg-name>.txt 
# Run below command to get dependency list.
# apt-cache policy $(debfoster -q --option UseRecommends=no -d <pckg-name>|tail -n +2) |awk '/^[^ ]/ { package=$0 } /  Installed/ { print package " " $2 }'><pckg-name>.txt
# Then run below script to download all the deb files.
# Make a new directory for each package.
# Then install all the packages by sudo dpkg -i *.deb from within the directory or sudo dpkg -i -R <directory-name> from outside the directory.

import subprocess
fname='<pck-name>.txt'
with open(fname) as f:
    content = f.readlines()
pckg_with_version= []
pckg=[]
fname1=fname.split('.')
pckg.append(fname1[0])
content = [x.strip() for x in content]
for i in content:
    pckg_with_version=i.split(': ')
    pckg.append(pckg_with_version[0])
for i in pckg:
    subprocess.call(['sudo', 'apt-get', 'download', i])
