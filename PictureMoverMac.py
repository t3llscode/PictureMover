import os
import glob
import shutil
from datetime import datetime
from datetime import timedelta as TD

def main():
    
    while True:
        #MAC os.system("cls")
        Es.resetLog()
        pictureMove = Mover([Directory(Es.sdCard, Es.allSuffixes)], [Directory(Es.picPath, Es.picSuffixes), Directory(Es.vidPath, Es.vidSuffixes)])
        input()

class Es:

    picSuffixes = [".ARW", ".JPG", ".dng", ".tif"]
    vidSuffixes = [".XML", ".MP4"]

    allSuffixes = picSuffixes + vidSuffixes

    # end with slash

    # picPath = "/Volumes/media/01 Media/00 Pictures/"
    # vidPath = "/Volumes/media/01 Media/01 Videos/"
    # sdCard = "/Volumes/4TB 990Pro/SD Cards/"

    picPath = "/Volumes/4TB 990Pro/SD Cards/00 Pictures/"
    vidPath = "/Volumes/4TB 990Pro/SD Cards/01 Videos/"
    sdCardName = "Untitled"
    sdCard = f"/Volumes/{sdCardName}/"

    SAVE_LOG = False
    logDir = "/path/to/log.txt"

    def log(text):
        if Es.SAVE_LOG:
            t = str(datetime.now()) + " " + text
            with open(Es.logDir, "a") as file:
                file.write(t + "\n")

    def resetLog():
        
        if Es.SAVE_LOG:
            with open(Es.logDir, "w") as file:
                file.write("")

class File:

    path = None
    name = None
    suffix = None
    sizeMB = 0.0
    cDate = None

    def __init__(self, _path) -> None:
        self.sdCardName = Es.sdCardName # this could be done different in a future version to run over multiple SD cards
        self.path = _path.replace("\\", "\\\\")
        self.dir = os.path.dirname(self.path)
        self.name = os.path.basename(self.path)
        self.newName = f"{Es.sdCardName}-{self.name}"
        self.newPath = os.path.join(self.dir, self.newName)
        self.suffix = os.path.splitext(self.path)[-1]
        self.sizeMB = os.path.getsize(self.path)/1024/1024
        self.cDate = datetime.fromtimestamp(os.path.getctime(self.path))

class Directory:

    path = None
    acceptedSuffixes = None
    files = None
    
    def __init__(self, _path, _acceptedSuffixes) -> None:
        self.path = _path
        self.createDir()
        self.acceptedSuffixes = _acceptedSuffixes
        self.files = self.updateFiles()

    def createDir(self):
        while not os.path.exists(self.path):
            try:    
                os.makedirs(self.path, exist_ok = False)
                Es.log(f"Directory {self.path} was created")
            except:
                input(f"Please ensure that {self.path} is available and confirm with \"Enter\".")
                #MAC os.system("cls")     

    def updateFiles(self):
        tmp = []
        for suffix in self.acceptedSuffixes:
            for path in glob.glob(self.path + "**/*" + suffix, recursive = True):
                tmp.append(File(path))
        return tmp

class Mover:

    srcDirs = []
    desDirs = []
    srcFiles = []
    moves = []
    movesMB = 0

    def __init__(self, _srcDirs, _desDirs) -> None:
        self.srcDirs = _srcDirs
        self.desDirs = _desDirs
        self.srcFiles = [file for dir in self.srcDirs for file in dir.files]
        self.movesMB = self.initiateMove()
        if len(self.moves) > 0:
            self.move()
        else:
            print("All files are up to date!")

    def initiateMove(self):
        for dir in self.desDirs:
            files = list(filter(lambda file: file.path.endswith(tuple(dir.acceptedSuffixes)) and not os.path.exists(os.path.join(dir.path, file.cDate.strftime("%Y-%m-%d"), file.newName)), self.srcFiles))
            for file in files:
                self.moves.append([file, dir])
                Es.log(f"File \"{file.path}\" was linked to Directory \"{dir.path}\"")
        print(f"Detected {len(self.srcFiles) - len(self.moves)} known and {len(self.moves)} new files on {', '.join(map(str, [dir.path for dir in self.srcDirs]))}")
        return round(sum([dataset[0].sizeMB for dataset in self.moves]), 2)

    def move(self):
        mbTransferred = [[0.0, datetime.now()]]
        
        print(f"Moving {len(self.moves)} files, {self.movesMB} MB in size")
        for dataset in self.moves:
            desDir = dataset[1].path + dataset[0].cDate.strftime("%Y-%m-%d/")
            if not os.path.exists(desDir):
                Directory(desDir, dataset[1].acceptedSuffixes)
            shutil.copy2(dataset[0].path, desDir + dataset[0].newName)
            mbTransferred.append([mbTransferred[-1][0] + dataset[0].sizeMB, datetime.now()])
            print(self.getTransferedOverview(mbTransferred) + Mover.getTransferedSpeed(mbTransferred), end = "\r")
        print("Transfer successfully completed!                                                                                              ")
        if Es.SAVE_LOG:
            Es.log("Detailed Log: " + Es.logDir)
        else:
            print("To get a detailed log, please set the variable \"SAVE_LOG\" to \"True\".")

    def getTransferedSpeed(list):
        if len(list) > 1:
            return f" (@ {round(((list[-2][0]- list[-1][0]) / TD.total_seconds(list[-2][1]- list[-1][1])), 2)} MB/s)                                                      "
        else:
            return ""

    def getTransferedOverview(self, list):
        return f"File {len(list)}/{len(self.moves)} - {round(list[-1][0], 2)}/{self.movesMB} MB"

if __name__=="__main__":
    main()