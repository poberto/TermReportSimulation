from helpers import HammingDistance, InitOutputs
import numpy as np

# Viterbi Decoder class
class ViterbiDecoder:
    def __init__(self, constraint, polynomials, puncpat=""):
        assert polynomials
        assert all(0 < p < (1 << constraint) for p in polynomials)
        self.constraint = constraint
        self.polynomials = polynomials
        self.puncpat = puncpat
        self.outputs = []
        InitOutputs(self)

    # outputs next state based on current state and inputs
    def NextState(self, CurrentState, input):
        return (CurrentState >> 1) | (input << (self.constraint - 2))

    # calculates output bits based on current state and input
    def Output(self, CurrentState, input):
        OutputBits = self.outputs[CurrentState | (input << (self.constraint - 1))]
        return format(OutputBits, f'0{len(self.polynomials)}b')

    #calculates the branch metric
    def BranchMetric(self, bits, SourceState, TargetState):
            assert len(bits) == len(self.polynomials)
            output = self.Output(SourceState, TargetState >> (self.constraint - 2))
            return HammingDistance(bits, output)

    #calculates the path metric
    def PathMetric(self, bits, prevPathMetrics, state):
        s = (state & ((1 << (self.constraint - 2)) - 1)) << 1
        SourceState1 = s | 0
        SourceState2 = s | 1

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
        trellis = []
        pathmetrics = np.full(1 << (self.constraint - 1), np.inf)
        pathmetrics[0] = 0
        StateTransitions = [] 
        
        for i in range(0, len(bits), len(self.polynomials)):
            current_bits = bits[i:i + len(self.polynomials)]
            newPathMetrics = np.full(len(pathmetrics), np.inf)
            NewTrellisCol = np.empty(len(pathmetrics), dtype=int)

            for state in range(len(newPathMetrics)):
                newPathMetrics[state], NewTrellisCol[state] = self.PathMetric(current_bits, pathmetrics, state)
                StateTransitions.append((state, NewTrellisCol[state]))  # Store state transition

                
            pathmetrics = newPathMetrics
            trellis.append(NewTrellisCol)

        decoded = ""
        state = np.argmin(pathmetrics)
        MLP = []
        for i in range(len(trellis) - 1, -1, -1):
            decoded += str(state >> (self.constraint - 2))
            MLP.insert(0, state)
            state = trellis[i][state]
        
        

        return decoded[::-1], StateTransitions, MLP  # Return the full reversed sequence

