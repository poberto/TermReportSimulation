#Written by Peter Bertola
import numpy as np
import matplotlib.pyplot as plt
from helpers import CalculateBER, CountCorrected, RandomBits, PlotTrellis
from Encoder import ConvolutionalEncoder
from ViterbiDecoder import ViterbiDecoder
from channel import Channel
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata



#This function is a test function that encodes and decodes a given bit sequence and asserts that the decoded bits match the input
def TestEncodeDecode(InputBits, TestName):
    #defines the polynomials used for encoding and decoding and initializes the encoder and decoder
    polynomials = ['111', '101']
    encoder = ConvolutionalEncoder(3, polynomials)
    decoder = ViterbiDecoder(3, [int(poly, 2) for poly in polynomials])

    #calculates the encoded bits and then decodes them using the encoder and decoder
    EncodedBits = encoder.encode(InputBits)
    DecodedBits, TrellisData, MLP  = decoder.decode(''.join(map(str, EncodedBits)))

    print(f"Input Bits: {InputBits}")
    print(f"Encoded Bits: {EncodedBits}")
    print(f"Decoded Bits: {DecodedBits}\n")
    
    #asserts that the decoded bits match the input
    assert ''.join(map(str, DecodedBits)) == ''.join(map(str, InputBits)), f"Test failed: {TestName} - Input: {InputBits}, Decoded: {DecodedBits}"
    print(f"Test passed: {TestName}")



