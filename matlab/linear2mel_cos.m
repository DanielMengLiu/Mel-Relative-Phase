% convert linear frequency to mel frequency

function [mel_freq] = linear2mel_cos(linear_freq)

for i=1:length(linear_freq)
    mel_freq = 2595*log10(1+linear_freq/700);  %mel 
    %mel_freq(i) = 2840-1127*log(1+(8000-linear_freq(i))/700); %imel
    %mel_freq = 0.355*linear_freq;  %linear
    
    % MidMel  
    %if linear_freq(i)>=0 & linear_freq(i)<=4000
    %  mel_freq(i) = 1420-563.5*log(1+(4000-linear_freq(i))/350);      
    %elseif linear_freq(i)>4000 & linear_freq(i)<=8000
    %   mel_freq(i) = 1420+563.5*log(1+(linear_freq(i)-4000)/350);     
    %end
    % 1/3Mel  
    %if linear_freq(i)>=0 & linear_freq(i)<=8000/3
    %   mel_freq(i) = 946.67-375.67*log(1+(8000-3*linear_freq(i))/700);      
    %elseif linear_freq(i)>8000/3 & linear_freq(i)<=8000
    %   mel_freq(i) = 946.67+751.33*log(1+(3*linear_freq(i)-8000)/1400);    
    %end

%%n = 7/5;
%linear2mel
%%if linear_freq(i)>=0 & linear_freq(i)<=8000/n
%%  mel_freq(i) = 2840/n-1127/n*log(1+(8000-n*linear_freq(i))/700);      
%%elseif linear_freq(i)>8000/n & linear_freq(i)<=8000
%%  mel_freq(i) = 2840/n+1127*(n-1)/n*log(1+(n*linear_freq(i)-8000)/(700*(n-1)));    
%%end

%linear2mel
%if linear_freq(i)>=0 & linear_freq(i)<=700
%  mel_freq(i) =   0.845*linear_freq(i);
%elseif linear_freq(i)>700 & linear_freq(i)<=3500
%  mel_freq(i) = 0.0423*linear_freq(i)+562.0875; 
%elseif linear_freq(i)>3500 & linear_freq(i)<=5000
%  mel_freq(i) = 0.74155*linear_freq(i)-1885.4367; 
%elseif linear_freq(i)>5000 & linear_freq(i)<=6700
%  mel_freq(i) = 0.0833*linear_freq(i)+1405.6535;  
%elseif linear_freq(i)>6700 & linear_freq(i)<=8000
%  mel_freq(i) = (219/325)*linear_freq(i)-33160/13;      
%end

%linear2mel
%if linear_freq(i)>=0 & linear_freq(i)<=900
%  mel_freq(i) =   994/900*linear_freq(i);
%elseif linear_freq(i)>900 & linear_freq(i)<=3700
% mel_freq(i) = 213/2800*linear_freq(i)+25915/28; 
%elseif linear_freq(i)>3700 & linear_freq(i)<=5000
%  mel_freq(i) = 71/325*linear_freq(i)+5183/13; 
%elseif linear_freq(i)>5000 & linear_freq(i)<=5800
%  mel_freq(i) = 71/800*linear_freq(i)+4189/4;  
%elseif linear_freq(i)>5800 & linear_freq(i)<=6800
%  mel_freq(i) = 213/500*linear_freq(i)-4544/5;     
%elseif linear_freq(i)>6800 & linear_freq(i)<=7600
%  mel_freq(i) = 71/800*linear_freq(i)-2769/2; 
%elseif linear_freq(i)>7600 & linear_freq(i)<=8000
%  mel_freq(i) = 781/400*linear_freq(i)-12780;  
%end

%linear2mel   4.01  31.52
%if linear_freq(i)>=0 & linear_freq(i)<=1000
%  mel_freq(i) = 2840*6/23000*linear_freq(i);
%elseif linear_freq(i)>1000 & linear_freq(i)<=8000
% mel_freq(i) = 2840-(17*1127/23)*log(1+(56000-8*(linear_freq(i)-1000))/4900); 
%end

%linear2mel 12.28 0.29
%if linear_freq(i)>=0 & linear_freq(i)<=1500
%  mel_freq(i) =  568/1500*linear_freq(i);
%elseif linear_freq(i)>1500 & linear_freq(i)<=4500
% mel_freq(i) = 101/200*linear_freq(i)-379/2; 
%elseif linear_freq(i)>4500 & linear_freq(i)<=6500
%  mel_freq(i) = 189/2000*linear_freq(i)+6631/4; 
%elseif linear_freq(i)>6500 & linear_freq(i)<=8000
%  mel_freq(i) = 142/375*linear_freq(i)-568/3;  
%end


end
