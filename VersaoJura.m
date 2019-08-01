np =[1]
dp = conv([1 6 0],[1 10])
Gp = tf(np,dp)
figure(8)
rlocus(Gp)
nc = [1 8.269]
dc = [1]
Gc = tf(nc,dc)
k = 67.28
G=k*Gc*Gp
gmf = G/(1+G)
figure(7)
rlocus(Gc*Gp)
figure(1)
step(gmf)
figure(2)
bode(G)
T=0.15/6.67
Gz = c2d(G,T,'tustin')
GmfZ = Gz/(1+Gz)
figure(3)
step(GmfZ)
figure(4)
rlocus(Gz)