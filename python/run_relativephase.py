import numpy as np
import scipy.signal
import share, mfcc, phase
#from matplotlib.pyplot import *
import os,sys
from os.path import *
from multiprocessing import Pool

cfg={}
####### config parameters #######
cfg['samplerate']  = 16000
cfg['frameshift']  = 0.005  * cfg['samplerate']
cfg['windowsize']  = 0.0125 * cfg['samplerate']
cfg['nfft']        = 256
cfg['sync']        = True
cfg['numChannels'] = 59
cfg['nbands']      = 8
cfg['basefreq']    = 1000
#################################

dataroot  = '/Work19/2017/liumeng/Antispoof/baseline_CM/wav/'
outroot   = '/Work19/2017/liumeng/Antispoof/baseline_CM/feature/'

if not exists(outroot):
  os.makedirs(outroot)

############## make targetfile list  ###################
filelist=[]
for dpath, dnames, fnames in os.walk(dataroot):
  for fname in fnames:
    if splitext(fname)[1]=='.wav':
      filelist.append(join(dpath,fname))

if not exists(outroot):
  os.makedirs(outroot)


def extract(infile):
  outfile = join(outroot, os.path.basename(infile).replace('.wav', '.mfc'))
  print(infile,'->',outfile)
  if not exists(dirname(outfile)):
    os.makedirs(dirname(outfile))
  signal = share.wavread(infile)
  audio  = signal[0]
  p      = phase.phase(audio, cfg)
  pn     = phase.normalize(p, cfg)
  pnsm   = phase.melfilterbank(np.sin(pn), cfg)
  pncm   = phase.melfilterbank(np.cos(pn), cfg)
  return np.hstack([pncm, pnsm])

  
for file in filelist:
  extract(file)
  
#p = Pool(16)
#p.map(extract, filelist)



















