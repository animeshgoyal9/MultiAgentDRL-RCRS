#! /bin/bash

. functions.sh

processArgs $*

# To create different log directories
echo $LOGDIR
LOGDIR="$LOGDIR-$HOSTNAME"

# Delete old logs
rm -f $LOGDIR/*.log

#startGIS
startKernel --nomenu --autorun 
startSims 

echo "Start your agents"
waitFor $LOGDIR/kernel.log "Kernel has shut down" 30

kill $PIDS
