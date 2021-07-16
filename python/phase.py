import numpy as np
import scipy.signal
from scipy.signal import firwin
from scipy.fftpack import fft, ifft
from scipy.fftpack.realtransforms import dct, idct
import RP.share as share
import RP.mfcc as mfcc

def phase(signal, cfg):
  signal = share.preEmphasis(signal, 0.97)
  if cfg['sync']:
    frames = share.enframe_sync(signal, cfg)
  else:
    frames = share.enframe(signal, cfg)

  out=[]
  for frame in frames:
    pspec = np.angle(fft(frame, cfg['nfft'])[:int(cfg['nfft']/2)])
    out.append(pspec)
  return np.array(out)

def normalize(frames, cfg):
  basebin = int(float(cfg['nfft']) / cfg['samplerate'] * cfg['basefreq'])-1
  out=[]
  for frame in frames:
    basephase  = frame[basebin]
    normalized = [frame[i]-float(i)/basebin*basephase  for i in range(len(frame))]
    out.append(normalized)
  return np.array(out) 

def normalize_bin(frames, cfg):
  basebin = cfg['basebin']
  out=[]
  for frame in frames:
    basephase  = frame[basebin]
    normalized = [frame[i]-float(i)/basebin*basephase  for i in range(len(frame))]
    out.append(normalized)
  return np.array(out) 

def normalize_bbb(frames, cfg):
  out = []
  basebins = []
  for n in range(cfg['nbands']):
    basebin = int((n+1)*(float(cfg['nfft'])/cfg['nbands']/2))-1
    for i in range(len(frames[0])/cfg['nbands']):
      basebins.append(basebin)
  for frame in frames:
    normalized = [frame[i]-float(i)/basebins[i]*frame[basebins[i]]  for i in range(len(frame))]
    out.append(normalized)
  return np.array(out)


def melfilterbank(frames, cfg):
  filterbank, fcenters = mfcc.melFilterBank(cfg['samplerate'], cfg['nfft'], cfg['numChannels'])
  out=[]
  for frame in frames:
    melspec = np.dot(frame, filterbank.T)
    out.append(melspec)
  return np.array(out)

def melnormfb(frames, cfg):
  filterbank, fcenters = mfcc.melFilterBank(cfg['samplerate'], cfg['nfft'], cfg['numChannels'])
  out=[]
  basebins=[]
  for i in range(cfg['numChannels']-1):
    basebins.append(int(fcenters[i+1]*cfg['nfft']/cfg['samplerate'])-1)
  basebins.append(cfg['nfft']/2-1)
  for frame in frames:
    tmp_sin=[]
    tmp_cos=[]
    for n in range(cfg['numChannels']):
      normalized = [frame[i]-float(i)/basebins[n]*frame[basebins[n]]  for i in range(len(frame))]
      filtered_sin   = np.dot(np.sin(normalized).T, filterbank[n])
      filtered_cos   = np.dot(np.cos(normalized).T, filterbank[n])
      tmp_sin.append(filtered_sin)
      tmp_cos.append(filtered_cos)
    out.append(np.hstack([tmp_cos,tmp_sin]))
  return np.array(out)

      
def melnormfb_ceps(frames, cfg):
  filterbank, fcenters = mfcc.melFilterBank(cfg['samplerate'], cfg['nfft'], cfg['numChannels'])
  out=[]
  basebins=[]
  for i in range(cfg['numChannels']-1):
    basebins.append(int(fcenters[i+1]*cfg['nfft']/cfg['samplerate'])-1)
  basebins.append(cfg['nfft']/2-1)
  for frame in frames:
    tmp_sin=[]
    tmp_cos=[]
    for n in range(cfg['numChannels']):
      normalized = [frame[i]-float(i)/basebins[n]*frame[basebins[n]]  for i in range(len(frame))]
      filtered_sin   = np.dot(np.sin(normalized).T, filterbank[n])
      filtered_cos   = np.dot(np.cos(normalized).T, filterbank[n])
      tmp_sin.append(filtered_sin)
      tmp_cos.append(filtered_cos)
    out.append(np.hstack([dct(tmp_cos)[:cfg['nceps']],dct(tmp_sin)[:cfg['nceps']]]))
  return np.array(out)


def delta(frames, cfg):
 out=[]
 for p in frames.T:
   out.append(scipy.signal.lfilter([1,-1], 1, p))
 return np.array(out).T

def gd(frames, cfg):
 out=[]
 for p in frames:
   out.append(scipy.signal.lfilter([1,-1], 1, p))
 return np.array(out)

def ceps(frames, cfg):
  out=[]
  for frame in frames:
    ceps = dct(frame, type=2, norm="ortho", axis=-1)
    out.append(ceps[:cfg['nceps']])
  return np.array(out)


if __name__=="__main__":
  signal = share.rawread('NF001002.raw')
  
  

