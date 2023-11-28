from helpers import HammingDistance, InitOutputs
import numpy as np

# Viterbi Decoder class
class ViterbiDecoder:
    def __init__(self, constraint, polynomials, puncpat=""):
        #makes sure polynomials are valid for given constraint length
        assert polynomials
        assert all(0 < p < (1 << constraint) for p in polynomials)
        
        """the constraint length and polynomials are like the ones in the encoder, but instead of a 
        state machine, the decoder will use them to create a "trellis digram" which visualizes all possible state transitions 
        and outputs for each state over time steps. This way the decoder can trace a path through this Trellis to find the most Likely
        sequence"""
        
        self.constraint = constraint
        self.polynomials = polynomials
        
        #unused variable for the puncturing pattern, that would allow for punctured convolutional code.
        self.puncpat = puncpat
        
        #initializes the outputs, which is really like drawing the state diagram for the encoder,
        #to be reffered to and used in later steps.
        self.outputs = []
        InitOutputs(self)

    # calculate and outputs the next state in the trellis based on the current state and input bit
    # This logic used is the same as that in the encoder's state transition diagram
    def NextState(self, CurrentState, input):
        return (CurrentState >> 1) | (input << (self.constraint - 2))

    # This determines the xpected output for a given state and input bit. This refers to the outputs list
    #This is needed for calculating branch metrics in the viterbi alg
    def Output(self, CurrentState, input):
        OutputBits = self.outputs[CurrentState | (input << (self.constraint - 1))]
        return format(OutputBits, f'0{len(self.polynomials)}b')

    #calculates the branch metric. The branch metric is the Hamming Distance between recieved bit and expected output for each state
    #This is basically the error between each possible state and the recieved bits. will be used to calculate the path metric
    def BranchMetric(self, bits, SourceState, TargetState):
            assert len(bits) == len(self.polynomials)
            output = self.Output(SourceState, TargetState >> (self.constraint - 2))
            return HammingDistance(bits, output)

    #calculates the path metric for each state. This is the cumulative cost of the path chosen up to this statein the Trellis,
    #which is basically a sum of branch metrics. Specifically it is found by asdding the branch metric to the previous state's path metric
    def PathMetric(self, bits, prevPathMetrics, state):
        s = (state & ((1 << (self.constraint - 2)) - 1)) << 1
        SourceState1 = s | 0
        SourceState2 = s | 1

        
        #calculates the path metrics for the two possible states and then chooses the 
        #lower cost one, which is the more likely one, then returns it 
        pm1 = prevPathMetrics[SourceState1]
        if pm1 < np.inf:
            pm1 += self.BranchMetric(bits, SourceState1, state)

        pm2 = prevPathMetrics[SourceState2]
        if pm2 < np.inf:
            pm2 += self.BranchMetric(bits, SourceState2, state)

        if pm1 <= pm2:
            return pm1, SourceState1
        else:
            return pm2, SourceState2
    
    #decodes the encoded bits
    def decode(self, bits):
        #initializes trellis and path metrics, the Trellis, as states before, is used to ktrace the best path through the states, which represents the best possible decoded sequence
        trellis = []
        pathmetrics = np.full(1 << (self.constraint - 1), np.inf)
        pathmetrics[0] = 0
        #keeps track of state transitions in the trellis
        StateTransitions = [] 
        
        #iterates over the recieved bits in chunks according to the number of genrator polynomials
        #each chunk corresponds to length of the polynomials, as each set of bits is decoded using entire set of polynomials
        for i in range(0, len(bits), len(self.polynomials)):
            current_bits = bits[i:i + len(self.polynomials)]
            
            #makes new array for updated path metrics of next trellis column
            newPathMetrics = np.full(len(pathmetrics), np.inf)
            #makes new array that will hold the states of the previus column that lead to smallest path metric for each current state
            NewTrellisCol = np.empty(len(pathmetrics), dtype=int)

            
            #calculates new path metric for each state and updates the trellis
            for state in range(len(newPathMetrics)):
                
                #calculates the path metric for this state based on previous states and stores the transition info
                #the transition info will be used at the end to backtrack and trace the most likely path
                newPathMetrics[state], NewTrellisCol[state] = self.PathMetric(current_bits, pathmetrics, state)
                StateTransitions.append((state, NewTrellisCol[state]))  # Store state transition

            #updates the path metrics for the next column   
            pathmetrics = newPathMetrics
            #adds the column to the trellis, tracing another step toeard the final state in the trellis
            trellis.append(NewTrellisCol)
        
        #backtracks through the trellis to find most likely path(MLP)
        #backtracks by starting at lowest path metric final state
        decoded = ""
        state = np.argmin(pathmetrics)
        MLP = []
        
        #works backwards through trellis. decodes the current step by finding most signifigant bit of current state
        #It records the state at each of these steps
        #moves to the previous state using the transition data. 
        #So the algorithm traces its way forward to the most likely final satte, while recording the transitions along the way
        #It then turns backward and traces backward to get the decoded bits from the states, effectively drawing the MLP
        for i in range(len(trellis) - 1, -1, -1):
            decoded += str(state >> (self.constraint - 2))
            MLP.insert(0, state)
            state = trellis[i][state]
        
        
        #this returns the full decoded sequence. the sequence is returned in reverse because it was found backward, decoding the first bit last
        return decoded[::-1], StateTransitions, MLP  # Return the full reversed sequence

