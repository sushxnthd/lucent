"""E002-252: replay unchanged E002-234 estimator on frozen participants."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.path.insert(0,"research/e002-234")
p=Path("research/e002-234/run.py")
b=p.read_bytes()
pin=hashlib.sha1(("blob %d\0"%len(b)).encode()+b).hexdigest()
assert pin=="0af7275f745d65561ffc3c7058bc7ff0cafaf439"
