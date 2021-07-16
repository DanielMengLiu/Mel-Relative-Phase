import numpy as np
import scipy.signal
import struct
import wave
import audioop
from matplotlib.pyplot import *

def rawread(infilename):
  data=np.memmap(infilename, dtype='int16', mode='r')
  return data.newbyteorder()/32768.0

def rawwrite(data, outfilename):
  out=np.memmap(outfilename, dtype='int16', mode='w+', shape=(1,len(data)))
  out[:]=(data*32768)[:]
  out[:]=out.newbyteorder()[:]

#---------------------------------------
#    function : read wave file
# Input arguments
#   -infilename : input filename
# Output arguments
#   -data       : normalized wave data
#   -param      : wave parameters
#---------------------------------------
def wavread(infilename):
  wav   = wave.open(infilename, "r")
  param = wav.getparams()
  x     = wav.readframes(wav.getnframes())
  data  = np.frombuffer(x, dtype = "int16")/32768.0  # normalization to (-1,1)
  #time = linspace(0.0, len(data)/fs, len(data))
  wav.close()
  return data, param

#---------------------------------------
#    function : write wave file
# Input arguments
#   -data        : wave data to write
#   -outfilename : output filename
#   -param       : wave parameters
#---------------------------------------
def wavwrite(data, outfilename, param):
  wav  = wave.open(outfilename, "w")
  wav.setparams(param)
  wav.writeframes(np.int16(data*32768).tostring())
  wav.close()

def preEmphasis(signal, p):
  return scipy.signal.lfilter([1.0, -p], 1, signal)

def enframe(signal, cfg):
  #numframes = int(len(signal)*float(1.0)/frameshift+float(0.5))
  windowsize = cfg['windowsize']
  frameshift = cfg['frameshift']
  numframes  = int(1+((len(signal)-windowsize)/frameshift))
  frameshift = int(frameshift)
  window     = np.hamming(windowsize)
  frames     = []
  for i in range(numframes):
    framestart = i*frameshift
    frameend   = framestart + windowsize
    frames.append(signal[framestart:frameend]*window)
  return np.array(frames)

def enframe_sync(signal, cfg):
  #numframes = int(len(signal)*float(1.0)/frameshift+float(0.5))
  windowsize = cfg['windowsize']
  frameshift = cfg['frameshift']
  numframes  = int(1+((len(signal)-windowsize)/frameshift))
  frameshift = int(frameshift)
  window     = np.hamming(windowsize)
  shift      = int(frameshift/2)
  frames     = []
  for i in range(numframes):
    framestart = i*frameshift
    frameend   = framestart + windowsize
    center = framestart+windowsize/2
    dif = np.argmax(signal[int(center-shift):int(center+shift)])-shift
    if framestart+dif < 0 or frameend+dif > len(signal):
      dif = 0
    frames.append(signal[framestart+dif:int(frameend)+dif]*window)
  return np.array(frames)

def simple_vad(framedata, cfg):
  powers = [np.sum(x*x) for x in framedata]
  threshold = sorted(powers, reverse=True)[int(len(framedata)*cfg['vadrate'])]
  vad = [1 if x>threshold else 0 for x in powers]
  return vad

def splice(framedata, n_context):
  out = []
  for i in range(len(framedata)):
    if i-n_context < 0:
      out.append(np.r_[np.zeros(len(framedata[0])*(n_context-i)), np.hstack(framedata[:i+n_context+1])])
    elif i+n_context >= len(framedata):
      out.append(np.r_[np.hstack(framedata[i-n_context:]), np.zeros(len(framedata[0])*(i+n_context+1-len(framedata)))])
    else:
      out.append(np.hstack(framedata[i-n_context:i+n_context+1]))
  return np.array(out)



def concatenate(frameddata, cfg):
  print(np.shape(frameddata))
  numsample = cfg['frameshift']*len(frameddata)+cfg['windowsize']
  outdata = np.zeros(numsample)
  framestart = 0
  frameend   = cfg['windowsize']
  window     = np.hamming(cfg['windowsize'])
  for frame in frameddata:
    outdata[framestart:frameend] += np.array(frame)
    framestart += cfg['frameshift']
    frameend += cfg['frameshift']
  return outdata

def join_magphase(mag, pha):
  out = []
  for i in range(len(mag)):
    out.append(mag[i]*np.cos(pha[i])+1j*mag[i]*np.sin(pha[i]))
  return np.array(out)

def mirror(spec):
  return np.hstack([spec, spec.T[::-1].T])

