from builtins import range, object


class RemoteAppRecord (object):
    """
    Class keeping internal data on remote application. The data contain:
    * appTunnel: reference to application ssh tunnel
    * jobMan: reference to jobManager 
    * jobManTunnel: reference to jobManager tunnel representation
    * jobID: jobID of application
    .. automethod:: __init__
    """
    def __init__(self, app, appTunnel, jobMan, jobManTunnel, jobID):
        """
        Constructor. Initializes the receiver
        :param Application app: application instance
        :param subprocess.Popen appTunnel: ssh tunnel subprocess representing ssh tunnel to application process
        :param JobManager jobMan: job manager instance that allocated application
        :param subprocess.Popen jobManTunnel: ssh tunnel subprocess representing ssh tunnel to jobManager
        :param string jobID: application jobID
        """
        self.app = []
        self.app.append(app)
        self.appTunnel = []
        self.appTunnel.append(appTunnel)
        self.jobMan = jobMan
        self.jobManTunnel = jobManTunnel
        self.jobID = []
        self.jobID.append(jobID)

    def appendNextApplication(self, app, appTunnel, jobID):
        """
        Append next application on existing instance
        :param Application app: application instance
        :param subprocess.Popen appTunnel: ssh tunnel subprocess representing ssh tunnel to application process
        :param string jobID: application jobID
        """
        self.app.append(app)
        self.appTunnel.append(appTunnel)
        self.jobID.append(jobID)

    def getApplication(self, num=0):
        """
        Returns application instance
        :param int num: number of application, default 0
        :return: Instance of Application
        """
        return self.app[num]

    def getApplicationUri(self, num=0):
        """
        Returns application uri
        :param int num: number of application, default 0
        :return: uri
        """
        return self.app[num].getURI()

    def getJobManager(self):
        return self.jobMan

    def getJobID(self, num=0):
        return self.jobID[num]

    def terminateAll(self):
        """
        Terminates all remote applications in app[] including their ssh tunnels.
        Terminates also jobManager and the associated ssh tunnel.
        """
        for i in range(0, len(self.app)):
            if self.app is not None:
                self.terminateApp(i)
                if self.jobMan:
                    self.jobMan.terminateJob(self.jobID[i])
        if self.jobManTunnel:
            if self.jobManTunnel != 'manual':
                self.jobManTunnel.terminate()

    def terminateApp(self, num):
        """
        Terminates app[num] and its ssh tunnel. Job manager and its tunnel remains untouched.
        :param int num: number of application
        """
        if self.app[num]:
            self.app[num].terminate()
        if self.appTunnel[num]:
            if self.appTunnel[num] != 'manual':
                self.appTunnel[num].terminate()
