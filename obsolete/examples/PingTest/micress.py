import sys
sys.path.append('../../..')
import os
import socket

from mupif import Model
from mupif import pyroutil

# import basic definitions -> need to be customized
import conf
#set application name (used also as an index to apps dictionary defined in conf.py)
appname='micress'

class micress(model.Model):
    """
    Mupif interface to micress (microstructure evolution simulation tool) 

    """
    def __init__(self, file):
        super(micress, self).__init__(file) #call base
        return
    def getApplicationSignature(self):
        return "Micress@"+ socket.gethostbyaddr(socket.gethostname())[0]+" version 1.0"



#create application
app = micress(os.devnull)
# run the application server
appRecord = conf.apps['micress']
pyroutil.runAppServer(server=appRecord.serverName, port=appRecord.remotePort, 
                      nathost=conf.nathost, natport=appRecord.natPort, 
                      nshost=conf.nshost, nsport=conf.nsport, 
                      appName=pyroutil.getNSAppName(conf.jobname, appname), hkey=conf.hkey, app=app)
