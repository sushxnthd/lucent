from shutter_certificate import phase_fraction,qualify_camera

def run():
    def q(f,lo,hi,uniform=True):
        return qualify_camera(F=1/f,w=.01,m=.01,D_lower=lo,D_upper=hi,
                              phase_uniform=uniform,timing_calibrated=True)
    assert abs(q(20,.058,.058).coverage_lower-.96)<1e-12
    assert q(25,.058,.058).guaranteed
    assert q(20,.058,.058,False).decision=='ABSTAIN'
    assert q(25,None,None).decision=='ABSTAIN'
    assert qualify_camera(F=.04,w=.01,m=.01,D_lower=.058,D_upper=.058,
                          phase_uniform=True,timing_calibrated=False).decision=='ABSTAIN'
    assert phase_fraction(.002,.1,.01,.005)==0
    try:q(25,.06,.04)
    except ValueError:pass
    else:raise AssertionError('invalid bounds accepted')
    print('PASS 7 certificate checks')
if __name__=='__main__':run()
