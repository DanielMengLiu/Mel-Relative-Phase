import numpy as np
import share, phase
import sys, os
from os.path import *
from multiprocessing import Pool, cpu_count

cfg={}
#############  config parameters  ###############
cfg['samplerate'] = 16000
cfg['frameshift'] = 0.005   * cfg['samplerate']
cfg['windowsize'] = 0.0125  * cfg['samplerate']
cfg['nfft']       = 256
cfg['sync']       = True
cfg['basefreq']   = 1000


########################### USAGE ##############################
#                                                              #
# $python pcm2phase.py /example/input/dir /example/output/dir  #
#                                                              #
#  This script extracts phase features from all of raw audio   #
# files in the input directry by pararell processing. And all  #
# output files are stored into the output directry.            #
#                                                              #
#                     !! caution !!                            #
#     Input files must be "raw" type in big endian, int16.     #
#    If you'd like to change this, fix share.py for your       #
#    audio format, or fix the format by "sox" command.         #
#                                                              #
#                                                              #
#                     REQUIREMENTS                             #
#                        python >= 2.7                         #
#                        numpy, scipy                          #
#                                                              #
################################################################


indir  = sys.argv[1]
outdir = sys.argv[2]

def extract(file):
  ## Setting input/output filename ##
  infilename  = join(indir, file)
  outfilename = join(outdir, file.replace('.raw', '.mfc'))
  print 'output:', outfilename

  ## Signal processing part ##
  signal = share.rawread(infilename)
  p      = phase.phase(signal, cfg)
  pn     = phase.normalize(p, cfg)
  outvec = np.hstack([np.cos(pn).T[1:13].T, np.sin(pn).T[1:13].T])

  ## Write to HTK format file ##
  share.writeHTK(outvec, outfilename)


## Making input raw filelist ##
filelist = []
for file in os.listdir(indir):
  if splitext(file)[1]=='.raw':
    filelist.append(file)


## Pararell processing by Pool module ##
p = Pool(10)               # set the pararell number
p.map(extract, filelist)   # Do feature extraction


