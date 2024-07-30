from sdv.single_table import CTGANSynthesizer
synthesizer = CTGANSynthesizer.load('anti_synth.pkl')
print(synthesizer.sample(num_rows=1))

