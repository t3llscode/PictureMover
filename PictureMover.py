import os
import glob
import shutil
from typing import List
from datetime import datetime

def main():
    pictureMove = Mover(Essentials.sdCard, Essentials.picPath, Essentials.vidPath, True)

class Essentials:

    picSuffixes = [".ARW", ".JPG", ".dng", ".tif"]
    vidSuffixes = [".XML", ".MP4"]

    allSuffixes = []
    for l in (picSuffixes,vidSuffixes):
        allSuffixes.extend(l) 

    picPath = "E:\\01 Media\\00 Pictures\\"
    vidPath = "E:\\01 Media\\01 Videos\\"
    errPath = "E:\\01 Media\\_Transfer Errors\\"

    sdCard = "G:\\"

class File:

    path = None
    filePath = None
    name = None
    cDate = None
    found = False

    def __init__(self, _path) -> None:
        self.path = _path.replace("\\", "\\\\")
        self.filePath = self.checkIfPic()
        self.name = os.path.basename(self.path)
        self.cDate = datetime.fromtimestamp(os.path.getctime(self.path))
        
    def checkIfPic(self):
        suffix = os.path.splitext(self.path)[1]
        if suffix in Essentials.picSuffixes:
            return Essentials.picPath
        elif suffix in Essentials.vidSuffixes:
            return Essentials.vidPath
        else:
            print(f"[WARNING] {os.path.basename(self.path)} is in an unknown File Format")
            return Essentials.errPath
        
class Mover:

    searchDir = None
    picDir = None
    vidDir = None
    searchSub = True
    files = []

    def __init__(self, _searchDir, _picDir, _vidDir, _searchSub) -> None:
        self.directory = _searchDir
        self.picDir = _picDir
        self.vidDir = _vidDir
        self.searchSub = _searchSub
        self.files = self.findFiles()
        self.createFolders()
        self.moveFiles()

    def findFiles(self): 
        tmp = []  
        for suffix in Essentials.allSuffixes:
            for path in glob.glob(self.directory + "**\\*" + suffix, recursive = self.searchSub):
                tmp.append(File(path))
        return tmp

    def createFolders(self):
        tmp = []
        dateList = [[], []] # 0 = pic # 1 = vid
        for file in self.files:
            if file.filePath == Essentials.picPath:
                tmp = [dateList[0]]
            elif file.filePath == Essentials.vidPath:
                tmp = [dateList[1]]
            tmp[0].append(file.cDate.strftime("%Y-%m-%d"))
        for d in range(len(dateList)):
            for date in list(dict.fromkeys(dateList[d])):
                if d == 0:
                    tmp = [self.picDir, "Picture Directory"]
                elif d == 1:
                    tmp = [self.vidDir, "Video Directory"]
                try:    
                    os.makedirs(tmp[0] + date, exist_ok = False)
                    print(f"[LOG] Created {tmp[1]} \"{date}\"")
                except:
                    print(f"[WARNING] {tmp[1]} \"{date}\" already existing")
    
    def moveFiles(self):
        for file in self.files:
            shutil.copy2(file.path, file.filePath + file.cDate.strftime("%Y-%m-%d\\") + file.name)
            print(f"[LOG] {file.name} was moved to " + file.filePath + file.cDate.strftime("%Y-%m-%d\\") + file.name)

if __name__=="__main__":
    main()