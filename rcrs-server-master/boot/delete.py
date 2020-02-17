import subprocess
import os
import socket
import sys
import htcondor
import classad

coll = htcondor.Collector()

ad = coll.locate(htcondor.DaemonTypes.Schedd, "submit-1.chtc.wisc.edu")
ad["MyAddress"]