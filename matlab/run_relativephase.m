function phase = run_relativephase(x,fs)

basefreq = 1000;
nfft = 256;
nfilters = 64;
signal = filter([1 -0.97],1,x); %预加重
frames = enframe(signal,hamming(200,'periodic'),80); %加hamming窗分帧

spec = fft(frames', nfft);
pspec = angle(spec(1:nfft/2,:)); %相位谱
rphase = zeros(size(pspec));

base_bin = round((nfft / fs * basefreq) - 1); %基频对应的fft bin

base_phase = pspec(base_bin+1,:); %base_phase
for cur_frm = 1:size(rphase,2) % current frame
    for cur_bin = 1:size(rphase,1) % current frequency bin
    rphase(cur_bin,cur_frm) = pspec(cur_bin,cur_frm) - (double(cur_bin-1)/double(base_bin) * base_phase(1,cur_frm));
    end
end
%rphase = rphase(:,any(rphase,1)); 

ps = melFilterBank_sin(fs, nfft, nfilters)*sin(rphase);
pc = melFilterBank_cos(fs, nfft, nfilters)*cos(rphase);

phase = cat(1,pc,ps);