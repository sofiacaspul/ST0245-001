import sys
import os
import pathlib
import numpy as np
import matplotlib
from matplotlib.image import imsave

from seam_carving_csv.seam_carving_code import seam_carving
# from huffman import huffmancode
from huffman.huffmancode import HuffmanCoding



def main():
    """Esta es la funcion principal, dado que aqui se leen todo los archivos y ya se encarga de comprimir todo y llamar cada metodo y clase
    """
    
    if len(sys.argv) != 6:
        print('\nusage: main.py <path_dir_in> <path_dir_out> <energyPath_out> <scale_columns> <scale_rows>')
        sys.exit(1)

    in_dirPath = sys.argv[1] #nombre del directorio q se lee
    out_dirPath = sys.argv[2] #nombre del directorio q guardamos el resultado comprimido
    outEnergy_path = sys.argv[3] #nombre del directorio donde se veran los mapas de energia
    scale_c = float(sys.argv[4]) #escala a comprimir en columnas
    scale_r = float(sys.argv[5]) #escala a comprimir en filas
    directory = pathlib.Path(in_dirPath)

    for in_filename in directory.iterdir():
        
        #seam carving compress
        csvFile = np.genfromtxt(in_filename, delimiter=',')
        out, energy_map = seam_carving(csvFile, scale_c, scale_r)
        outEnergy_path_temp = outEnergy_path + '\\' +  in_filename.name[:-4] + ".png" #organizamos el path con el mismo nombre del archivo y una extencion png
        imsave(outEnergy_path_temp, energy_map, cmap='gray')
        out_dirPath_temp = out_dirPath + '\\' + in_filename.name
        np.savetxt(out_dirPath_temp, out, delimiter=',', fmt='%d')

        #huffman compress 
        in_filename = out_dirPath_temp
        filename, file_extension = os.path.splitext(in_filename)
        output_path = filename + ".bin"

        #r+ permite leer y escribir - 'wb' permite escribir binario
        file = open(in_filename, 'r+')
        output = open(output_path, 'wb')
        obj = HuffmanCoding()
        b = obj.compress(file)
        output.write(bytes(b))

        print("Compressed file path: " + output_path)

        #descompress 
        input_path = output_path
        filename, file_extension = os.path.splitext(in_filename)
        output_path = filename + "_decompressed" + ".txt"
        file = open(input_path, 'rb') 
        output = open(output_path, 'w')
        decompressed_text = obj.decompress(file)
        output.write(decompressed_text)









main()