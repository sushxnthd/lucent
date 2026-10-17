# E002-258 exact aggregate counterexample

Two sessions of two frames. X=(-11,-9,9,11). World A reference Y=(-71,-3,3,71). World B reference Y=(-17,-69,69,17). Both have zero means, sum X^2=404, sum Y^2=10100, sum XY=1616, Pearson r=4/5 and MSE=1818. Each session has Pearson r=+1 in A and -1 in B. Therefore identical participant-level first/second moments do not determine within-session correlation.

For any pooled r strictly between -1 and 1, choose x=(a,b) in between-session/within-session coordinates with a/b>|r|/sqrt(1-r^2). Set y+ = r*x/||x|| + sqrt(1-r^2)*Jx/||x|| and y- = r*x/||x|| - sqrt(1-r^2)*Jx/||x||, J(a,b)=(-b,a). Both have equal norm and inner product with x, but opposite within-session signs. This is elementary covariance geometry, not a new general theorem or an RGB physiological impossibility result.