def main():
    
    #defines Signal to noise ratio and bit length 
    BitLength = 1000
    SNRdB = 20  # Signal-to-Noise Ratio
    InputBits = np.array(RandomBits(BitLength))
    polynomials = ['111', '101']
    
    # Conduct various tests with different input bit sequences to validate the encoder and decoder.
    # These tests cover basic encoding/decoding, handling of different bit patterns, and edge cases.
    TestEncodeDecode([1, 0, 1, 1], "Basic Encoding and Decoding")
    TestEncodeDecode([1, 0, 1, 1], "Basic Encoding and Decoding")
    TestEncodeDecode([1, 1, 0, 0, 1, 1, 0, 1, 0, 1], "Longer Bit Sequence")
    TestEncodeDecode([0, 0, 0, 0, 0], "All Zeros")
    TestEncodeDecode([1, 1, 1, 1, 1], "All Ones")
    TestEncodeDecode([1, 0, 1, 0, 1, 0, 1, 0], "Alternating Bits")
    TestEncodeDecode([1, 0, 0, 1, 1, 0, 1, 0, 0, 1], "Random Bit Sequence")
    TestEncodeDecode([1], "Single Bit - 1")
    TestEncodeDecode([0], "Single Bit - 0")
    TestEncodeDecode([], "Empty Sequence")
    TestEncodeDecode([1, 1, 0, 0, 1, 1, 0, 0], "Sequence with Repeating Patterns")
    TestEncodeDecode([0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1], "Long Random Sequence")
    TestEncodeDecode([0, 1, 0, 0, 0, 0, 0, 0], "Sequence with Single Alternation")
    TestEncodeDecode([1, 0, 1, 0, 0, 1, 0, 1], "Sequence with Multiple Alternations")
    TestEncodeDecode([0, 0, 0, 0, 0, 0, 0, 1], "Long Sequence of Zeros with One One")
    TestEncodeDecode([0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1,
           0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0,
           1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1,
           1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0,
           0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0,
           1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0,
           0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1,
           1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1,
           0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
           1, 1],'testsnr')
    
    # Initialize the encoder, decoder, and channel with the given parameters.
    encoder = ConvolutionalEncoder(3, polynomials)
    decoder = ViterbiDecoder(3, [int(poly, 2) for poly in polynomials])
    channel = Channel(SNRdB)

    # Encoding
    EncodedBits = encoder.encode(InputBits)
    SignalStr = str(np.array(EncodedBits)[()])
    signal = np.array(list(map(int, SignalStr)), dtype=int)
    
    
    # Transmit 
    ReceivedBits = channel.transmit(signal)
    ReceivedBits = ''.join(map(str, ReceivedBits))
    
    # Decoding
    DecodedBits, TrellisData, MLP = decoder.decode(ReceivedBits)
    DecodedBits = np.array(list(map(int, DecodedBits)), dtype=int)
    
    #BER and number of corrected errors
    ber = CalculateBER(InputBits, DecodedBits)
    print(f"Bit Error Rate (BER) for a sequence of {BitLength} bits at SNR {SNRdB} dB: {ber}")
    
    CorrectedErrors = CountCorrected(InputBits, np.array(list(map(int, ReceivedBits)), dtype=int), DecodedBits)
    print(f"Number of corrected errors: {CorrectedErrors}")


    states = 1 << (decoder.constraint - 1)
    bitnum = len(ReceivedBits) // len(decoder.polynomials)
    PlotTrellis(TrellisData, states, bitnum, MLP)



    #plots BER vs SNR    
    SNRs = np.arange(0, 5, 0.5)
    
    polynomial_sets = {'Rate 1/2, Constraint Length 3': ['111', '101'],  # Two polynomials of length 3
    'Rate 1/3, Constraint Length 3': ['111', '101', '110'],  # Three polynomials of length 3
    'Rate 1/2, Constraint Length 4': ['1111', '1011'],  # Two polynomials of length 4
}
    BERscoded = {scenario: [] for scenario in polynomial_sets} # BER values with convolutional coding
    BERsuncoded = []  # BER values without convolutional coding

    for snr in SNRs:
        
        for scenario, polys in polynomial_sets.items():
            K = len(polys[0])
            CodeRate = 1/len(polys)
            
            encoder = ConvolutionalEncoder(K, polys)
            decoder = ViterbiDecoder(K, [int(poly, 2) for poly in polys])
            channel = Channel(snr)
            EncodedBits = encoder.encode(InputBits)
            SignalStr = str(np.array(EncodedBits)[()])
            signal = np.array(list(map(int, SignalStr)), dtype=int)
            ReceivedBits = channel.transmit(signal)
            ReceivedBits = ''.join(map(str, ReceivedBits))
            DecodedBits, TrellisData, MLP = decoder.decode(ReceivedBits)
            DecodedBits = np.array(list(map(int, DecodedBits)), dtype=int)
            
            ber = CalculateBER(InputBits, DecodedBits)
            CorrectedErrors = CountCorrected(InputBits, np.array(list(map(int, ReceivedBits)), dtype=int), DecodedBits)
            BERscoded[scenario].append(CalculateBER(InputBits, DecodedBits))
            
        #without Convolutional Coding
        signal = InputBits
        ReceivedBitsUncoded = channel.transmit(signal)
        BERsuncoded.append(CalculateBER(InputBits, ReceivedBitsUncoded))

    
    # Plotting BER vs SNR for all scenarios
    plt.figure(figsize=(10, 6))
    for scenario, bers in BERscoded.items():
        plt.semilogy(SNRs, bers, label=f'{scenario}')

    # Include the uncoded scenario in the plot
    plt.semilogy(SNRs, BERsuncoded, label='Uncoded', linestyle='--')

    plt.title('BER vs SNR Comparison')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.grid(True, which='both')
    plt.legend()
    plt.show()
    
    
    #3D plot
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    X, Y, Z = [], [], []
    for scenario, bers in BERscoded.items():
        code_rate = 1 / len(polynomial_sets[scenario])  # Calculate code rate
        X.extend(SNRs)
        Y.extend([code_rate] * len(SNRs))
        Z.extend(bers)
    
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    xi = np.linspace(X.min(), X.max(), 200)
    yi = np.linspace(Y.min(), Y.max(), 200)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate Z values on grid
    zi = griddata((X, Y), Z, (xi, yi), method='cubic')  # Using cubic interpolation

    # Plot the surface
    surf = ax.plot_surface(xi, yi, zi, cmap=plt.cm.coolwarm, linewidth=0, antialiased=False, shade=True)
    ax.contour3D(xi, yi, zi, 50, linestyles="solid", colors='k')
    cset = ax.contourf(xi, yi, zi, zdir='z', offset=zi.min(), cmap=plt.cm.coolwarm, alpha=0.5)
    ax.set_xlabel('SNR (dB)')
    ax.set_ylabel('Code Rate')
    ax.set_zlabel('BER')
    ax.set_title('3D Surface Plot of BER vs SNR and Code Rate')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

    

if __name__ == "__main__":
    main()


