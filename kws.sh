#!/bin/sh

pocketsphinx_continuous -hmm model/hmm/en -dict model/keywords_en.dic -kws model/keywords_en.txt -kws_threshold 1e-20 -inmic yes

