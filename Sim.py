import numpy as np
import matplotlib.pyplot as plt
from helpers import CalculateBER, CountCorrected, RandomBits, PlotTrellis
from Encoder import ConvolutionalEncoder
from ViterbiDecoder import ViterbiDecoder
from channel import Channel

from BlockEncoder import BlockEncoder
from BlockDecoder import BlockDecoder



def TestEncodeDecode(InputBits, TestName):
    polynomials = ['111', '101']
    c_encoder = ConvolutionalEncoder(3, polynomials)
    c_decoder = ViterbiDecoder(3, [int(poly, 2) for poly in polynomials])

    b_encoder = BlockEncoder(3, polynomials)
    b_decoder = BlockDecoder(3, [int(poly, 2) for poly in polynomials])

    c_EncodedBits = c_encoder.encode(InputBits)
    c_DecodedBits, c_TrellisData, c_MLP  = c_decoder.decode(''.join(map(str, c_EncodedBits)))

    b_EncodedBits = b_encoder.encode(InputBits)
    b_DecodedBits, b_TrellisData, b_MLP  = b_decoder.decode(''.join(map(str, b_EncodedBits)))

    print(f"Input Bits: {InputBits}")
    print(f"Convolutional - Encoded Bits: {c_EncodedBits}")
    print(f"Convolutional - Decoded Bits: {c_DecodedBits}\n")
    print(f"Block - Encoded Bits: {b_EncodedBits}")
    print(f"Block - Decoded Bits: {b_DecodedBits}\n")
    
    assert ''.join(map(str, c_DecodedBits)) == ''.join(map(str, InputBits)), f"Test failed (convolutional): {TestName} - Input: {InputBits}, Decoded: {c_DecodedBits}" #convo code check
    assert ''.join(map(str, b_DecodedBits)) == ''.join(map(str, InputBits)), f"Test failed (block): {TestName} - Input: {InputBits}, Decoded: {b_DecodedBits}" #block code check
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
    
    c_encoder = ConvolutionalEncoder(3, polynomials)
    c_decoder = ViterbiDecoder(3, [int(poly, 2) for poly in polynomials])
    b_encoder = BlockEncoder(3, polynomials)
    b_decoder = BlockDecoder(3, [int(poly, 2) for poly in polynomials])
    channel = Channel(SNRdB)

    # Encoding
    c_EncodedBits = c_encoder.encode(InputBits)
    c_SignalStr = str(np.array(c_EncodedBits)[()])
    c_signal = np.array(list(map(int, c_SignalStr)), dtype=int)
    b_EncodedBits = b_encoder.encode(InputBits)
    b_SignalStr = str(np.array(b_EncodedBits)[()])
    b_signal = np.array(list(map(int, b_SignalStr)), dtype=int)
    
    
    # Transmit 
    c_ReceivedBits = channel.transmit(c_signal)
    c_ReceivedBits = ''.join(map(str, c_ReceivedBits))
    b_ReceivedBits = channel.transmit(b_signal)
    b_ReceivedBits = ''.join(map(str, b_ReceivedBits))
    
    # Decoding
    c_DecodedBits, c_TrellisData, c_MLP = c_decoder.decode(c_ReceivedBits)
    c_DecodedBits = np.array(list(map(int, c_DecodedBits)), dtype=int)
    b_DecodedBits, b_TrellisData, b_MLP = b_decoder.decode(b_ReceivedBits)
    b_DecodedBits = np.array(list(map(int, b_DecodedBits)), dtype=int)
    
    #BER and number of corrected errors
    c_ber = CalculateBER(InputBits, c_DecodedBits)
    print(f"Bit Error Rate (BER) for a sequence of {BitLength} bits at SNR {SNRdB} dB (Convolutional Method): {c_ber}")
    c_CorrectedErrors = CountCorrected(InputBits, np.array(list(map(int, c_ReceivedBits)), dtype=int), c_DecodedBits)
    print(f"Number of corrected errors (Convolutional Method): {c_CorrectedErrors}")
    b_ber = CalculateBER(InputBits, b_DecodedBits)
    print(f"Bit Error Rate (BER) for a sequence of {BitLength} bits at SNR {SNRdB} dB (Convolutional Method): {b_ber}")
    b_CorrectedErrors = CountCorrected(InputBits, np.array(list(map(int, b_ReceivedBits)), dtype=int), b_DecodedBits)
    print(f"Number of corrected errors: {b_CorrectedErrors}")

    c_states = 1 << (c_decoder.constraint - 1)
    c_bitnum = len(c_ReceivedBits) // len(c_decoder.polynomials)
    PlotTrellis(c_TrellisData, c_states, c_bitnum, True, c_MLP)
    b_states = 1 << (b_decoder.constraint - 1)
    b_bitnum = len(b_ReceivedBits) // len(b_decoder.polynomials)
    PlotTrellis(b_TrellisData, b_states, b_bitnum, True, b_MLP)

    #plots BER vs SNR - still need to modify for block code   
    SNRs = np.arange(-20, 25, 2)
    c_bers = []
    b_bers = []
    for snr in SNRs:
        
        c_encoder = ConvolutionalEncoder(3, polynomials)
        b_encoder = BlockEncoder(3, polynomials)
        c_decoder = ViterbiDecoder(3, [int(poly, 2) for poly in polynomials])
        b_decoder = BlockDecoder(3, [int(poly, 2) for poly in polynomials])
        channel = Channel(snr)
        c_EncodedBits = c_encoder.encode(InputBits)
        b_EncodedBits = b_encoder.encode(InputBits)
        c_SignalStr = str(np.array(c_EncodedBits)[()])
        b_SignalStr = str(np.array(b_EncodedBits)[()])
        c_signal = np.array(list(map(int, c_SignalStr)), dtype=int)
        b_signal = np.array(list(map(int, b_SignalStr)), dtype=int)
        c_ReceivedBits = channel.transmit(c_signal)
        b_ReceivedBits = channel.transmit(b_signal)
        c_ReceivedBits = ''.join(map(str, c_ReceivedBits))
        b_ReceivedBits = ''.join(map(str, b_ReceivedBits))
        c_DecodedBits, c_TrellisData, c_MLP = c_decoder.decode(c_ReceivedBits)
        b_DecodedBits, b_TrellisData, b_MLP = b_decoder.decode(b_ReceivedBits)
        c_DecodedBits = np.array(list(map(int, c_DecodedBits)), dtype=int)
        b_DecodedBits = np.array(list(map(int, b_DecodedBits)), dtype=int)
        
        c_ber = CalculateBER(InputBits, c_DecodedBits)
        b_ber = CalculateBER(InputBits, b_DecodedBits)
        c_CorrectedErrors = CountCorrected(InputBits, np.array(list(map(int, c_ReceivedBits)), dtype=int), c_DecodedBits)
        b_CorrectedErrors = CountCorrected(InputBits, np.array(list(map(int, b_ReceivedBits)), dtype=int), b_DecodedBits)
        c_bers.append(c_ber)
        b_bers.append(b_ber)
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(SNRs, c_bers, 'o-', label='BER vs SNR')
    plt.title('BER vs SNR Performance (Convolutional)')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.grid(True, which='both')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.semilogy(SNRs, b_bers, 'o-', label='BER vs SNR')
    plt.title('BER vs SNR Performance (Block)')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.grid(True, which='both')
    plt.legend()
    plt.show()

        
    

if __name__ == "__main__":
    main()


