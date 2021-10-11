import sys
import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve

# tqdm is not strictly necessary, but it gives us a pretty progress bar
# to visualize progress.
from tqdm import trange

def calc_energy(img):

    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # Dado que jpg tiene tres canales replicamos la matriz 1D por una 3D para cada canal
    filter_du = np.stack([filter_du] * 3, axis=2)
    
    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # Dado que jpg tiene tres canales replicamos la matriz 1D por una 3D para cada canal
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))
    #sumamos las energias de los canales red, green and blue
    energy_map = convolved.sum(axis=2)
    
    return energy_map
    
    
def main():

    in_filename = sys.argv[1]
    out_filename = sys.argv[2]

    img = imread(in_filename)
    out = calc_energy(img)
    print(out)
    print(out.shape)
    imwrite(out_filename, out)

if __name__ == '__main__':
    main()