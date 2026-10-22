"""Synthetic-only quotient separation certificate."""
def qualify(rho,A,b,eps,calibrated=False):
 if min(rho,A,b,eps)<0 or rho>1 or A>1:raise ValueError('invalid bounds')
 margin=rho*A-2*b-4*eps
 return {'status':'CERTIFY' if calibrated and margin>0 else 'ABSTAIN','margin':margin,'human_validated':False}
if __name__=='__main__':
 assert qualify(.1,.6,.009,.01,True)['status']=='CERTIFY'
 assert qualify(.1,.6,.01,.01,True)['status']=='ABSTAIN'
 assert qualify(.1,.6,.009,.01)['status']=='ABSTAIN'
 print('PASS')
