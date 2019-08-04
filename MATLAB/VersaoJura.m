np =[1]
dp = conv([1 6 0],[1 10])
Gp = tf(np,dp)
figure(1)
rlocus(Gp)
nc = [1 6.3]
dc = [1 35.57]%condição de ângulo
Gc = tf(nc,dc)
%k = 2459.85 %calculo da condi��o de Módulo
k = 1000
G=k*Gc*Gp
gmf = G/(1+G)
figure(2)
rlocus(Gc*Gp)
figure(3)
step(gmf)
figure(4)
bode(G)
T=0.15/7.71
Gcz =c2d(Gc,T,'tustin')
Gpz =c2d(Gp,T,'tustin')
Gz = c2d(G,T,'tustin');
GmfZ = Gz/(1+Gz)
figure(5)
step(GmfZ)
figure(6)
rlocus(Gz)