import os
from PIL import Image
import csv
import shutil

folderPath = "F:/"

validCount = 0
validMoved = [0, 0]
validPath = "./Valid"

corruptCount = 0
corruptMoved = [0, 0]
corruptPath = "./Corrupt"

csvFileName = "status.csv"

""" folderPath = "F:/"
validPath = "E:/New folder/rec/Valid"
corruptPath = "E:/New folder/rec/Corrupt"
 """
fileEndings = ["jpg", "png"]


def Move(path, filename, destPath, successArray):

    if os.path.exists(destPath)  == False:
        os.mkdir(destPath)
    try:
        shutil.move((path + "/" + filename), (destPath + "/" + filename))
        successArray[0] += 1
        return "True"
    except:
        print("Error: copying file: ", filename)
        successArray[1] += 1
        return "False"


rw = "w"
if os.path.exists(csvFileName):
    rw = "a"

print(rw)
fileCount = len([f for f in os.listdir(folderPath)
                if os.path.isfile(os.path.join(folderPath, f))])
progress = fileCount

print("{}/{} Remaining".format(progress, fileCount))
input("Press enter to start")
with open(csvFileName, mode=rw) as csv_file:
    fieldNames = ['FileName', 'valid', 'Moved']
    writer = csv.DictWriter(csv_file, fieldnames=fieldNames)

    if rw == "w":
        writer.writeheader()

    for fileName in os.listdir(folderPath):
        if fileName.lower().endswith(tuple(fileEndings)):
            print("{}/{} Remaining".format(progress, fileCount))
            try:
                img = Image.open(folderPath + "/"+ fileName)
                img.verify()
                print("Works: ", fileName)
                validCount += 1
                moved = Move(folderPath, fileName, validPath, validMoved)
                writer.writerow(
                    {'FileName': fileName, 'valid': 'True', 'Moved': moved})

            except (IOError, SyntaxError) as e:
                corruptCount += 1
                print('Corrupt file:', fileName)
                moved = Move(folderPath, fileName, corruptPath, corruptMoved)
                writer.writerow(
                    {'FileName': fileName, 'valid': 'False', 'Moved': moved})
            progress = progress - 1


print("""
Valid file: {}
Valid files moved: {}
Valid files not moved: {}
Corrupted files: {}
Corrupted files moved: {}
Corrupted files not moved: {}
""".format(validCount, validMoved[0], validMoved[1], corruptCount, corruptMoved[0], corruptMoved[1]))
