import pandas as pd
import pathlib

pathName = "./datasets/enfermos"
directory = pathlib.Path(pathName)
binaryImages = {}

for file in directory.iterdir():
    fileName = file.name
    matriz = pd.read_csv(file)
    binaryImages[fileName] = matriz


print (binaryImages)
