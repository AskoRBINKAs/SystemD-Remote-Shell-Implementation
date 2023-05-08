import os
import subprocess
from threading import Thread
import pickle


SYSTEMCTL_PATH="/usr/bin/systemctl"
JOURNALCTL_PATH="/usr/bin/journalctl"


class Core:
    def __init__(self):
        self.version = "v0.1-dev"
        self.daemons_list={}
        self.restoreDaemons()
        self.checkStatusOfDaemons()

    def addDaemon(self,name,ptsf,category):
        self.daemons_list[name] = Daemon(name,ptsf,category)
        self.saveDaemons()

    def saveDaemons(self):
        for daemon in self.daemons_list:
            with open(f'{self.daemons_list[daemon].name}.pkl','wb') as fp:
                pickle.dump(self.daemons_list[daemon],fp)
            os.replace(f'{self.daemons_list[daemon].name}.pkl', f"saved/{self.daemons_list[daemon].name}.pkl")
        return f"All {len(self.daemons_list)} saved"

    def checkStatusOfDaemons(self):
        for daemon in self.daemons_list:
            self.daemons_list[daemon].getStatus()
    def restoreDaemons(self):
        try:
            for files in os.listdir("saved/"):
                with open("saved/"+files,'rb') as fp:
                    self.daemons_list[files.replace('.pkl','')]=(pickle.load(fp))
        except Exception as e:
            return f'Error caused during restoring daemons from files:\n{e}'
            
    def getVersion(self):
        return self.version

    def getDaemonList(self):
        self.checkStatusOfDaemons()
        list_text=""
        for daemon in self.daemons_list:
            list_text+=f'{self.daemons_list[daemon].name} - {self.daemons_list[daemon].category} - {self.daemons_list[daemon].status}\n'
        return list_text

    def stopDaemon(self,name):
        self.daemons_list[name].stopDaemon()
        return f'Daemon {name} will be stopped\n'

    def stopAllDaemons(self):
        for daemon in self.daemons_list:
            self.daemons_list[daemon].stopDaemon()
        return f'All {len(self.daemons_list)} daemons will be stopped\n'

    def startDaemon(self,name):
        self.daemons_list[name].startDaemon()
        return f'Daemon {name} will be started\n'

    def startAllDaemons(self):
        for daemon in self.daemons_list:
            self.daemons_list[daemon].startDaemon()
        return f'All {len(self.daemons_list)} daemons will be started\n'

    def restartDaemon(self, name):
        self.daemons_list[name].startDaemon()
        return f'Daemon "{name}" will be restarted\n'

    def restartAllDaemons(self):
        for daemon in self.daemons_list:
            self.daemons_list[daemon].restartDaemon()
        return f'All {len(self.daemons_list)} daemons will be restarted\n'

    def getRunningDaemons(self):
        output=""
        for daemon in self.daemons_list:
            if self.daemons_list[daemon].status == "RUNNING":
                output+=f"{self.daemons_list[daemon].name} - {self.daemons_list[daemon].category}\n"
        return output

    def getStoppedDaemons(self):
        output=""
        for daemon in self.daemons_list:
            if self.daemons_list[daemon].status != "RUNNING":
                output+=f"{self.daemons_list[daemon].name} - {self.daemons_list[daemon].category}\n"
        return output
class Daemon:
    def __init__(self,name,path_to_service_file,category):
        self.name = name
        self.path_to_service_file = path_to_service_file
        self.status = None
        self.category = category
        self.isFavourite= False

    def __getstate__(self) -> dict:
        state={}
        state['name'] = self.name
        state['ptsf'] = self.path_to_service_file
        state['category'] = self.category
        state['isFavourite'] = self.isFavourite
        return state

    def __setstate__(self,state:dict):
        self.name = state['name']
        self.path_to_service_file = state['ptsf']
        self.category = state['category']
        self.isFavourite = state['isFavourite']

    def getStatus(self):
        try:
            output = subprocess.check_output([SYSTEMCTL_PATH, 'status', self.name], encoding="UTF-8")
            if output.find('active (running)')!=-1:
                self.status = "RUNNING"
            else:
                self.status = "STOPPED"
            return output
        except:
            self.status = "STOPPED"
        return f'{self.name} expected error while checking the status'

    def getServiceFile(self):
        try:
            output = subprocess.check_output(['cat',self.path_to_service_file],encoding="UTF-8")
            return output
        except Exception as e:
            return f'{e}'
    def getLog(self):
        output = subprocess.check_output([JOURNALCTL_PATH,'-u',self.name],encoding="UTF-8")
        return output

    def stopDaemon(self):
        Thread(target=lambda: subprocess.check_output([SYSTEMCTL_PATH,'stop',self.name],encoding='UTF-8')).start()
        return f'Trying to stop {self.name}. Check log or status later'

    def startDaemon(self):
        Thread(target=lambda: subprocess.check_output([SYSTEMCTL_PATH,'start',self.name],encoding='UTF-8')).start()
        return f'Trying to start {self.name}. Check log or status later'

    def restartDaemon(self):
        Thread(target=lambda: subprocess.check_output([SYSTEMCTL_PATH,'stop',self.name],encoding='UTF-8')).start()
        return f'Trying to statr {self.name}. Check log or status later'

    def changeCategory(self,category):
        old_category = self.category
        self.category = category
        return f'Category for {self.name} changed from {old_category} to {self.category}'