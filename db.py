from PIL import Image
import os, os.path

class DB:
    def __init__(self):
        self.totalImage = 0
        self.imageListPath = []     # Store path of all image
        self.imageList = []     # Store Image

    def LoadDB(self, path="database"):
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
        
    def __str__(self):

        return "------------ Database ------------\n" + \
                f"Total image: {self.totalImage},\nImage Path:\n\t" + \
                "\n\t".join(item for item in self.imageListPath) + \
                "\n---------------------------------"