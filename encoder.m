function [encStr] = encoder(dataStr, numParity, lenMessage)

lenWithParity = numParity + lenMessage; %Find the total length of the encoded message by adding the number of parity bits to the
%number of data bits

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

%At this point, the encoding string has parity bits reserved at 0's
%The encoded string is reversed, to make indexing easier
%MUST be reversed prior to being passed out of the function

parVec = zeros(numParity, 1); %Reserve memory for a vector holding the sum of the parity values
for i = 1:numParity %For each parity value:
    tempPar = 0; %Follow the algorithm for determining the value of parity bits
    for j = 1:lenWithParity %Iterate through the entire message (With bits reserved for parity)
        tempStr = flip(transpose(dec2bin(j, numParity))); %Convert the index to a binary string, and reverse the string to ease indexing
        if(tempStr(i) == '1') %If the parity bit-number index of the binary string is "1", count it towards the parity of the bit
            tempPar = tempPar + encStr(j);
        end
    end
    parVec(i) = tempPar; %Append to vector holding the sum of the parity
end

for i = 1:numParity %Assign value according to even-parity:
    if(rem(parVec(i), 2) == 0 || parVec(i)==0)
        encStr(2^(i-1)) = 0;
    else
        encStr(2^(i-1)) = 1;
    end
end
encStr = flip(encStr, 1); %Reverse the new array, encoded with parity bits
