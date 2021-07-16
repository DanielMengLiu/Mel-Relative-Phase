 % convert mel frequency to linear frequency

function [linear_freq] = mel2linear_sin(mel_freq)

% slow implementation
for i=1:length(mel_freq)
% fast implementation
linear_freq = 700*( 10.^(mel_freq/2595)-1 );    %mel
%linear_freq(i) = 8000-700*(exp((2840-mel_freq(i))/1127)-1);   %imel
%linear_freq = mel_freq/0.355;   %linear

%MidMel
%if mel_freq(i)>=0 & mel_freq(i)<=1420
%    linear_freq(i) = 350*(1-exp((1420-mel_freq(i))/563.5))+4000;      
%elseif mel_freq(i)>1420 & mel_freq(i)<=2850   %+startFrequency
%    linear_freq(i) = 350*(exp((mel_freq(i)-1420)/563.5)-1)+4000;     
%end
%1/3Mel
%if mel_freq(i)>=0 & mel_freq(i)<=2840/3
%  linear_freq(i) = 233.33*(1-exp((946.67-mel_freq(i))/375.67))+2666.67;      
%elseif mel_freq(i)>2840/3 & mel_freq(i)<=2850
%  linear_freq(i) = 466.66*(exp((mel_freq(i)-946.67)/751.33)-1)+2666.67;    
%end

%%n = 7/5;
%%%mel2linear
%%if mel_freq(i)>=0 & mel_freq(i)<=2840/n
%%   linear_freq(i) = 700/n*(1-exp(n/1127*(2840/n-mel_freq(i))))+8000/n;      
%%elseif mel_freq(i)>2840/n & mel_freq(i)<=2850  % should be 2840  but bigger for startmel
%%  linear_freq(i) = (n-1)*700/n*(exp((mel_freq(i)-2840/n)*n/((n-1)*1127))-1)+8000/n;    
%%end


%mel2linear
%if mel_freq(i)>=0 & mel_freq(i)<=591.67
%   linear_freq(i) = mel_freq(i)/0.845;      
%elseif mel_freq(i)>591.67 & mel_freq(i)<=710 
%  linear_freq(i) = (mel_freq(i)-562.0875)/0.0423;  
%elseif mel_freq(i)>710 & mel_freq(i)<=1822.33 
%  linear_freq(i) = (mel_freq(i)+1885.4367)/0.74155; 
%elseif mel_freq(i)>1822.33 & mel_freq(i)<=1964 
%  linear_freq(i) = (mel_freq(i)-1405.6535)/0.0833; 
%elseif mel_freq(i)>1964 % & mel_freq(i)<=2840 
%  linear_freq(i) = (mel_freq(i)+33160/13)/(219/325);   
%end

%mel2linear
%if mel_freq(i)>=0 & mel_freq(i)<=994
%   linear_freq(i) = mel_freq(i)/(994/900);      
%elseif mel_freq(i)>994 & mel_freq(i)<=1207 
%  linear_freq(i) = (mel_freq(i)-(25915/28))/(213/2800);  
%elseif mel_freq(i)>1207 & mel_freq(i)<=1491
%  linear_freq(i) = (mel_freq(i)-(5183/13))/(71/325); 
%elseif mel_freq(i)>1491 & mel_freq(i)<=1562 
%  linear_freq(i) = (mel_freq(i)-(4189/4))/(71/800); 
%elseif mel_freq(i)>1562 & mel_freq(i)<=1988 
%  linear_freq(i) = (mel_freq(i)+(4544/5))/(213/500);   
%elseif mel_freq(i)>1988 & mel_freq(i)<=2059 
%  linear_freq(i) = (mel_freq(i)-(2769/2))/(71/800);   
%elseif mel_freq(i)>2059 & mel_freq(i)<=2840 
%  linear_freq(i) = (mel_freq(i)+12780)/(781/400);   
%end

%mel2linear
%if mel_freq(i)>=0 & mel_freq(i)<=2840*6/23
%   linear_freq(i) = mel_freq(i)/(2840*6/23000);      
%elseif mel_freq(i)>2840*6/23 & mel_freq(i)<=2840 
%  linear_freq(i) = 1000+(4900*(1-exp(23*(2840-mel_freq(i) )/(1127*17)))+56000)/8;  
%end

%mel2linear
%if mel_freq(i)>=0 & mel_freq(i)<=568
%   linear_freq(i) = mel_freq(i)/(568/1500);      
%elseif mel_freq(i)>568 & mel_freq(i)<=2083
%  linear_freq(i) = (mel_freq(i)+(379/2))/(101/200);  
%elseif mel_freq(i)>2083 & mel_freq(i)<=2272
%  linear_freq(i) = (mel_freq(i)-(6631/4))/(189/2000); 
%elseif mel_freq(i)>2272 & mel_freq(i)<=2840
%  linear_freq(i) = (mel_freq(i)+(568/3))/(142/375);  
%end

%mel2linear
%if mel_freq(i)>=0 & mel_freq(i)<=1136
%   linear_freq(i) = mel_freq(i)/(1136/1000);      
%elseif mel_freq(i)>1136 & mel_freq(i)<=1325
%  linear_freq(i) = (mel_freq(i)-(947))/(189/1000);  
%elseif mel_freq(i)>1325 & mel_freq(i)<=2083
%  linear_freq(i) = (mel_freq(i)+(191))/(379/500); 
%elseif mel_freq(i)>2083 & mel_freq(i)<=2272
%  linear_freq(i) = (mel_freq(i)-(1894))/(63/1000);  
%elseif mel_freq(i)>2272 & mel_freq(i)<=2840
%  linear_freq(i) = (mel_freq(i)-(568))/(71/250);  
%end

end
