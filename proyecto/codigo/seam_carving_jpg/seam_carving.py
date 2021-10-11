import sys
import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve

# tqdm es para ver una barra de progreso
from tqdm import trange

def calc_energy(img):
    # print(img)
    # exit()
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

    # We sum the energies in the red, green, and blue channels
    energy_map = convolved.sum(axis=2)

    return energy_map

def minimum_seam(img, energy_map):
    r, c, _ = img.shape
    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=int)#creo un array con de la misma dimesion que M y lo lleno de 0

    # Sacamos el valor de arriba hacia abajo minimo para recorrer la matriz y guardamos los valores en M
    # En backtrack guardamos los caminos q debemos tomar para llegar a x valor de la ultima fila de M
    for i in range(1, r):
        for j in range(0, c):
            #Nos aseguramos que no haya un desbordamiento siendo j -1
            if j == 0:
                idx = np.argmin(M[i - 1, j:j + 2]) #retorna el nume
                backtrack[i, j] = idx + j
                min_energy = M[i - 1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy
    return M, backtrack

def carve_column(img, energyMap):
    
    r, c, _ = img.shape #image size
    M, backtrack = minimum_seam(img, energyMap)

    # Creamos una matriz r*c donde la llenamos con un valor TRUE y luego cambiamos algunas 
    # posiciones a False que seran los pixeles a eliminar
    mask = np.ones((r, c), dtype=bool)

    # Encuentre la posicion con el menor valor en la ultima fila
    j = np.argmin(M[-1])
    
    for i in reversed(range(r)):
        # marcamos el pixel para luego eliminarlo
        mask[i, j] = False
        j = backtrack[i, j]

    #Elimino el borde con menos energia del mapa energetico
    energyMap = energyMap[mask].reshape(r, c - 1)
    #Como la imagen tiene 3 canales, convertimos mask a 3D
    mask = np.stack([mask] * 3, axis=2)
    # Eliminamos todos los pixeles marcados como falso en mask y luego le hacemos
    # resize a la nueva dimension de la imagen
    img = img[mask].reshape((r, c - 1, 3))

    return img, energyMap

def crop_c(img, energyMap, scale_c):
    
    r, c, _ = img.shape
    new_c = int(scale_c * c)
    for _ in trange(c - new_c): # tqdm es lo mismo que un range pero sirve para mostrar una barra de carga
        img, energyMap = carve_column(img, energyMap)

    return img, energyMap

def crop_r(img, energyMap, scale_r):
    img = np.rot90(img, 1, (0, 1))
    energyMap = np.rot90(energyMap, 1, (0, 1))
    img, _ = crop_c(img, energyMap, scale_r)
    img = np.rot90(img, 3, (0, 1))
    return img

def main():

    if len(sys.argv) != 5:
        print('\nusage: seam_carving.py <scale_columns> <scale_rows> <image_in> <image_out>')
        sys.exit(1)

    scale_c = float(sys.argv[1])
    scale_r = float(sys.argv[2])
    in_filename = sys.argv[3]
    out_filename = sys.argv[4]

    img = imread(in_filename)
    energyMap = calc_energy(img)#matriz de mapa energetico

    imwrite('ene.jpg', energyMap)

    outc, energyMap = crop_c(img, energyMap, scale_c)
    imwrite('ene2.jpg', energyMap)
    imwrite('ene3.jpg', outc)
    outr = crop_r(outc, energyMap, scale_r)
    imwrite(out_filename, outr)

if __name__ == '__main__':
    main()