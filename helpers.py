import numpy as np
import random
import matplotlib.pyplot as plt

# calculates Hamming Distance
#Hamming diatance is the number of bits in the number that differ freom the expected
#Since this is Hard decision decoding, the branch metric used is the Hamming distance 
def HammingDistance(x, y):
    assert len(x) == len(y)
    distance = 0
    for i in range(len(x)):
        if x[i] != '-' and y[i] != '-':
            distance += x[i] != y[i]
    return distance

#calculates output bits for each state
#This function basically draws the state machine of the encoder so that each output of each possible state is defined when the encoder is initialized
def InitOutputs(self):
    self.outputs = [0] * (1 << self.constraint)
    for i in range(len(self.outputs)):
        for j, polynomial in enumerate(self.polynomials):
            #This reverses the bits of the polynomial so it correctly matches the state machine
            reversed_polynomial = ReverseBits(self.constraint, polynomial)
            input = i
            output = 0
            #This performs the XOR operations accoreding to the encoer's state mechine, defined by the constraint and polynomials
            for k in range(self.constraint):
                output ^= (input & 1) & (reversed_polynomial & 1)
                reversed_polynomial >>= 1
                input >>= 1
            #updates the outputs for this state
            self.outputs[i] += output << j


#reverses bit order. This is needed when tracing backwards through the trellis to find the MLP
def ReverseBits(bitnum, input):
    output = 0
    while bitnum > 0:
        output = (output << 1) + (input & 1)
        input >>= 1
        bitnum -= 1
    return output

# counts number of errors corrected errors by decoder
#finds them by comparing input, recieved, and decoded bits
def CountCorrected(InputBits, RecievedBits, DecodedBits):
    num_corrected_errors = sum(i != r and i == d for i, r, d in zip(InputBits, RecievedBits, DecodedBits))
    return num_corrected_errors

#calculates bit errro rate, the proportion of bits incorrectly decoded
def CalculateBER(InputBits, DecodedBits):
    errors = sum(i != d for i, d in zip(InputBits, DecodedBits))
    return errors / len(InputBits)

#generates random bit string, just used for randomizing input when testing
def RandomBits(length):
    return [random.randint(0, 1) for _ in range(length)]

#plits the trellis diagram of the decoder and highlights the most likely path(MLP)
def PlotTrellis(trellis_data, states, bitnum, MLP=None):
    plt.figure(figsize=(12, 8))

    for bit in range(bitnum):
        for state in range(states):
            #this plots the state transitions at each time step
            NextState = trellis_data[bit * states + state]
            NextBit, NextState = NextState  # Extract individual values
            plt.plot([bit, bit + 1], [state, NextState], marker='s', markersize=11, linestyle='--', linewidth=0.6, color='k')

    #highlights most likesly path
    if MLP is not None:
        for i in range(bitnum - 1):
            CurrentState = MLP[i]
            NextState = MLP[i + 1]
            plt.plot([i, i + 1], [CurrentState, NextState], marker='s', markersize=11, linestyle='-', linewidth=2.5, color='r')

    state_labels = [f'State {i}' for i in range(states)]
    plt.yticks(range(states), state_labels)
    plt.xticks(range(bitnum + 1))
    # if(isConvolutional):
    #     plt.title('Trellis Diagram (Convolutional)')
    # else:
    #     plt.title('Trellis Diagram (Block)')
    plt.xlabel('Time Step')
    plt.ylabel('State')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    