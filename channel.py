#Written by Peter Bertola
import numpy as np
class Channel:
    
    def __init__(self, SNRdB):
        self.SNRdB = SNRdB
        
        
    def transmit(self, signal):
        
        signal = np.where(signal == 0, -1, 1)
        SignalPower = np.mean(np.abs(signal) ** 2)
        LinearSNR = 10 ** (self.SNRdB/ 10)
        NoisePower = (SignalPower / LinearSNR) # Multiplying by a factor for more noise

        # AWGN noise
        noise = np.random.normal(0, np.sqrt(NoisePower), len(signal))

        # Add noise to the signal
        NoisySignal = signal + noise

        # Convert the noisy analog signal back to binary values
        return np.where(NoisySignal < 0, 0, 1)

