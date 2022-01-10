# Mechanical server for nonstationary problem
import os
import sys
import logging
import argparse
sys.path.extend(['..', '../..'])
from mupif import *
import models
log = logging.getLogger()
util.changeRootLogger('mechanical.log')

# locate nameserver
ns = pyroutil.connectNameServer()
mechanical = models.MechanicalModel()

pyroutil.runAppServer(
    ns=ns,
    appName='mechanical-ex08',
    app=mechanical
)
