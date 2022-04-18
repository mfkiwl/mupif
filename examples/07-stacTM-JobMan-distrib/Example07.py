import Pyro5
import threading
import time as timeT
import sys
sys.path.extend(['.', '..', '../..'])
from mupif import *
import mupif as mp
import logging
log = logging.getLogger()


class Example07(workflow.Workflow):
   
    def __init__(self, metadata={}):
        """
        Initializes the workflow. As the workflow is non-stationary, we allocate individual 
        applications and store them within a class.
        """
        MD = {
            'Name': 'Thermo-mechanical non-stationary problem',
            'ID': 'Thermo-mechanical-1',
            'Description': 'Non-stationary thermo-mechanical problem using finite elements on rectangular domain',
            # 'Dependencies' are generated automatically
            'Version_date': '1.0.0, Feb 2019',
            'Inputs': [],
            'Outputs': [
                {'Type': 'mupif.Field', 'Type_ID': 'mupif.DataID.FID_Displacement', 'Name': 'Displacement field',
                 'Description': 'Displacement field on 2D domain', 'Units': 'm'}]
        }
        super().__init__(metadata=MD)
        self.updateMetadata(metadata)

        self.thermalJobMan = None
        self.mechanicalJobMan = None
        self.thermalSolver = None
        self.mechanicalSolver = None
        self.daemon = None

    def initialize(self, workdir='', metadata={}, validateMetaData=True, **kwargs):
        # locate nameserver
        ns = pyroutil.connectNameserver()
        self.daemon = pyroutil.getDaemon(ns)

        # connect to JobManager running on (remote) server
        self.thermalJobMan = pyroutil.connectJobManager(ns, 'Mupif.JobManager@ThermalSolver-ex07')
        self.mechanicalJobMan = pyroutil.connectJobManager(ns, 'Mupif.JobManager@MechanicalSolver-ex07')

        # allocate the application instances
        try:
            self.thermalSolver = pyroutil.allocateApplicationWithJobManager(
                ns=ns,
                jobMan=self.thermalJobMan,
            )
            log.info('Created thermal job')
            self.mechanicalSolver = pyroutil.allocateApplicationWithJobManager(
                ns=ns,
                jobMan=self.mechanicalJobMan,
            )
            log.info('Created mechanical job')
        except Exception as e:
            log.exception(e)
            return False
        else:  # No exception
            self.registerModel(self.thermalSolver, 'thermal')
            self.registerModel(self.mechanicalSolver, 'mechanical')

            ival = super().initialize(workdir=workdir, metadata=metadata, validateMetaData=validateMetaData, **kwargs)
            if ival is False:
                return False
            if (self.thermalSolver is not None) and (self.mechanicalSolver is not None):

                thermalSolverSignature = self.thermalSolver.getApplicationSignature()
                log.info("Working thermal solver on server " + thermalSolverSignature)

                mechanicalSolverSignature = self.mechanicalSolver.getApplicationSignature()
                log.info("Working mechanical solver on server " + mechanicalSolverSignature)

                # To be sure update only required passed metadata in models
                passingMD = {
                    'Execution': {
                        'ID': self.getMetadata('Execution.ID'),
                        'Use_case_ID': self.getMetadata('Execution.Use_case_ID'),
                        'Task_ID': self.getMetadata('Execution.Task_ID')
                    }
                }

                ival = self.thermalSolver.initialize(
                    workdir=self.thermalJobMan.getJobWorkDir(self.thermalSolver.getJobID()),
                    metadata=passingMD
                )
                if ival is False:
                    return False
                thermalInputFile = mp.PyroFile(filename='./inputT.in', mode="rb")
                self.daemon.register(thermalInputFile)
                self.thermalSolver.set(thermalInputFile)

                ival = self.mechanicalSolver.initialize(
                    workdir=self.mechanicalJobMan.getJobWorkDir(self.mechanicalSolver.getJobID()),
                    metadata=passingMD
                )
                if ival is False:
                    return False
                mechanicalInputFile = mp.PyroFile(filename='./inputM.in', mode="rb")
                self.daemon.register(mechanicalInputFile)
                self.mechanicalSolver.set(mechanicalInputFile)

            else:
                log.debug("Connection to server failed, exiting")

        return True

    def solveStep(self, istep, stageID=0, runInBackground=False):

        start = timeT.time()
        log.info('Timer started')
        log.info("Solving thermal problem")
        log.info(self.thermalSolver.getApplicationSignature())
        
        self.thermalSolver.solveStep(istep)
        log.info("Thermal problem solved")
        uri = self.thermalSolver.getFieldURI(DataID.FID_Temperature, self.mechanicalSolver.getAssemblyTime(istep))
        log.info("URI of thermal problem's field is " + str(uri))
        field = pyroutil.getObjectFromURI(uri)
        self.mechanicalSolver.set(field)
        log.info("Solving mechanical problem")
        self.mechanicalSolver.solveStep(istep)
        log.info("URI of mechanical problem's field is " + str(self.mechanicalSolver.getFieldURI(DataID.FID_Displacement, istep.getTargetTime())))
        displacementField = self.mechanicalSolver.get(DataID.FID_Displacement, istep.getTime())

        # save results as vtk
        temperatureField = self.thermalSolver.get(DataID.FID_Temperature, istep.getTime())
        temperatureField.toMeshioMesh().write('temperatureField.vtk')
        displacementField.toMeshioMesh().write('displacementField.vtk')
        log.info("Time consumed %f s" % (timeT.time()-start))

    def getCriticalTimeStep(self):
        # determine critical time step
        return 1*mp.U.s

    def terminate(self):
        self.thermalSolver.terminate()
        self.mechanicalSolver.terminate()
        super().terminate()

    def getApplicationSignature(self):
        return "Example07 workflow 1.0"

    def getAPIVersion(self):
        return "1.0"

    
if __name__ == '__main__':
    demo = Example07()
    md = {
        'Execution': {
            'ID': '1',
            'Use_case_ID': '1_1',
            'Task_ID': '1'
        }
    }
    demo.initialize(metadata=md)
    demo.set(mp.ConstantProperty(value=1.*mp.U.s, propID=mp.DataID.PID_Time, valueType=mp.ValueType.Scalar, unit=mp.U.s), objectID='targetTime')
    demo.solve()
    demo.printMetadata()
    demo.printListOfModels()
    demo.terminate()
    log.info("Test OK")
