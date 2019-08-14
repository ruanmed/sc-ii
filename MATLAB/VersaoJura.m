% configuração das figuras
x0=100;
y0=100;
width=550;
height=400;
fontsize=10;


np =[1]
dp = conv([1 6 0],[1 10])
Gp = tf(np,dp)

figure(1)
set(gcf,'position',[x0,y0,width,height])
rlocus(Gp)
title('Lugar das raízes de Gp(s)')
set(gca,'FontSize',fontsize)
saveas(gcf,'f1-rlocus-gp.png')

nc = [1 6.3]
dc = [1 35.57]
Gc = tf(nc,dc)
k = 2459.85 %calculo da condição de módulo
k1 = 1050
G=k*Gc*Gp
gmf = G/(1+G)

figure(2)
set(gcf,'position',[x0,y0,width,height])
rlocus(Gc*Gp)
title('Lugar das raízes de Gp(s)*Gc(s)')
set(gca,'FontSize', fontsize)
saveas(gcf,'f2-rlocus-gp-gc.png')

figure(3)
set(gcf,'position',[x0,y0,width,height])
step(gmf)
title('Resposta ao degrau de G(s)')
set(gca,'FontSize',fontsize)
grid on
grid minor
saveas(gcf,'f3-step-g.png')

figure(4)
set(gcf,'position',[x0,y0,width,height])
bode(G)
title('Diagrama de Bode de G(s)')
set(gca,'FontSize',fontsize)
saveas(gcf,'f4-bode-gs.png')

%T=0.15/7.71
T=0.5/7.71
Gcz =c2d(k*Gc,T,'tustin')
Gpz =c2d(Gp,T,'tustin')
Gz = c2d(G,T,'tustin');
GmfZ = Gz/(1+Gz)

figure(5)
set(gcf,'position',[x0,y0,width,height])
step(GmfZ)
title('Resposta ao degrau de G(z) com k=2459.85')
set(gca,'FontSize',fontsize)
grid on
grid minor
saveas(gcf,'f5-step-gz-k2459.png')

figure(6)
set(gcf,'position',[x0,y0,width,height])
rlocus(Gz)
title('Lugar das raízes de G(z) com k=2459.85')
set(gca,'FontSize',fontsize)
saveas(gcf,'f6-rlocus-gz-k2459.png')

G1=k1*Gc*Gp
gmf1 = G1/(1+G1)

figure(7)
set(gcf,'position',[x0,y0,width,height])
step(gmf1)
title('Resposta ao degrau de G(s) com k=1050')
set(gca,'FontSize',fontsize)
grid on
grid minor
saveas(gcf,'f7-step-gs-k1050.png')

Gz1 = c2d(G1,T,'tustin');
GmfZ1 = Gz1/(1+Gz1)

figure(8)
set(gcf,'position',[x0,y0,width,height])
step(GmfZ1)
title('Resposta ao degrau de G(z) com k=1050')
set(gca,'FontSize',fontsize)
grid on
grid minor
saveas(gcf,'f8-step-gz-k1050.png')


