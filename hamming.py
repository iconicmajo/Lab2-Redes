"""
LABORATORIO 2 - REDES
Maria Jose Castro 181202
Paula Camila Gonzalez 18398
"""
# chequea el numero de paridad de bits en la generacion del hamming code
# devuelve el numero de bits con paridad requeridos para hacerles append a una palabra con el tamaño dado 
def num_parity_bits(nBits):
	i=0
	while 2.**i <= nBits+i: # (potencia de 2 + bits con paridad contados) para cada 4 bits de la palabra se necesitan 3 con paridad
		i+=1
	return i

# genera numero de bits con paridad mientras duelve el numero de paridad en una palabra con tamaño deseado
def num_parity_bits_code(nBits):
	i=0
	while 2.**i <= nBits:
		i+=1

	return i


# devuelve  una lista con la posicion de los bits con paridad que es 0
def append_parity_bits(data):
	n=num_parity_bits(len(data)) #numero de paridad requeridad para la longitud de la data 
	i=0 #contador dle loop
	j=0 #numero de bits con paridad
	k=0 #nuemro de data bits
	parity_list=list()
	while i <n+len(data):
		if i== (2.**j -1):
			parity_list.insert(i,0)
			j+=1
		else:
			parity_list.insert(i,data[k])
			k+=1
		i+=1
	return parity_list


#devuelve lista de hamming codes con paridad par
def hamming_codes(data):
	n=num_parity_bits(len(data))
	parity_par=append_parity_bits(data) # lista de parity bits en posiciones correctas
	i=0 #contador del loop 
	k=1 #2 a la potencia kth parity bit
	while i<n:
		k=2.**i
		j=1
		total=0
		while j*k -1 <len(parity_par):
			if j*k -1 == len(parity_par)-1: #si un indice menos es el ultimo para tomar en cuenta en  la sublista entonces
				lower_index=j*k -1
				temp=parity_par[int(lower_index):len(parity_par)]
			elif (j+1)*k -1>=len(parity_par):
				lower_index=j*k -1
				temp=parity_par[int(lower_index):len(parity_par)] # si el list size es menor que el punto mínimo 
			elif (j+1)*k -1<len(parity_par)-1:
				lower_index=(j*k)-1
				upper_index=(j+1)*k -1
				temp=parity_par[int(lower_index):int(upper_index)]
			
			total=total+sum(int(e) for e in temp) #se suma la sub lista de los parity bits
			print (total,j)
			j+=2 #se incrementan cada dos para ir alternando las parejas de numeros en la list 
		if total%2 >0:
			parity_par[int(k)-1]=1 # chequear paridad impar
			print ("Element is ",parity_par[int(k)-1],k)
		i+=1
	return parity_par

# identifica los parity bits que son incorrectas (impares) 
def hamming_correction(data):
	n=num_parity_bits_code(len(data))
	i=0
	parity_impar_list=list(data)
	print (parity_impar_list)
	errorthBit=0
	while i<n:
		k=2.**i
		j=1
		total=0
		while j*k -1 <len(parity_impar_list):
			if j*k -1 == len(parity_impar_list)-1:
				lower_index=j*k -1
				temp=parity_impar_list[int(lower_index):len(parity_impar_list)]
			elif (j+1)*k -1>=len(parity_impar_list):
				lower_index=j*k -1
				temp=parity_impar_list[int(lower_index):len(parity_impar_list)] #si un indice menos es el ultimo para tomar en cuenta en  la sublista entonces
			elif (j+1)*k -1<len(parity_impar_list)-1:
				lower_index=(j*k)-1
				upper_index=(j+1)*k -1
				temp=parity_impar_list[int(lower_index):int(upper_index)]
			
			total=total+sum(int(e) for e in temp)
			print (total,j)
			j+=2 #se incrementan cada dos para ir alternando las parejas de numeros en la list 
		if total%2 >0:
			errorthBit+=k # se chequea la paridad par sumando todos los items de la lista
		i+=1
	if errorthBit>=1:
		print ("error in ",errorthBit," bit after correction data is " )
		#toggle the corrupted bit
		if parity_impar_list[int(errorthBit-1)]=='0' or parity_impar_list[int(errorthBit-1)]==0:
			parity_impar_list[int(errorthBit-1)]=1
			print(parity_impar_list)
		else:
			parity_impar_list[int(errorthBit-1)]=0
			print(parity_impar_list)
	else:
		print ("No error")
	data_bits_list=list()
	i=0
	j=0
	k=0
	#se devuleve la data ignorando los parity bits
	while i<len(parity_impar_list): 
		if i!= ((2**k)-1):
			temp=parity_impar_list[int(i)]
			data_bits_list.append(temp)
			j+=1
		else:
			k+=1
		i+=1
	return data_bits_list

hamming_correction("11010010")