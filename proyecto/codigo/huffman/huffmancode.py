#Code based on https://github.com/bhrigu123/huffman-coding
import heapq



class HuffmanCoding:
	def __init__(self):
		""" Constructor de la clase Huffman.
			Recibe como parametro 'path' que es el archivo csv
		"""
		# self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			""" Constructor de la clase HeapNode.
				Recibe como parametro:
					'char' que es el caracter idenficador
					'freq' numero de repeticiones del caracter
			"""
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None
		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other)):
				return False
			return self.freq == other.freq


	# functions for compression:

	def make_frequency_dict(self, text):
			"""Esta funcion recibe como parametro un texto plano.
				Retorna un diccionario donde el 'key' es el caracter y
				'value' equivale a las repeticiones de ese caracter
			"""
			frequency = {}
			#tomamos los numeros como caracteres entonces el diccionario solo tendra un rango (0,9) las ',' y '\n'
			for character in text:#O(len(row)*columns) 
				if not character in frequency:#como frequency es un diccionario es de O(1)
					frequency[character] = 0
				frequency[character] += 1
			
			return frequency

	def make_heap(self, frequency):
			""" Se construye una priority queue, minHeap
				Como parametro recibe el diccionario de frecuencias
			"""


			for key in frequency:
				node = self.HeapNode(key, frequency[key])#instaciamos un nodo con el valor y frecuencia
				heapq.heappush(self.heap, node)#agregamos el nodo al priority queue

	def merge_nodes(self):
			""" Construimos el arbol de huffman.
			"""

			#obtenemos los dos primeros nodos que equivalen a quienes tienen menor frecuencia
			while(len(self.heap)>1):
				node1 = heapq.heappop(self.heap)
				node2 = heapq.heappop(self.heap)

				merged = self.HeapNode(None, node1.freq + node2.freq)#creamos un nodo padre que va a contener los nodos anteriores a la derecha y izquierda
				merged.left = node1
				merged.right = node2

				heapq.heappush(self.heap, merged)#agregamos este nodo al priority queue


	def make_codes_helper(self, root, current_code):
		""" Recorremos el arbol de huffman para asignar el codigo binario a cada caracter
			Parametros:
			'root' -> es la raiz del arbol de huffman
			'current_code' -> Recibe un string vacio. Es el codigo binario q se va formando recursivamente. 
		"""
		if (root == None):
				return
		if(root.char != None):
			self.codes[root.char] = current_code#guardamos el codigo binario en un diccionario
			self.reverse_mapping[current_code] = root.char#guardamos el caracter en un diccionario donde el 'key' sera el codigo binario.
			return

		self.make_codes_helper(root.left, current_code + "0") #avanzamos recursivamente
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		""" Esta funcion utiliza como funcion auxiliar a make_codes_helper 
		"""
		root = heapq.heappop(self.heap)#obtenemos la raiz del arbol
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):

		""" Convierte el texto en codigo binario
			Parametros:
			'text' -> recibe un string que equivale al archivo a comprimir
			
			Retornamos el texto codificado
		"""
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		
		""" Esta funcion se utiliza para hacer que el codigo binario sea multiplo de 8, para asi guardarlo luego como bytes.
			En caso de no ser multiplo de 8 le agregamos '0' al final para forzarlo a ser multiplo de 8.
			Parametros:
				'encoded_text' -> Recibe un string del texto en codigo binario
        """

		extra_padding = 8 - len(encoded_text) % 8#calculmaos cuanto falta por agregar
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)#le agregamos una informacion adicionar la cual utilizaremos despues al comprimir para saber cuantos 0 le agregamos y despues poder eliminarlos
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		"""Parametros:
				'padded_encoded_text' -> Recibe un string del texto en codigo binario ya equilibrado en multiplos de 8
			
			En esta funcion convertimos los bits del string en bytes y lo guardamos, esto con el fin de guardar el tamaño.

			Retorna:
				Retornamos el array de bytes con la informacion comprimida
        """
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self, file):
		""" 
			Esta funcion se encarga de todo el procedimiento para comprimir el archivo del cual ya se guardo el 'path' en el
			init al instancear la clase Huffman. Esta funcion se apoya de otras funciones para hacer el codigo mas facil.

			1. construimos un diccionario de frequencia
			2. construimos un priority queue(usando MinHeap)
			3. Construimos un arbol de Huffman seleccionando dos nodos minimos y juntandolos
			4. Asignamos codigos a cada caracter(recorriendo el arbol desde la raiz)
			5.codificamos el texto de entrada(se reemplaza cada caracter con su respectivo codigo binario)
			6. si la longitud final del codigo binario no es multiplo de 8 agregamos rellono al texto
			7. guardamos la informacion de ese relleno(en 8 bits) al comienzo del todo el texto comprimido
			8. escribimos el resultado a un archivo binario de salida
		"""
		
		text = file.read() 
		text = text.rstrip() #elimina los espacios en blanco del final

		
		frequency = self.make_frequency_dict(text)#obtenemos la frencuencia de cada numero en el texto
		self.make_heap(frequency)
		self.merge_nodes()
		self.make_codes()
		encoded_text = self.get_encoded_text(text)
		padded_encoded_text = self.pad_encoded_text(encoded_text)

		b = self.get_byte_array(padded_encoded_text)

		return b
		


	""" Functions to decompress: """


	def remove_padding(self, padded_encoded_text):
		"""Esta funcion elimina el relleno que añadimos al comprimir para que la codificacion binario 
		fuera multiplo de 8, con esto obtenemos el texto para decodificar
        """
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		""" Parametros: 
			'encoded_text' -> es un string que contiene todo el archivo en binario

			Esta funcion lee los bits y lo reemplaza el codigo de huffman q tenemos en el diccionario por el respectivo
			caracter el cual representa los valores de los pixeles
        """
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, file):
		""" Esta funcion descomprime un archivo binario removiendo el relleno y decodificando el texto binario
		luego guarda la informacion decodificada en un archivo de salida obteniendo la informacion original devuelta
    	"""
		
		bit_string = ""

		byte = file.read(1)
		while(len(byte) > 0):
			byte = ord(byte)
			bits = bin(byte)[2:].rjust(8, '0')
			bit_string += bits
			byte = file.read(1)

		encoded_text = self.remove_padding(bit_string)

		decompressed_text = self.decode_text(encoded_text)
		
		print("Decompressed")
		return decompressed_text


