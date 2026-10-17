"""E002-252: replay unchanged E002-234 estimator on frozen participants."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.path.insert(0,"research/e002-234")
p=Path("research/e002-234/run.py")
b=p.read_bytes()
pin=hashlib.sha1(("blob %d\0"%len(b)).encode()+b).hexdigest()
assert pin=="0af7275f745d65561ffc3c7058bc7ff0cafaf439"
s=json.loads(Path("research/e002-228/E002_252_SOURCES.json").read_text())
spec=importlib.util.spec_from_file_location("frozen_234",p)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.PINS={person:s[person]["video"]["sha256"] for person in ("P_01","P_02","P_07")}
mod.main()
