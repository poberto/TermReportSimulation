import numpy as np
import matplotlib.pyplot as plt
from helpers import CalculateBER, CountCorrected, RandomBits, PlotTrellis
from Encoder import ConvolutionalEncoder
from ViterbiDecoder import ViterbiDecoder
from channel import Channel



def TestEncodeDecode(InputBits, TestName):
    polynomials = ['111', '101']
    encoder = ConvolutionalEncoder(3, polynomials)
    decoder = ViterbiDecoder(3, [int(poly, 2) for poly in polynomials])

    EncodedBits = encoder.encode(InputBits)
    DecodedBits, TrellisData, MLP  = decoder.decode(''.join(map(str, EncodedBits)))

    print(f"Input Bits: {InputBits}")
    print(f"Encoded Bits: {EncodedBits}")
    print(f"Decoded Bits: {DecodedBits}\n")
    
    assert ''.join(map(str, DecodedBits)) == ''.join(map(str, InputBits)), f"Test failed: {TestName} - Input: {InputBits}, Decoded: {DecodedBits}"
    print(f"Test passed: {TestName}")



def main():
     
    BitLength = 100 
    SNRdB = 20  # Signal-to-Noise Ratio
    InputBits = np.array(RandomBits(BitLength))
    polynomials = ['111', '101']
    
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
    SNRs = np.arange(-20, 25, 2)
    bers = []
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
        bers.append(ber)
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(SNRs, bers, 'o-', label='BER vs SNR')
    plt.title('BER vs SNR Performance')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.grid(True, which='both')
    plt.legend()
    plt.show()

        
    

if __name__ == "__main__":
    main()


