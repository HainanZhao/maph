# C59 idea selection: exact Pólya multiplier

The full Gram route is deferred because the pinned environment has no SDP
solver and an arbitrary sparse Gram restriction would not test its stated
claim. Choose instead the exact Pólya family: factor the S3 3-cycle smoothing
deficit as ​\((u-v)^2R(x,y,u,v)\), then test coefficientwise positivity of
\((x+y+u+v)^K R\) for frozen \(0\le K\le24\). A pass is a continuous S3
certificate; a cap failure rejects only this multiplier family.
