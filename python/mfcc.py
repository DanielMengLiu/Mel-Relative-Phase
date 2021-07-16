import numpy as np
import scipy.fftpack.realtransforms
import RP.share as share 

def hz2mel(f):
    return 1127.01048 * np.log(f / 700.0 + 1.0) ## mel scale
    #return 0.355 * f ## linear scale

def mel2hz(m):
    return 700.0 * (np.exp(m / 1127.01048) - 1.0) ## mel scale
    #return m/0.355 ## linear scale
    
def melFilterBank(fs, nfft, numChannels):
    fmax = fs / 2
    melmax = hz2mel(fmax)
    nmax = nfft / 2
    df = fs / nfft
    dmel = melmax / (numChannels + 1)
    melcenters = np.arange(1, numChannels + 1) * dmel
    fcenters = []
    for mc in melcenters:
        fcenters.append(mel2hz(mc))

    #fcenters = mel2hz(melcenters)
    indexcenter = []
    for fc in fcenters:
        indexcenter.append(np.round(fc / df))
    indexstart = np.hstack(([0], indexcenter[0:numChannels - 1]))
    indexstop = np.hstack((indexcenter[1:numChannels], [nmax]))
    filterbank = np.zeros((numChannels, int(nmax)))
    for c in np.arange(0, numChannels):
        if indexcenter[c] - indexstart[c] != 0:
            increment= 1.0 / (indexcenter[c] - indexstart[c])
        for i in np.arange(indexstart[c], indexcenter[c]):
            filterbank[c, int(i)] = (int(i) - indexstart[c]) * increment
        if indexstop[c] - indexcenter[c] != 0:
            decrement = 1.0 / (indexstop[c] - indexcenter[c])
        for i in np.arange(indexcenter[c], indexstop[c]):
            filterbank[c, int(i)] = 1.0 - ((int(i) - indexcenter[c]) * decrement)
    return filterbank, fcenters

def mfcc(signal, cfg):
    signal = share.preEmphasis(signal, 0.97)
    filterbank, fcenters = melFilterBank(cfg['samplerate'], cfg['nfft'], cfg['numChannels'])
    frames = share.enframe(signal, cfg)

    mfc=[]
    for frame in frames:
      spec = np.abs(np.fft.fft(frame, cfg['nfft']))[:cfg['nfft']/2]
      melspec = np.log10(np.dot(spec, filterbank.T))
      ceps = scipy.fftpack.realtransforms.dct(melspec, type=2, norm="ortho", axis=-1)
      mfc.append(ceps[:cfg['nceps']])
    return np.array(mfc)



