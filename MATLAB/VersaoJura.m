np =[1]
dp = conv([1 6 0],[1 10])
Gp = tf(np,dp)
figure(1)
rlocus(Gp)
nc = [1 6.3]
dc = [1 35.57]
Gc = tf(nc,dc)
%k = 2459.85 %calculo da condição de módulo
k = 1100
G=k*Gc*Gp
gmf = G/(1+G)
figure(2)
rlocus(Gc*Gp)
figure(3)
step(gmf)
figure(4)
bode(G)
T=0.15/7.71
Gcz =c2d(k*Gc,T,'tustin')
Gpz =c2d(Gp,T,'tustin')
Gz = c2d(G,T,'tustin');
GmfZ = Gz/(1+Gz)
figure(5)
step(GmfZ)
figure(4)
rlocus(Gz)