# E002-329: exact conditional geometry and optical gauge

RGB forward model: I_j(u)=Q_j{ integral w_j(t)[G_j(t)(K_j*Render(u;r,R,gaze,aperture,optics,reflectance))+B_j(t)]dt+n_j(u)}. The conic analysis assumes instantaneous, fully visible pupil and outer-iris contours. Exposure integration, lighting, eyelid occlusion, glasses and clock error remain separate nuisance factors.

For concentric coplanar circles of radii r,R, C_r=diag(1,1,-r²), C_R=diag(1,1,-R²). Under a shared homography H, both conics transform as H^(-T) C H^(-1). The generalized eigenvalues have a repeated lambda_d and simple lambda_s. Their ratio yields r/R=sqrt(lambda_s/lambda_d), invariant under common projective transformation. Known prior art: Wang, Chern & Alexa (2019), arxiv:1902.04541.

Naive area normalization is not projectively invariant. Under h_k(x,y)=(x/(1+kx),y/(1+kx)), disk area becomes pi*s²/(1-k²*s²)^(3/2). Set rho=r/R, q=kR. The measured square-root area ratio is rho*((1-q²)/(1-q²*rho²))^(3/4). A relative underestimation no greater than delta holds iff |q|<=sqrt((1-(1-delta)^(4/3))/(1-rho²*(1-delta)^(4/3))). For rho=.4, delta=.05, qcritical=.27877880968035884. This is a model parameter, not a gaze angle.

For a pinhole camera, z=(r/R)*(Zi/Zp), where Zp is effective entrance-pupil depth and Zi limbus depth. Unknown differential magnification destroys radius identifiability. Worlds (r,Zp,Zi)=(2/5,10,10) and (1/2,25/2,10) have identical projected pupil and iris circles. A full RGB renderer also generates 11 identical frames for opposite true pupil slopes by varying Zp smoothly by 2/101.

If d=log(z_t/z_0), x=log(r_t/r_0), and |log(m_t/m_0)|<=B independently calibrated, then x lies sharply in [d-B,d+B]. Certify dilation iff d>B, constriction iff d<-B; equality abstains. No bound means no sign certificate. All claims are conditional on the optical model, not measured human physiology.