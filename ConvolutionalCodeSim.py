import numpy as np
import matplotlib.pyplot as plt
from helpers import CalculateBER, CountCorrected, RandomBits, PlotTrellis
from Encoder import ConvolutionalEncoder
from ViterbiDecoder import ViterbiDecoder
from channel import Channel


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
    SNRs = np.arange(0, 10, 0.5)
    
    BERscoded = []  # BER values with convolutional coding
    BERsuncoded = []  # BER values without convolutional coding

    for snr in SNRs:
        
        encoder = ConvolutionalEncoder(3, polynomials)
        decoder = ViterbiDecoder(3, [int(poly, 2) for poly in polynomials])
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
        BERscoded.append(ber)
        
        #without Convolutional Coding
        signal = InputBits
        ReceivedBitsUncoded = channel.transmit(signal)
        BERsuncoded.append(CalculateBER(InputBits, ReceivedBitsUncoded))

    
    plt.figure(figsize=(10, 6))
    plt.semilogy(SNRs, BERscoded, 'o-', label='BER with Convolutional Coding')
    plt.semilogy(SNRs, BERsuncoded, 'o-', label='BER without Convolutional Coding')
    plt.title('BER vs SNR Comparison')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.grid(True, which='both')
    plt.legend()
    plt.show()
        
    

if __name__ == "__main__":
    main()


