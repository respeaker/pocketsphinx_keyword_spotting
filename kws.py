#!/usr/bin/python

import sys, os
from pocketsphinx.pocketsphinx import Decoder
import pyaudio


script_dir = os.path.dirname(os.path.realpath(__file__))


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string("-logfn", os.devnull)
config.set_string('-hmm', os.path.join(script_dir, 'model/hmm/en'))
config.set_string('-dict', os.path.join(script_dir, 'model/keywords_en.dic'))
if True:
    config.set_string('-kws', os.path.join(script_dir, 'model/keywords_en.txt'))
else:
    config.set_string('-keyphrase', 'miss j')
    config.set_float('-kws_threshold', 1e-15)

# Process audio chunk by chunk. On keyword detected perform action and restart search
decoder = Decoder(config)
decoder.start_utt()


stream = None
if len(sys.argv) > 1:
    stream = open(sys.argv[1], "rb")
else:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()


print('start...')

while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break

    hypothesis = decoder.hyp()
    if hypothesis:
        print('\nhypothesis: %s, score: %d' % (hypothesis.hypstr, hypothesis.best_score))
        print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
        print ("Detected keyword, restarting search")
        os.system('mpg123 ' + os.path.join(script_dir, 'hi.mp3'))

        print('restart...')
        decoder.end_utt()
        decoder.start_utt()
        print('ok')
        # break

stream.close()
