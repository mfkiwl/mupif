import mupif
import Pyro5


@Pyro5.api.expose
class DFT_Pre(mupif.Model):
    def __init__(self, metadata=None):

        MD = {
            "ClassName": "DFT_Pre",
            "ModuleName": "dft_pre",
            "Name": "DFT Pre",
            "ID": "dft_pre",
            "Description": "DFT Pre",
            "Version_date": "1.0.0, Jan 2023",
            "Inputs": [
                {
                    "Name": "InpProp",
                    "Type": "mupif.Property",
                    "Required": True,
                    "Type_ID": "mupif.DataID.ID_None",
                    "Units": "",
                    "Obj_ID": "",
                    "Set_at": "timestep",
                    "ValueType": "Scalar"
                },
                {
                    "Name": "InpHS",
                    "Type": "mupif.HeavyStruct",
                    "Required": True,
                    "Type_ID": "mupif.DataID.ID_None",
                    "Units": "",
                    "Obj_ID": "",
                    "Set_at": "timestep"
                }
            ],
            "Outputs": [
                {
                    "Name": "OutHS",
                    "Type": "mupif.HeavyStruct",
                    "Type_ID": "mupif.DataID.ID_None",
                    "Units": "",
                    "Obj_ID": ""
                },
                {
                    "Name": "OutStrings",
                    "Type": "mupif.DataList[mupif.String]",
                    "Type_ID": "mupif.DataID.ID_None",
                    "Units": "",
                    "Obj_ID": ""
                }
            ],
            "Solver": {
                "Software": "Own",
                "Type": "tester",
                "Accuracy": "High",
                "Sensitivity": "Low",
                "Complexity": "High",
                "Robustness": "High",
                "Estim_time_step_s": 1,
                "Estim_comp_time_s": 1,
                "Estim_execution_cost_EUR": 0.01,
                "Estim_personnel_cost_EUR": 0.01,
                "Required_expertise": "None",
                "Language": "",
                "License": "LGPL",
                "Creator": "",
                "Version_date": "1.0.0, Jan 2023",
                "Documentation": "not available"
            },
            "Physics": {
                "Type": "Other",
                "Entity": "Other"
            },
            "Execution_settings": {
                "Type": "Distributed",
                "jobManName": "UOI.DFT_Pre",
                "Class": "DFT_Pre",
                "Module": "dft_pre"
            }
        }

        super().__init__(metadata=MD)
        self.updateMetadata(metadata)

        self.input_InpProp = None
        self.input_InpHS = None
        self.output_OutHS = None
        self.output_OutStrings = None

    def initialize(self, workdir='', metadata=None, validateMetaData=True, **kwargs):
        super().initialize(workdir=workdir, metadata=metadata, validateMetaData=validateMetaData, **kwargs)

    def get(self, objectTypeID, time=None, objectID=""):
        if objectTypeID == mupif.DataID.ID_None and objectID == "":
            if self.output_OutHS is None:
                raise ValueError("Value not defined")
            return self.output_OutHS
        if objectTypeID == mupif.DataID.ID_None and objectID == "":
            if self.output_OutStrings is None:
                raise ValueError("Value not defined")
            return self.output_OutStrings

    def set(self, obj, objectID=""):
        if obj.isInstance(mupif.Property) and obj.getDataID() == mupif.DataID.ID_None and objectID == "":
            self.input_InpProp = obj
        if obj.isInstance(mupif.HeavyStruct) and obj.getDataID() == mupif.DataID.ID_None and objectID == "":
            self.input_InpHS = obj

    def getApplicationSignature(self):
        return "DFT_Pre"

    def getAPIVersion(self):
        return 1

    def solveStep(self, tstep, stageID=0, runInBackground=False):
        for inp in [self.input_InpProp, self.input_InpHS]:
            if inp is None:
                raise ValueError("A required input was not defined")

        raise NotImplementedError("Not implemented")


if __name__ == '__main__':
    import dft_pre

    mupif.SimpleJobManager(
        ns=mupif.pyroutil.connectNameserver(),
        appClass=dft_pre.DFT_Pre,
        appName='UOI.DFT_Pre',
        maxJobs=10
    ).runServer()
