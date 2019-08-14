np =[1]
dp = conv([1 6 0],[1 10])
Gp = tf(np,dp)
figure(1)
rlocus(Gp)
title('Lugar das raízes de Gp(s)')
set(gca,'FontSize',18)
nc = [1 6.3]
dc = [1 35.57]
Gc = tf(nc,dc)
k = 2459.85 %calculo da condição de módulo
k1 = 1050
G=k*Gc*Gp
gmf = G/(1+G)
figure(2)
rlocus(Gc*Gp)
title('Lugar das raízes de Gp(s)*Gc(s) k=2459.85')
set(gca,'FontSize',18)
figure(3)
step(gmf)
title('Resposta ao degrau de G(s)')
set(gca,'FontSize',18)
figure(4)
bode(G)
title('Diagrama de Bode de G(s)')
set(gca,'FontSize',18)
%T=0.15/7.71
T=0.5/7.71
Gcz =c2d(k*Gc,T,'tustin')
Gpz =c2d(Gp,T,'tustin')
Gz = c2d(G,T,'tustin');
GmfZ = Gz/(1+Gz)
figure(5)
step(GmfZ)
title('Resposta ao degrau de G(z)k=2459.85')
set(gca,'FontSize',18)
figure(6)
rlocus(Gz)
title('Lugar das raízes de G(z)k=2459.85')
set(gca,'FontSize',18)
G1=k1*Gc*Gp
gmf1 = G1/(1+G1)
figure(7)
step(gmf1)
title('Resposta ao degrau de G(s) k=1050')
Gz1 = c2d(G1,T,'tustin');
GmfZ1 = Gz1/(1+Gz1)
figure(8)
step(GmfZ1)
title('Resposta ao degrau de G(z)k=1050')



