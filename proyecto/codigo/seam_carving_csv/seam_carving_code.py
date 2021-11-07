import sys
import numpy as np
from scipy.ndimage.filters import convolve
import matplotlib
# from matplotlib.image import imsave
from matplotlib import pyplot
import pathlib

# tqdm is not strictly necessary, but it gives us a pretty progress bar
# to visualize progress.
from tqdm import trange

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

    img = img.astype('int')

    energy_map = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    return energy_map

def minimum_seam(energy_map, r, c):

    M = energy_map.copy() #hacemos una copia del mapa de energia
    backtrack = np.zeros_like(M, dtype=int)#creo un array con de la misma dimesion que M y lo lleno de 0

    # Sacamos el valor de arriba hacia abajo minimo para recorrer la matriz y guardamos los valores en M
    # En backtrack guardamos los caminos q debemos tomar para llegar a x valor de la ultima fila de M
    for i in range(1, r):
        for j in range(0, c):
            #Nos aseguramos que no haya un desbordamiento siendo j -1
            if j == 0:
                idx = np.argmin(M[i - 1, j:j + 2]) 
                backtrack[i, j] = idx + j
                min_energy = M[i - 1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack


def carve_column(img, energyMap, r, c):
        
    M, backtrack = minimum_seam(energyMap, r, c)

    # Creamos una matriz r*c donde la llenamos con un valor TRUE y luego cambiamos algunas 
    # posiciones a False que seran los pixeles a eliminar
    mask = np.ones((r, c), dtype=bool)

    # Encuentre la posicion con el menor valor en la ultima fila
    j = np.argmin(M[-1])

    for i in reversed(range(r)): #recorremos la matriz de abajo hacia arriba siguien el camino minimo
        # marcamos el pixel para luego eliminarlo
        mask[i, j] = False
        j = backtrack[i, j]

    #Elimino el borde con menos energia del mapa energetico
    energyMap = energyMap[mask].reshape(r, c - 1)
    # Eliminamos todos los pixeles marcados como falso en mask y luego le hacemos resize a la nueva dimension de la imagen
    img = img[mask].reshape(r, c - 1)

    return img, energyMap

    
def crop_c(img, energyMap, scale_c):    
    r, c = img.shape #image size
    new_c = int(scale_c * c)
    for _ in trange(c - new_c): # tqdm es lo mismo que un range pero sirve para mostrar una barra de carga
        img, energyMap = carve_column(img, energyMap, r, c)
        c = c - 1
    return img, energyMap

def crop_r(img, energyMap, scale_r):
    img = np.rot90(img, 1, (0, 1))
    energyMap = np.rot90(energyMap, 1, (0, 1))
    img, _ = crop_c(img, energyMap, scale_r)
    img = np.rot90(img, 3, (0, 1))
    return img

def seam_carving(csvFile, scale_c, scale_r):
    """
        Esta funcion se encargara de comprimir el archivo con seam_carving
        Parametros:
            'in_filename' -> nombre del directorio q se lee
            'scale_c' -> escala a comprimir en columnas
            'scale_r' -> escala a comprimir en filas
    """
    # matplotlib.image.imsave('ouput.png', csvFile, cmap='gray')
    # image_2 = matplotlib.image.imread('ouput.png')
    # pyplot.imshow(image_2)
    # pyplot.show()

    energy_map = calc_energy(csvFile)
    energy_map_copy = energy_map


    out, energy_map_copy = crop_c(csvFile, energy_map_copy, scale_c)
    out = crop_r(out, energy_map_copy, scale_r)


    # Esto convierte el archivo csv a png, luego lo lee y lo muestra en pantalla
    # matplotlib.image.imsave('output.png', out, cmap='gray')
    # image_1 = matplotlib.image.imread('output.png')
    # pyplot.imshow(image_1)
    # pyplot.show()

    return out, energy_map

# if __name__ == '__main__':
#     main()