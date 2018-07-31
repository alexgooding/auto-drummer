%Long fill rule set.

0 {fillHit(k, T+16) : time(T)} 8. 
0 {fillHit(s, T+16) : time(T)} 8.

4 {fillHit(h, T+16) : oddSH(T)} 4.

:- fillHit(k, T), fillHit(s, T).
