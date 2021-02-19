from builtins import str
import sys
sys.path.append('../../..')
from mupif import *
import os
import logging
log = logging.getLogger()
import mupif.physics.physicalquantities as PQ

class application1(model.Model):
    """
    Simple application that generates a property with a value equal to actual time
    """
    def __init__(self):
        super(application1, self).__init__()
        return
    def getProperty(self, propID, time, objectID=0):
        if (propID == PropertyID.PID_Concentration):
            return property.ConstantProperty(self.value, PropertyID.PID_Concentration, ValueType.Scalar, 'kg/m**3', time)
        else:
            raise apierror.APIError ('Unknown property ID')
    def solveStep(self, tstep, stageID=0, runInBackground=False):
        time = tstep.getTime().inUnitsOf('s').getValue()
        self.value=1.0*time
    def getCriticalTimeStep(self):
        return PQ.PhysicalQuantity(0.1,'s')
    def getAssemblyTime(self, tstep):
        return tstep.getTime()


class application3(model.Model):
    """
    Simple application that computes an arithmetical average of mapped property using an external code
    """
    def __init__(self):
        # list storing all mapped values from the beginning
        super(application3, self).__init__()
        self.values = []
    def getProperty(self, propID, time, objectID=0):
        if (propID == PropertyID.PID_CumulativeConcentration):
            log.debug("Getting property name: %s with ID  %d" % (PropertyID.PID_CumulativeConcentration.name,PropertyID.PID_CumulativeConcentration.value) )
            # parse output of application3 
            f = open('app3.out', 'r')
            answer = float(f.readline())
            f.close()
            return property.ConstantProperty(answer, PropertyID.PID_CumulativeConcentration, ValueType.Scalar, 'kg/m**3', time, 0)
        else:
            raise apierror.APIError ('Unknown property ID')
    def setProperty(self, property, objectID=0):
        if (property.getPropertyID() == PropertyID.PID_Concentration):
            # remember the mapped value
            self.concentration=property
        else:
            raise apierror.APIError ('Unknown property ID')
    def solveStep(self, tstep, stageID=0, runInBackground=False):
        if (tstep.getNumber() == 1):
            f=open('app3.in', 'w')
        else:
            f = open('app3.in', 'a')
        # process list of mapped values and store them into an external file 
        f.write(str(self.concentration.getValue(self.getAssemblyTime(tstep)))+'\n')
        f.close()
        # execute external application to compute the average
        os.system("./application3")

    def getCriticalTimeStep(self):
        return PQ.PhysicalQuantity(1.0,'s')
    def getAssemblyTime(self, tstep):
        return tstep.getTime()

class Demo03(workflow.Workflow):
    def __init__ (self, targetTime=PQ.PhysicalQuantity('0 s')):
        super(Demo03, self).__init__(targetTime=targetTime)
        
        self.app1 = application1()
        self.app3 = application3()
        
    def initialize(self):
        MD = { 'model.Model_description' : 'Workflow with two applications computing average' }
        super(Demo03, self).initialize(metaData=MD)
        MD = { 'model.Model_description' : 'App1 stores actual time' }
        self.app1.initialize(metaData=MD)
        MD = { 'model.Model_description' : 'App3 computes the average' }
        self.app3.initialize(metaData=MD)

    def solveStep (self, istep, stageID=0, runInBackground=False):

        #solve problem 1
        self.app1.solveStep(istep)
        #handshake Concentration property from app1 to app2
        self.app3.setProperty (self.app1.getProperty(PropertyID.PID_Concentration,
                                                     self.app3.getAssemblyTime(istep)))
        # solve second sub-problem 
        self.app3.solveStep(istep)

        self.app1.finishStep(istep)
        self.app3.finishStep(istep)

    def getCriticalTimeStep(self):
        # determine critical time step
        
        return min (self.app1.getCriticalTimeStep(), self.app3.getCriticalTimeStep())

    def terminate(self):
        #self.thermalAppRec.terminateAll()
        self.app1.terminate()
        self.app3.terminate()
        super(Demo03, self).terminate()

    def getApplicationSignature(self):
        return "Demo03 workflow 1.0"

    def getAPIVersion(self):
        return "1.0"

    def setProperty(self, property, objectID=0):
         if (property.getPropertyID() == PropertyID.PID_UserTimeStep):
             # remember the mapped value
             self.userDT = PQ.PhysicalQuantity(property.getValue()[0], property.getUnits())
         else:
             raise apierror.APIError ('Unknown property ID')
    def getProperty(self, propID, time, objectID=0):
         if (propID == PropertyID.PID_KPI01):
             return self.app3.getProperty (PropertyID.PID_CumulativeConcentration, time)
         else:
             raise apierror.APIError ('Unknown property ID')
        
if __name__=='__main__':
    # instanciate workflow
    targetTime =PQ.PhysicalQuantity(3.0, 's')
    demo = Demo03(targetTime)
    demo.initialize()
    # pass some parameters using set ops
    demo.setProperty(property.ConstantProperty((0.2,), PropertyID.PID_UserTimeStep, ValueType.Scalar, 's'))
    #execute workflow
    demo.solve()
    #get resulting KPI for workflow
    kpi01 = demo.getProperty (PropertyID.PID_KPI01, targetTime)

    log.info("KPI returned " +  str(kpi01.getValue(targetTime)) + str(kpi01.getUnits()))

    if (kpi01.getValue(targetTime) == 1.55):
        log.info("Test OK")
        sys.exit(0)
    else:
        log.info("Test FAILED")
        sys.exit(1)


