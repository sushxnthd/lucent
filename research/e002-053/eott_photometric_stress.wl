(* Lucent E002-053; frozen protocol a1e32a1061d784c293cd0ceba5b26cbf8ca74344e33e602e261f2e8c42c8f533. Development only. *)
ClearAll[rr,num,le,get,eye,analyze,stress,rank,methods,iou,to8];
u="https://webgazer.cs.brown.edu/data/WebGazerETRA2018Dataset_Release20180420.zip";n=21263599023;
rr[a_Integer,b_Integer]:=Module[{r=URLRead[HTTPRequest[u,<|"Headers"->{"Range"->"bytes="<>ToString[a]<>"-"<>ToString[b]}|>]]},If[r["StatusCode"]=!=206,Throw["HTTP range non-206"]];Normal[r["BodyByteArray"]]];
num[a_List,i_Integer,k_Integer]:=FromDigits[Reverse[a[[i;;i+k-1]]],256];
le[x_Integer,k_Integer]:=Reverse[IntegerDigits[x,256,k]];
z=rr[n-450000,n-1];s=FromCharacterCode[z,"ISO8859-1"];
to8[v_]:=Round[255 Clip[v,{0,1}]]/255;
rank[v_]:=Module[{ix=Take[Ordering[MapIndexed[{#1,First[#2]}&,v]],Ceiling[.2 Length[v]]]},Normal[SparseArray[Thread[ix->1],Length[v]]]];
methods[v_]:=Module[{lo=Quantile[v,.1],hi=Quantile[v,.9]},<|"fixed"->(Boole[#<=.14]&/@v),"contrast"->If[hi>lo,(Boole[#<=lo+.25(hi-lo)]&/@v),ConstantArray[0,Length[v]]],"rank"->rank[v]|>];
iou[a_,b_]:=N[Total[Unitize[a*b]]/Max[1,Total[Unitize[a+b]]]];
stress[v_,shape_]:=Module[{w=shape[[2]],x,g1,g2},x=N[Mod[Range[Length[v]]-1,w]/Max[1,w-1]];g1=.75+.5 x;g2=1.25-.5 x;<|"gamma08"->to8[v^.8],"gamma12"->to8[v^1.2],"gain08"->to8[.8v],"gain12"->to8[1.2v],"shade_lr"->to8[v*g1],"shade_rl"->to8[v*g2]|>];
analyze[arr_]:=Module[{shape=Dimensions[arr],v=Flatten[arr],ss,base,other,calc,counts,k,flags},v=to8[v];ss=stress[v,shape];base=methods[v];other=AssociationMap[methods,ss];counts=BinCounts[Round[255v],{0,256,1}];k=Ceiling[.2 Length[v]];
flags=<|"zero_fraction"->N[Count[v,0]/Length[v]],"max_bin_fraction"->N[Max[counts]/Length[v]],"q90_minus_q10"->N[Quantile[v,.9]-Quantile[v,.1]],"rank_boundary_tie_fraction"->N[Count[v,Sort[v][[k]]]/Length[v]]|>;
flags=Join[flags,<|"admissibility_veto"->(flags["zero_fraction"]>=.10||flags["max_bin_fraction"]>=.20||flags["q90_minus_q10"]<.10)|>];
calc[m_]:=Module[{b=base[m],g08=other["gamma08"][m],g12=other["gamma12"][m],l=other["shade_lr"][m],r=other["shade_rl"][m],g8=other["gain08"][m],g12b=other["gain12"][m]},<|"base_fraction"->N[Mean[b]],"gamma_swing"->N[Abs[Mean[g08]-Mean[g12]]],"gain_swing"->N[Abs[Mean[g8]-Mean[g12b]]],"gamma_mean_symdiff"->N[Mean[{Mean[Abs[b-g08]],Mean[Abs[b-g12]]}]],"shade_mean_symdiff"->N[Mean[{Mean[Abs[b-l]],Mean[Abs[b-r]]}]],"shade_min_iou"->Min[iou[b,l],iou[b,r]],"gamma_min_iou"->Min[iou[b,g08],iou[b,g12]]|>];
<|"shape"->shape,"quality"->flags,"methods"->AssociationMap[calc,{"fixed","contrast","rank"}],"histogram256"->counts|>];
eye[g_,q_]:=Module[{xs=q[[All,1]],ys=q[[All,2]],x1,x2,y1,y2},x1=Max[1,Floor[Min[xs]]-4];x2=Min[640,Ceiling[Max[xs]]+4];y1=Max[1,480-Ceiling[Max[ys]]-6];y2=Min[480,480-Floor[Min[ys]]+6];analyze[g[[y1;;y2,x1;;x2]]]];
get[pid_Integer]:=Module[{hits,p,fn,crc,sz,rawsz,method,off,h,datastart,comp,f,lh,cd,eocd,path,st,dest,files,v,im,ff,g},
hits=StringPosition[s,RegularExpression["WebGazerETRA2018Dataset_Release20180420/P_"<>ToString[pid]<>"/[^\\x00-\\x1F]*?\\.webm"]];
If[Length[hits]==0,Return[<|"pid"->pid,"error"->"missing"|>]];
p=First[SortBy[hits,num[z,#[[1]]-46+20,4]&]][[1]]-46;fn=num[z,p+28,2];crc=num[z,p+16,4];sz=num[z,p+20,4];rawsz=num[z,p+24,4];method=num[z,p+10,2];off=num[z,p+46+fn+4,8];h=rr[off,off+29];If[h[[1;;4]]=!={80,75,3,4},Return[<|"pid"->pid,"error"->"bad header"|>]];datastart=off+30+num[h,27,2]+num[h,29,2];comp=rr[datastart,datastart+sz-1];f=ToCharacterCode["clip.webm"];
lh=Join[{80,75,3,4},le[20,2],le[0,2],le[method,2],le[0,2],le[0,2],le[crc,4],le[sz,4],le[rawsz,4],le[Length[f],2],le[0,2],f,comp];
cd=Join[{80,75,1,2},le[20,2],le[20,2],le[0,2],le[method,2],le[0,2],le[0,2],le[crc,4],le[sz,4],le[rawsz,4],le[Length[f],2],le[0,2],le[0,2],le[0,2],le[0,2],le[0,4],le[0,4],f];
eocd=Join[{80,75,5,6},le[0,2],le[0,2],le[1,2],le[1,2],le[Length[cd],4],le[Length[lh],4],le[0,2]];
path=FileNameJoin[{$TemporaryDirectory,"lucent053_"<>ToString[pid]<>".zip"}];st=OpenWrite[path,BinaryFormat->True];BinaryWrite[st,Join[lh,cd,eocd],"Byte"];Close[st];dest=FileNameJoin[{$TemporaryDirectory,"lucent053_"<>ToString[pid]}];If[DirectoryQ[dest],DeleteDirectory[dest,DeleteContents->True]];CreateDirectory[dest];files=Quiet@Check[ExtractArchive[path,dest],$Failed];If[files===$Failed,Return[<|"pid"->pid,"error"->"unzip"|>]];v=Quiet@Check[Import[First[files]],$Failed];If[v===$Failed,Return[<|"pid"->pid,"error"->"video"|>]];im=Quiet@Check[VideoExtractFrames[v,.5],$Failed];If[Head[im]=!=Image,Return[<|"pid"->pid,"error"->"frame"|>]];ff=Quiet@Check[FacialFeatures[im,{"LeftEyePoints","RightEyePoints"}],{}];If[!ListQ[ff]||Length[ff]!=1,Return[<|"pid"->pid,"error"->"face"|>]];g=ImageData[ColorConvert[im,"Grayscale"]];<|"pid"->pid,"crc32"->crc,"compressed_bytes"->sz,"left"->eye[g,ff[[1,"LeftEyePoints"]]],"right"->eye[g,ff[[1,"RightEyePoints"]]]|>];
