%Short fill rule set.

1 {fillHit(k, T+16) : time(T)} 4. 
1 {fillHit(s, T+16) : time(T)} 4.

2 {fillHit(h, T+16) : oddSH(T)} 2.

:- fillHit(k, T), fillHit(s, T).
