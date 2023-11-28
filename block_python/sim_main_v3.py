# Block-Code Simulation, coverted into Python
# Jeremy Love

import numpy as np

# encoder implementation
def encoder(dataStr, numParity, lenMessage) :
	
	lenWithParity = numParity + lenMessage
	
	i = 0
	expVal = 0
	tempInd = lenMessage
	
	encStr = np.zeros(lenWithParity)
	
	while i < lenWithParity :
		if i == 2 ** expVal :
			encStr[i] = 0
			expVal += 1
		else :
			encStr[i] = dataStr[tempInd - 1]
			tempInd -= 1
		i += 1
	
	parVec = np.zeros(numParity)
	
	for i in range(1, numParity + 1) :
	#for i in range(1, numParity + 1) :
		tempPar = 0
		for k in range(1, lenWithParity + 1) :
		#for k in range(1, lenWithParity + 1) :
			tempStr = np.flip(np.binary_repr(k, width=numParity))
			if tempStr[i] == '1' :
				tempPar += encStr[k]
				
		parVec[i] = tempPar
		
	for i in range(1, numParity + 1) :
		if parVec[i] % 2 == 0 or parVec[i] == 0 :
			encStr[2 ** (i - 1)] = 0
		else :
			encStr[2 ** (i - 1)] = 1
			
	encStr = np.flip(encStr)
	return encStr

# decoder implementation
def decoder(encStr) :
	
	tempLen = len(encStr)
	lenOfRecData = tempLen
	recParity = 0
	
	while 2 ** recParity < lenOfRecData + 1 :
		recParity += 1
		
	encStr = np.flip(encStr)
	parVec = np.zeros(recParity)
	
	for i in range(1, recParity + 1) :
		tempPar = 0
		for k in range(1, lenOfRecData + 1) :
			tempStr = np.flip(np.binary_repr(k, width=recParity))
			if tempStr[i] == '1' :
				tempPar += encStr[k]
		parVec[i] = tempPar
		
	finalString = ""
	
	for i in range(1, recParity + 1) :
		if parVec[i] % 2 == 0 or parVec[i] == 0 :
			finalString += '0'
		else:
			finalString += '1'

	erSpace = int(finalString[::-1], 2)
	return erSpace

# simulation implementation
def sim_main_v3() :
	lenMessage = np.random.randint(2, 8)
	numParity = 0
	
	while 2 ** numParity < lenMessage + numParity + 1 :
		numParity += 1
		
	dataStr = np.random.randint(2, size = lenMessage)
	print("Data string prior to transmission:")
	print(dataStr)
	lenWithParity = lenMessage + numParity
	
	# call encoder
	encodedVec = encoder(dataStr, numParity, lenMessage)
	
	# insert error
	encodedVec = np.flip(encodedVec)
	indRandom = np.random.randint(0, lenWithParity)
	
	if encodedVec[indRandom] == 1 :
		encodedVec[indRandom] = 0
	else :
		encodedVec[indRandom] = 1
		
	encodedVec = np.flip(encodedVec)
	
	# call decoder
	errorSpace = decoder(encodedVec)
	
	if errorSpace == 0 :
		print("No error occurred.")
	else :
		print("The error occurred at the following index in the encoded data:")
		print(errorSpace)
		
	encodedVec = np.flip(encodedVec)
	
	if encodedVec[errorSpace - 1] == 0 :
		encodedVec[errorSpace - 1] = 1
	else :
		encodedVec[errorSpace - 1] = 0
	
	encodedVec = np.flip(encodedVec)

	tempLen = encodedVec.shape
	lenOfRecData = tempLen[0]
	recParity = 0
	while 2 ** recParity < lenOfRecData + 1 :
		recParity = recParity + 1
	lenMessage = lenOfRecData - recParity

	#tempLen = len(encodedVec)
	#lenOfRecData = tempLen - numParity
	
	encodedVec = np.flip(encodedVec)
	k = 0
	t = 0
	dataVec = np.zeros((lenMessage, 1), dtype=int)
	#dataVec = np.zeros(lenOfRecData)
	
	#for i in range(1, tempLen + 1) :
	for i in range(1, lenOfRecData + 1):
		if i == 2 ** k :
			k += 1
			continue
		else :
			dataVec[t] = encodedVec[i - 1]
			t += 1
	
	dataVec = np.flip(dataVec)
	print("The corrected, original message is:")
	print(dataVec)

sim_main_v3()
