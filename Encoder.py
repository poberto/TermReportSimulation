from helpers import InitOutputs

#convolutional encoder class
class ConvolutionalEncoder:
    def __init__(self, constraint, polynomials):
        self.constraint = constraint
        self.polynomials = [int(p, 2) for p in polynomials]
        self.outputs = []
        InitOutputs(self)

    #calculates next state based on current state and input
    def NextState(self, CurrentState, input):
        return (CurrentState >> 1) | (input << (self.constraint - 2))

    #encodes the input bits
    def encode(self, bits):
        state = 0
        encoded = ""
        for bit in bits:
            InputBit = int(bit)
            encoded += format(self.outputs[state | (InputBit << (self.constraint - 1))], f'0{len(self.polynomials)}b')
            state = self.NextState(state, InputBit)
        return encoded
