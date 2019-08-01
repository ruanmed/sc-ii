np = [1]
dp = conv([1 6],[1 10])
Gp = tf(np,dp)
figure(1)
rlocus(Gp)
nc = [1 6*1.05] %anular o polo em 6
dc = [1 0]
Gc = tf(nc,dc)
figure(2)
rlocus(Gc*Gp)
%Gma = 110*Gc*Gp %ts = 0.8s mp = 20%
%Gma = 24*Gc*Gp  %ts = 1.1s mp = 0%
k = 38
Gma = k*Gc*Gp  %ts = 0.58s mp = 2%
figure(3)
bode(Gma)
%FzdB = 3.58
FzdB = 3.89
T = 0.15/FzdB
Gmf = Gma/(1+Gma)
figure(4)
step(Gmf)
grid
%Gz = c2d(Gc*Gp,T,'tustin')
Gcz = c2d(38*Gc,T,'tustin')
Gpz = c2d(Gp,T,'tustin')
Gz = Gcz*Gpz
%Gz = c2d(Gc*Gp,T)
figure(5)
rlocus(Gz)
Gfz = Gz/(1+Gz)
figure(6)
step(Gfz)