def delta(frames, deltawindow):
  N_vec, N_cep = np.shape(frames)
  first_vec=frames[0]
  last_vec =frames[-1]
  for i in range(deltawindow):
    frames = np.vstack([first_vec, frames])
    frames = np.vstack([frames   , last_vec])

  i=deltawindow
  delta_coef=np.zeros((N_vec, N_cep))
  for j in np.arange(deltawindow)+1:
    delta_coef += j*(frames[i+j:i+j+N_vec] - frames[i-j:i-j+N_vec])
  delta_coef = delta_coef / sum(np.power(np.arange(deltawindow)+1, 2)) /2
  return np.array(delta_coef)


def writeHTK(data, outfilename):
  shift = 50000
  framebyte = len(data[0])*4
  type = 3014
  #type = 9
  fw=open(outfilename,'wb')
  odata = ""
  odata += struct.pack('>IIHH', len(data), shift, framebyte, type)
  for i in range(len(data)):
   for j in range(len(data[0])):
      odata += struct.pack('>f', data[i][j])
  fw.write(odata)
  fw.close()


def readHTK(infilename):
  fr=open(infilename, 'rb')
  nframes, shift, framebyte, typei = struct.unpack('>IIHH', fr.read(12))
  dim = framebyte/4
  data = struct.unpack('>'+str(dim*nframes)+'f', fr.read())
  fr.close()
  return np.ndarray(shape=(nframes,dim), buffer=np.array(data))

def pasteHTKFeats(infilelist, outfilename):
  feats=[]
  length=[]
  for filename in infilelist:
    feats.append(readHTK(filename))
    length.append(len(feats[-1]))
  outfeat = np.hstack([ x[:np.min(length)] for x in feats])
  writeHTK(outfeat, outfilename)

    

def extractSPHheader(header):
  config={}
  for line in header.split('\n')[2:]:
    if line.find('end_head')>=0:
      break
    name, type, value = line.split()
    if type.find('i')>=0:
      config[name]=int(value)
    if type.find('s')>=0:
      config[name]=value
    if type.find('r')>=0:
      config[name]=float(value)
  return config

def makeSPHheader(conf):
  header="NIST_1A\n1024\n"
  for name in conf.keys():
    header += name
    header += ' '
    if isinstance(conf[name], int):
      header += '-i'
      header += str(len(str(conf[name])))
    if isinstance(conf[name], str):
      header += '-s'
      header += str(len(conf[name]))
    if isinstance(conf[name], float):
      header += '-r'
    header += ' '
    header += str(conf[name])
    header += '\n'
  header += 'end_head\n'
  for i in range(1024-len(header)):
    header += '\n'

  return header

def splitChannel(signal):
  signalA = np.array([signal[i] for i in np.arange(0,len(signal)-1,2)])
  signalB = np.array([signal[i] for i in np.arange(1,len(signal),2)])
  return [signalA, signalB]

def readSPH(infilename):
  fr=open(infilename, 'rb')
  conf = extractSPHheader(fr.read(1024))
  data = audioop.ulaw2lin(fr.read(), 2)
  signal = np.array(struct.unpack('<'+str(len(data)/2)+'h', data))
  if conf['channel_count']==2:
    signal = splitChannel(signal)
  else:
    signal=[signal, []]
  return signal, conf

def writeSPH(signal, conf, outfilename):
  fw=open(outfilename, 'w')
  header = makeSPHheader(conf)
  fw.write(header)
  if conf['sample_coding']=='ulaw':
    data = audioop.lin2ulaw(signal,2)
  fw.write(data)

def writevad(outfilename, vad):
  fw = open(outfilename, 'wb')
  for value in vad:
    fw.write(str(value))
  fw.close()
  

####### config parameters #######
cfg={}
cfg['samplerate'] = 16000
cfg['frameshift'] = 0.005  * cfg['samplerate']
cfg['windowsize'] = 0.025  * cfg['samplerate']
cfg['nfft']       = 512
#cfg['basefreq']   = 1000
cfg['vadrate']    = 0.4

if __name__=='__main__':
  file = '/wanglab/kyoutput/waves/JNAS_multi/3db/duct/F001/NF001002.raw' 
  signal = rawread(file)
 
  frames = enframe(signal, cfg)
  vad = simple_vad(frames, cfg)

  subplot(2,1,1)
  plot(signal)
  subplot(2,1,2)
  ylim(0,1.5)
  plot(vad)
  show()
  writevad('./test.vad', vad)
  #fw = open('./test.vad', 'w')
  #fw.write(str(vad))
  #fw.close()

