#!/bin/sh -e
#
# Put this script in /path/to/project/local/upgrade.sh
# and customize if necessary
 
cd $(dirname "$0")/..
 
echo $(date): invoked with args: $* | tee -a $0.log
