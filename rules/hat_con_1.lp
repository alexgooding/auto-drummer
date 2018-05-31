% The rules associated with mildly constrained hat placement.

%Only even quarter-beat hats placed just before a kick hit.
:- chooseHit(h, 2*T), time(T), not chooseHit(k, 2*T+1).