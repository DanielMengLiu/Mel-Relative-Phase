function [filterbank, fcenters] = melFilterBank(fs, nfft, numChannels)

fmax = fs / 2;
melmax = linear2mel_cos(fmax);
nmax = nfft / 2;
df = fs / nfft;
dmel = melmax / (numChannels + 1);
channels=linspace(1, numChannels,numChannels);
melcenters =  channels * dmel;
fcenters = mel2linear_cos(melcenters);

indexcenter = round(fcenters / df)+1;

indexstart = cat(2,1, indexcenter(1,1:numChannels-1));
indexstop = cat(2,indexcenter(1,2:numChannels), nmax+1);
filterbank = zeros(numChannels, nmax);
for c = linspace(1, numChannels, numChannels)
    increment= 1.0 / (indexcenter(c) - indexstart(c));
    for i = linspace(indexstart(c), indexcenter(c)-1,indexcenter(c)-indexstart(c))
        if indexstart(c) ~= indexcenter(c)
            filterbank(c, i) = (i - indexstart(c)) * increment;
        end
    end
    decrement = 1.0 / (indexstop(c) - indexcenter(c));
    for i = linspace(indexcenter(c), indexstop(c)-1,indexstop(c)-indexcenter(c))
        if indexcenter(c) ~= indexstop(c)
            filterbank(c, i) = 1.0 - ((i - indexcenter(c)) * decrement);
        end
    end
end
    
