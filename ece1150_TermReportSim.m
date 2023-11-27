%Block-Code Simulation
%Lillian Jones

lenMessage = randi([2, 4]); %Generate a random length for the binary message
numParity = 0;
while(2^numParity < lenMessage + numParity + 1) %Follow the equation for finding the number of parity bits...
       numParity=numParity+1; %... needed for a message of a specific length
end
lenWithParity = numParity + lenMessage; %Add the number of parity bits to the number of data bits to find the total length of the encoded message
dataStr = randi([0 1], lenMessage, 1); %Create a random binary string that is the length of the message

disp("Original string of data prior to encoding:");
disp(dataStr);

%----------BEGIN ENCODER HERE----------:
i = 1; %Iterator
expVal = 0; %Value of the exponent - Will eventally equal the number of parity bits
tempInd = lenMessage; %Used to iterate through the data string backwards when appending to the encoding string

encStr = zeros(lenWithParity, 1);

while(i<=lenWithParity)
    if(i == 2^expVal)
        encStr(i) = 0; %Insert a parity bit if the index is a power of 2
        expVal = expVal + 1; %Iterate the exponent value to begin checking for the next power of 2
    else
        encStr(i) = dataStr(tempInd); %If a parity bit is not needed at this index, append the data from the end of the original string
        tempInd = tempInd-1; %Decrement the data index
    end
    i = i + 1; %Increment
end

%At this point, parity bits are reserved, but not yet set
parVec = zeros(numParity, 1); %Reserve memory for a vector holding the sum of the parity values
for i = 1:numParity %For each parity value:
    tempPar = 0; %Follow the algorithm for determining the value of parity bits
    for j = 1:lenWithParity
        tempStr = transpose(dec2bin(j, numParity));
        if(tempStr(i) == '1')
            tempPar = tempPar + encStr(j);
        end
    end
    parVec(i) = tempPar;
end
parVec = flip(parVec, 1);

for i = 1:numParity %Assign value according to even-parity:
    if(rem(parVec(i), 2) == 0 || parVec(i) == 0)
        encStr(2^(i-1)) = 0;
    else
        encStr(2^(i-1)) = 1;
    end
end
encStr = flip(encStr, 1); %Reverse the new array with reserved parity bits
%----------END ENCODER HERE----------

%Now, a bit error must be randomly added to the string of encoded data
encStr = flip(encStr, 1);
indRandom = randi([1, lenWithParity]); %Select a random bit to produce an error
if(encStr(indRandom) == 1) %Swap whatever the bit value at the specified index is
    encStr(indRandom) = 0;
else
    encStr(indRandom) = 1;
end
encStr = flip(encStr, 1);
disp(encStr);

%----------BEGIN DECODER HERE----------
tempLen = size(encStr); %Decoder must first determine the length of the received data
lenOfRecData = tempLen(1, 1); %Extract number of elements from returned array
recParity = 0; %Find received number of parity bits (Re-use of code from above)

while(2^recParity < lenOfRecData + 1) %Follow the equation for finding the number of parity bits...
       recParity = recParity + 1; %... needed for a message of a specific length
end

encStr = flip(encStr, 1); %Reverse the data string to make it easier to index
j = 0; %Iterators
t = 1;
dataVec = zeros((lenOfRecData-recParity), 1); %Reserve space to hold the encoded data bits

for i = 1:lenOfRecData %Iterate through all of the received data
    if(i == 2^j) %If the bit index is a power of two, it is a parity bit, so do not add it to the data
        j = j + 1; %Increment the parity number
        continue; %Move to the next iteration
    else
        dataVec(t) = encStr(i); %Otherwise, add the data bit to the data vector
        t = t + 1; %Increment
    end
end
dataVec = flip(dataVec, 1);


%Find the parity bits of the newly-extracted data bits:
i = 1; %Iterator
expVal = 0; %Value of the exponent - Will eventally equal the number of parity bits
tempInd = lenMessage; %Used to iterate through the data string backwards when appending to the encoding string

encFin = zeros(lenWithParity, 1);

while(i<=lenWithParity)
    if(i == 2^expVal)
        encFin(i) = 0; %Insert a parity bit if the index is a power of 2
        expVal = expVal + 1; %Iterate the exponent value to begin checking for the next power of 2
    else
        encFin(i) = dataVec(tempInd); %If a parity bit is not needed at this index, append the data from the end of the original string
        tempInd = tempInd-1; %Decrement the data index
    end
    i = i + 1; %Increment
end
% disp(dataVec);
% disp(encFin);

%At this point, parity bits are reserved, but not yet set
parVec = zeros(numParity, 1); %Reserve memory for a vector holding the sum of the parity values
for i = 1:numParity %For each parity value:
    tempPar = 0; %Follow the algorithm for determining the value of parity bits
    for j = 1:lenWithParity
        tempStr = transpose(dec2bin(j, numParity));
        if(tempStr(i) == '1')
            tempPar = tempPar + encFin(j);
        end
    end
    parVec(i) = tempPar;
end
parVec = flip(parVec, 1);

for i = 1:numParity %Assign value according to even-parity:
    if(rem(parVec(i), 2) == 0 || parVec(i) == 0)
        encFin(2^(i-1)) = 0;
    else
        encFin(2^(i-1)) = 1;
    end
end
encStr = flip(encStr, 1);

finalString = "";
for i = 1:numParity
    finalString = finalString + int2str(encFin(2^(i-1)));
end
finalString = reverse(finalString);
erSpace = bin2dec(finalString);






