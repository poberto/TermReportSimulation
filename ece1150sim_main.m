%Block-Code Simulation
%Lillian Jones

valVec = [2, 4, 8, 16, 32, 64]; %Vector to hold the length of the binary string for each iteration
for i = 1:6
    tic;
    lenMessage = valVec(i); %Generate a random length for the binary message (Between 2-4)
    numParity = 0; %Number of parity bits is initialized as 0
    while(2^numParity < lenMessage + numParity + 1) %Follow the equation for finding the number of parity bits
           numParity = numParity + 1;
    end
    dataStr = randi([0 1], lenMessage, 1); %Create a random binary string that is the length of the message
    disp("Data string prior to transmission:");
    disp(dataStr);
    lenWithParity = lenMessage + numParity;
    
    %----Call encoding function----
    encodedVec = encoder(dataStr, numParity, lenMessage);
    
    %----Insert random error into the encoded data string----
    encodedVec = flip(encodedVec, 1);
    indRandom = randi([1, lenWithParity]); %Select a random bit to produce an error
    
    if(encodedVec(indRandom) == 1) %Swap whatever the bit value at the specified index is
        encodedVec(indRandom) = 0;
    else
        encodedVec(indRandom) = 1;
    end
    encodedVec = flip(encodedVec, 1);
    
    %----Begin decoding----
    errorSpace = decoder(encodedVec);
    if(errorSpace == 0)
        disp("No error occurred.");
    else
        disp("The error occured at the following index in the encoded data:");
        disp(errorSpace);
    end
    
    encodedVec = flip(encodedVec, 1);
    if(encodedVec(errorSpace) == 0)
        encodedVec(errorSpace) = 1;
    else
        encodedVec(errorSpace) = 0;
    end
    encodedVec = flip(encodedVec, 1);
    
    tempLen = size(encodedVec); %Decoder must first determine the length of the received data
    lenOfRecData = tempLen(1, 1); %Extract number of elements from returned array
    recParity = 0; %Find received number of parity bits (Re-use of code from above)
    while(2^recParity < lenOfRecData + 1) %Follow the equation for finding the number of parity bits...
           recParity = recParity + 1; %... needed for a message of a specific length
    end
    lenMessage = lenOfRecData - recParity;
    
    encodedVec = flip(encodedVec, 1); %Reverse the data string to make it easier to index
    j = 0; %Iterators
    t = 1;
    dataVec = zeros(lenMessage, 1); %Reserve space to hold the encoded data bits
    
    for i = 1:lenOfRecData %Iterate through all of the received data
        if(i == 2^j) %If the bit index is a power of two, it is a parity bit, so do not add it to the data
            j = j + 1; %Increment the parity number
            continue; %Move to the next iteration
        else
            dataVec(t) = encodedVec(i); %Otherwise, add the data bit to the data vector
            t = t + 1; %Increment
        end
    end
    dataVec = flip(dataVec, 1);
    disp("The decoded and corrected message is:");
    disp(dataVec);
    toc;
    disp("----");
end




