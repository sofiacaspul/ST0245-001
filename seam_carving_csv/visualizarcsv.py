from numpy import genfromtxt
from matplotlib import pyplot
from matplotlib.image import imread

import matplotlib

def main():
    my_data = genfromtxt('example.csv', delimiter=',')
    matplotlib.image.imsave('output.png', my_data, cmap='gray')
    image_1 = imread('output.png')
    # plot raw pixel data
    pyplot.imshow(image_1)
    # show the figure
    pyplot.show()
main()