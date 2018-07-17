%Long fill rule set.

lf.

0 {fillHit(k, T) : time(T)} 8. 
0 {fillHit(s, T) : time(T)} 8.

4 {fillHit(h, T+16) : oddSH(T)} 4.

:- fillHit(k, T), fillHit(s, T).
%:- fillHit(k, T), chooseHit(s, T).
%:- fillHit(s, T), chooseHit(k, T). 
