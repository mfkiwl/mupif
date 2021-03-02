# converted from examples/Example09
from builtins import str

import unittest,sys
sys.path.append('../..')

from mupif import *
from mupif.tests import demo
import mupif.physics.physicalquantities as PQ

timeUnits = PQ.makeUnit('s',   1.,    [0,0,1,0,0,0,0,0,0])

class TestUnits(unittest.TestCase):
    def setUp(self):
        self.app1=demo.AppCurrTime(None)
    def tearDown(self):
        self.app1.terminate()
    def testUnits(self):
        app1=self.app1
        time,targetTime,timestepnumber=0,10,0
        while True:
            #determine critical time step
            dt = app1.getCriticalTimeStep().inUnitsOf(timeUnits).getValue()
            #update time
            time = time+dt
            if (time > targetTime):
                #make sure we reach targetTime at the end
                time = targetTime
            timestepnumber = timestepnumber+1
            # print ("Step: ", timestepnumber, time, dt)
            # create a time step
            istep = timestep.TimeStep(time, dt, targetTime, timeUnits, timestepnumber)
          
            #solve problem 1
            app1.solveStep(istep)
            #request Concentration property from app1
            v = app1.getProperty(PropertyID.PID_Velocity, istep.getTime())
          
            #Create a PhysicalQuantity object 
            V = PQ.makeQuantity(v.getValue(istep.getTime()), v.getUnits())

            velocity = V.inBaseUnits()
            self.assert_(v.getValue(istep.getTime())==time)

            #can be converted in km/s?
            self.assert_(V.isCompatible('km/s'))

            #can be converted in km?
            self.assertFalse(V.isCompatible('km'))
          
            # convert in km/h
            V.convertToUnit('km/h') 
            #sys.stderr.write(str(V))

            #give only the value
            value = float(str(V).split()[0])
            self.assertAlmostEqual(value,3.6*v.getValue(istep.getTime()))

            if time==targetTime: break


