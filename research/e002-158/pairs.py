import pathlib,hashlib
def matched(z):
 names=z.namelist()
 jpg=[n for n in names if "/fullFrames/" in n and n.lower().endswith((".jpg",".jpeg"))]
 png={pathlib.PurePosixPath(n).stem:n for n in names if "/annotation/png/" in n and n.lower().endswith(".png")}
 a=[(n,png[pathlib.PurePosixPath(n).stem]) for n in jpg if pathlib.PurePosixPath(n).stem in png]
 a.sort(key=lambda t:hashlib.sha256(t[0].encode()).hexdigest())
 return a,{"jpg":len(jpg),"png":len(png),"paired":len(a),"skip":960}
