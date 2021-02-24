import sys
sys.path.append('../../..')
import os
import socket

import conf
from mupif import Model
from mupif import pyroutil

#nameserver app name
appname='local'

class local(model.Model):
    """
    Mupif interface to Local dummy task

    """
    def __init__(self, file):
        super(local, self).__init__(file) #call basereturn
    def getApplicationSignature(self):
        return "local@"+ socket.gethostbyaddr(socket.gethostname())[0]+" version 1.0"

#create application
app = local(os.devnull)
# run the application server
appRecord = conf.apps['local']
pyroutil.runAppServer(server=appRecord.serverName,
                      port=appRecord.remotePort, 
                      nathost=conf.nathost, natport=appRecord.natPort, 
                      nshost=conf.nshost, nsport=conf.nsport, 
                      appName=pyroutil.getNSAppName(conf.jobname, appname), hkey=conf.hkey, app=app)




