
import PIL.Image as img
import os, os.path


# The following are from another script and has little to do with CSE5544 project.
# They are put here merely as reference or placeholder 

# Although the image finding functions may be of help


def openAndConvert(dirFileNames=[], filesNames=[], outDir = './/OutputImages//', targetFormat ="png"):
    '''Given the files, open them and convert to another format and then save'''

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for name, file in enumerate(dirFileNames):
        im = img.open(file).convert("RGB")
        noExtName = filesNames[name][:-4]
        print(filesNames[name][:-4])
        im.save(outDir + noExtName + '.' + targetFormat)


def getImages(path='.//Images//Baseline', targetFormat ="png"):
    dirFileNames = []
    filesNames = []
    valid_images = [".jpg"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        dirFileNames.append(os.path.join(path, f))
        filesNames.append(f)

    return dirFileNames, filesNames


dirFileNames, filesNames = getImages()
openAndConvert(dirFileNames=dirFileNames, filesNames=filesNames)