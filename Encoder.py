#Written by Peter Bertola
from helpers import InitOutputs

#convolutional encoder class
class ConvolutionalEncoder:
    def __init__(self, constraint, polynomials):
        #constraint length of the encoder, the length of the sliding window and number of message bits used for the XOR operations in encoding process
        #Polynomials are generator polynomials that define how the XOR operations on the message bits are performed
        self.constraint = constraint      
        self.polynomials = [int(p, 2) for p in polynomials]
        self.outputs = [] #each state in the encoder's state machine has a unique output, this holds those outputs flor each state
        InitOutputs(self) # This function basically draws the state machine of the encoder so that each output of each possible state is defined when the encoder is initialized
        #each state represents a particular "memory" of previous input bits 

    #calculates next state based on current state and input
    # this function examines the current state and follows the defined state machine of the encoder to the next state 
    def NextState(self, CurrentState, input):
        return (CurrentState >> 1) | (input << (self.constraint - 2))

    #encodes the input bits
    def encode(self, bits):
        #starts here as 0 because there are no previous input bits and initializes a string to hold output bits
        state = 0
        encoded = ""
        
        #iterates over each input bit to encode
        for bit in bits:
            #converts current bit to int 0 or 1 for processing
            InputBit = int(bit)
            
            #The current state and the input bit together decide which output in the list of outputs is used for this input bit
            #The outputs were iriginally defined using the state diagram of the encoder, derived from the polynomials. The length of the output is defined by the number of polynomials
            #each polynomial contributes to one bit of the output.
            encoded += format(self.outputs[state | (InputBit << (self.constraint - 1))], f'0{len(self.polynomials)}b')
            
            #updates the state for the next iteration and input bit
            state = self.NextState(state, InputBit)
            
            #returns the final encoded sequence
        return encoded
