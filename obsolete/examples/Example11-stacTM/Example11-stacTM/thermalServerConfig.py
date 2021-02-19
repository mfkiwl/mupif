#Configuration file for JobMan2cmd
import os,sys
sys.path.extend(['..','../Example10'])
import conf_vpn as cfg

import demoapp
applicationClass = demoapp.thermal
applicationInitialFile = '..'+os.path.sep+'..'+os.path.sep+'Example11-thermoMechanical-Local-VPN-JobMan'+os.path.sep+'inputT11.in'

nshost = cfg.nshost #NameServer - do not change
nsport = cfg.nsport #NameServer's port - do not change
hkey = cfg.hkey #Password for accessing nameServer and applications

server = cfg.server#IP of your server
serverNathost=cfg.server
