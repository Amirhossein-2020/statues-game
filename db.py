from PIL import Image
import os, os.path

class DB:
    def __init__(self):
        
        # * Image variables * #
        self.totalImage = 0
        
        # imageListPath & imageList have the same structure
        # Dict ["player_name"] = [list of images]
        self.imageListPath = {} # Store path of all image
        self.imageList = {}     # Store Image
        self.playerList = []    # db gets player name from the folder name # we can say playerList is a list of every folder inside database/players
        
        # * Audio variables * #
        self.totalAudio = 0

        # Dict ["type of audio"] = [list of .mp3]
        self.audioListPath = {} # Store audio .mp3
        self.audioDirList = []  # Store names of the folders inside database/audio

    def UpdateDB(self):

        # * Reset all variable * #
        self.totalImage = 0
        self.imageListPath = {}
        self.imageList = {}
        self.playerList = []
        self.totalAudio = 0
        self.audioListPath = {}
        self.audioDirList = []

        self.LoadDB()

    def LoadDB(self, path="database"):
        validImageExt = [".jpg", ".jpeg", ".png"]
        validAudioExt = [".mp3"]

        for TypedirName in os.listdir(path): # checking database/
            if os.path.isdir(f"{path}/{TypedirName}"):
                for dirName in os.listdir(f"{path}/{TypedirName}"): # checking database/type of dir
                    
                    # * IF YOU ADD OR CHANGE NAME TO FOLDERS, ADD/UPDATE IT HERE * #
                    if TypedirName == "players":
                        self.playerList.append(dirName)
                        self.imageListPath[dirName] = []
                        self.imageList[dirName] = []
                    elif TypedirName == "audio":
                        self.audioDirList.append(dirName)
                        self.audioListPath[dirName] = []

                    for filename in os.listdir(f"{path}/{TypedirName}/{dirName}"): # Checking database/type of dir/contents
                        
                        ext = os.path.splitext(filename)[1]

                        if TypedirName == "players":
                            if ext.lower() not in validImageExt:
                                continue

                            # Store image path
                            imgPath = f"{path}/{TypedirName}/{dirName}/{filename}"
                            self.imageListPath[dirName].append(imgPath)

                            # Store image
                            img = Image.open(imgPath)
                            self.imageList[dirName].append(img)

                            # Increase img counter
                            self.totalImage += 1
                        
                        elif TypedirName == "audio":
                            if ext.lower() not in validAudioExt:
                                continue

                            # Store audio path
                            audioPath = f"{path}/{TypedirName}/{dirName}/{filename}"
                            self.audioListPath[dirName].append(audioPath)

                            # Increase audio counter
                            self.totalAudio += 1


        print("------------------------")
        print(f"Loaded {self.totalImage} images.")
        print(f"Loaded {self.totalAudio} audio.")
        print("------------------------")

    # OUTDATED
    def __oldLoadDB(self, path="database/players"):
        validExt = [".jpg", ".jpeg", ".png"]

        for filename in os.listdir(path):
            ext = os.path.splitext(filename)[1]
            if ext.lower() not in validExt:
                continue

            # Store image path
            img_path = os.path.join(path, filename)
            self.imageListPath.append(img_path)

            # Store image
            img = Image.open(os.path.join(path, filename))
            self.imageList.append(img)

        self.totalImage = len(self.imageListPath)
        
    def printAllDatabase(self):

        print("\n---- Printing players ----")

        for player in self.playerList:
            print(player)

        print("\n---- Printing image path ----")

        for key in self.imageListPath.keys():
            if len(self.imageListPath[key]) == 0:
                print(key + " - empty")
            else:
                print(key)

                for item in self.imageListPath[key]:
                    if self.imageListPath[key][-1] == item:
                        print("  └─"+item)
                    else:
                        print("  ├─"+item)

        print("\n---- Printing audio path ----")
        
        for key in self.audioListPath.keys():
            if len(self.audioListPath[key]) == 0:
                print(key + " - empty")
            else:
                print(key)

                for item in self.audioListPath[key]:
                    if self.audioListPath[key][-1] == item:
                        print("  └─"+item)
                    else:
                        print("  ├─"+item)


    # OUTDATED
    # original name __str__
    def __str(self):

        return "------------ Database ------------\n" + \
                f"Total image: {self.totalImage},\nImage Path:\n\t" + \
                "\n\t".join(item for item in self.imageListPath) + \
                "\n---------------------------------"