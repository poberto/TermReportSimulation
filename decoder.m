function [erSpace] = decoder(encStr)

tempLen = size(encStr); %Decoder must first determine the length of the received data
lenOfRecData = tempLen(1, 1); %Extract number of elements from returned array
recParity = 0; %Find received number of parity bits (Re-use of code from above)
while(2^recParity < lenOfRecData + 1) %Follow the equation for finding the number of parity bits...
       recParity = recParity + 1; %... needed for a message of a specific length
end

encStr = flip(encStr, 1); %Reverse the data string to make it easier to index
% j = 0; %Iterators
% t = 1;
% dataVec = zeros(lenMessage, 1); %Reserve space to hold the encoded data bits
% 
% for i = 1:lenOfRecData %Iterate through all of the received data
%     if(i == 2^j) %If the bit index is a power of two, it is a parity bit, so do not add it to the data
%         j = j + 1; %Increment the parity number
%         continue; %Move to the next iteration
%     else
%         dataVec(t) = encStr(i); %Otherwise, add the data bit to the data vector
%         t = t + 1; %Increment
%     end
% end
% dataVec = flip(dataVec, 1);
%----
parVec = zeros(recParity, 1); %Reserve memory for a vector holding the sum of the parity values
for i = 1:recParity %For each parity value:
    tempPar = 0; %Follow the algorithm for determining the value of parity bits
    for j = 1:lenOfRecData %Iterate through the entire message (With bits reserved for parity)
        tempStr = flip(transpose(dec2bin(j, recParity))); %Convert the index to a binary string, and reverse the string to ease indexing
        if(tempStr(i) == '1') %If the parity bit-number index of the binary string is "1", count it towards the parity of the bit
            tempPar = tempPar + encStr(j);
        end
    end
    parVec(i) = tempPar; %Append to vector holding the sum of the parity
end

finalString = "";
for i = 1:recParity %Assign value according to even-parity:
    if(rem(parVec(i), 2) == 0 || parVec(i)==0)
        finalString = finalString + '0';
    else
        finalString = finalString + '1';
    end
end
erSpace = bin2dec(reverse(finalString));
