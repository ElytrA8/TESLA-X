#!/bin/bash

expect -c " 
spawn sftp $sfuser@frs.sourceforge.net
expect \"yes/no\"
send \"yes\r\"
expect \"Password\"        
send \"$sfpass\r\"
expect \"sftp> \"
send \"cd $sfdir\r\"
set timeout -1
send \"put $file_dir\r\"
expect \"Uploading\"
expect \"100%\"
expect \"sftp>\"
interact"

rm -rf .ssh/known_hosts
