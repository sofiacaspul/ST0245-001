import sys
import numpy as np
from scipy.ndimage.filters import convolve
import pandas as pd
from numpy import genfromtxt
import matplotlib
from matplotlib import pyplot
from matplotlib.image import imread
import pathlib

def calc_energy(img):

    #sobel operator deteccion de bordes, calcula la intesidad de la imagen(energia)
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])

    img = img.astype('float32')
    energy_map = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    return energy_map
    
    
def main():


    if len(sys.argv) != 3:
        print('\nusage: ejemplo.py <path_dir_in> <energyPath_out>')
        sys.exit(1)

    in_dirPath = sys.argv[1] #nombre del directorio q se lee
    outEnergy_path = sys.argv[2] #nombre del directorio donde se veran los mapas de energia

    directory = pathlib.Path(in_dirPath)
    
    for in_filename in directory.iterdir():
        
        csvFile = np.genfromtxt(in_filename, delimiter=',')
        energy_map = calc_energy(csvFile)

        outEnergy_path_temp = outEnergy_path + '\\' +  in_filename.name[:-4] + ".png"
        print(outEnergy_path_temp)
        
        matplotlib.image.imsave(outEnergy_path_temp, energy_map, cmap='gray')


    # image_2 = imread('imageNormal.png')
    # image_1 = imread('output.png')
    # # plot raw pixel data
    # # pyplot.imshow(image_2)
    # # pyplot.show()
    # pyplot.imshow(image_1)
    # # show the figure
    # pyplot.show()

if __name__ == '__main__':
    main()