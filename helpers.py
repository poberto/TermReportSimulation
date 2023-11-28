import numpy as np
import random
import matplotlib.pyplot as plt

# calculates Hamming Distance
def HammingDistance(x, y):
    assert len(x) == len(y)
    distance = 0
    for i in range(len(x)):
        if x[i] != '-' and y[i] != '-':
            distance += x[i] != y[i]
    return distance

#calculates output bits for each state
def InitOutputs(self):
    self.outputs = [0] * (1 << self.constraint)
    for i in range(len(self.outputs)):
        for j, polynomial in enumerate(self.polynomials):
            reversed_polynomial = ReverseBits(self.constraint, polynomial)
            input = i
            output = 0
            for k in range(self.constraint):
                output ^= (input & 1) & (reversed_polynomial & 1)
                reversed_polynomial >>= 1
                input >>= 1
            self.outputs[i] += output << j


#reverses bit order
def ReverseBits(bitnum, input):
    output = 0
    while bitnum > 0:
        output = (output << 1) + (input & 1)
        input >>= 1
        bitnum -= 1
    return output

# counts number of errors corrected 
def CountCorrected(InputBits, RecievedBits, DecodedBits):
    num_corrected_errors = sum(i != r and i == d for i, r, d in zip(InputBits, RecievedBits, DecodedBits))
    return num_corrected_errors

#calculates bit errro rate
def CalculateBER(InputBits, DecodedBits):
    errors = sum(i != d for i, d in zip(InputBits, DecodedBits))
    return errors / len(InputBits)

#generates random bit string
def RandomBits(length):
    return [random.randint(0, 1) for _ in range(length)]

#plits the trellis diagram of the decoder and highlights the most likely path(MLP)
def PlotTrellis(trellis_data, states, bitnum, isConvolutional, MLP=None):
    plt.figure(figsize=(12, 8))

    for bit in range(bitnum):
        for state in range(states):
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
    if(isConvolutional):
        plt.title('Trellis Diagram (Convolutional)')
    else:
        plt.title('Trellis Diagram (Block)')
    plt.xlabel('Time Step')
    plt.ylabel('State')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    