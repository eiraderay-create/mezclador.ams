import streamlit as st
st.set_page_config(page_title="AMS COLOR Mixer",layout="wide")
_cl=lambda x:(x.strip().replace(" ","") if x.strip().replace(" ","").startswith('#') else '#'+x.strip().replace(" ",""))[:7].upper()
def _hr(x):
 try:
  h=x.lstrip('#');return tuple(int(h[i:i+2],16) for i in (0,2,4)) if len(h)==6 else (255,255,255)
 except:return (255,255,255)
_rh=lambda x:'#%02x%02x%02x'%x
def _tx(_t):
 _v=[x/255 for x in _t];_k=1-max(_v);_w=min(_v)
 if _k<1:_a=(1-_v[0]-_k)/(1-_k);_s=(1-_v[1]-_k)/(1-_k);_d=(1-_v[2]-_k)/(1-_k)
 else:_a=_s=_d=0
 _q=_a+_s+_d+_k+_w
 return [round((x/_q)*4,1) if _q>0 else 0 for x in [_a,_s,_d,_k,_w]]
def _ax(_tr,_fc,_nf):
 _v=[0.0]*len(_fc)
 for _ in range(_nf):
  _bi,_md=0,9e9
  for _i in range(len(_fc)):
   _tv=list(_v);_tv[_i]+=1.0;_sv=sum(_tv)
   _re=tuple(int(sum(_fc[j][k]*_tv[j] for j in range(len(_fc)))/_sv) for k in range(3))
   _dist=sum((_tr[k]-_re[k])**2 for k in range(3))
   if _dist<_md:_md,_bi=_dist,_i
  _v[_bi]+=1.0
 return [int(x) for x in _v]
if 'ini' not in st.session_state:
 st.session_state.ini=True;st.session_state.n_f=4;st.session_state.p_tgt="#60A26A"
 _df=["#FFFFFF","#00FFFF","#000000","#FFFF00","#FF0000","#00FF00","#0000FF","#FF00FF","#808080","#A52A2A"]
 for i in range(10):
  st.session_state[f"p_{i}"]=_df[i];st.session_state[f"t_{i}"]=_df[i];st.session_state[f"n_{i}"]=1.0 if i==0 else 0.0
def _sk(i):st.session_state[f"t_{i}"]=st.session_state[f"p_{i}"].upper()
def _st(i):st.session_state[f"p_{i}"]=_cl(st.session_state[f"t_{i}"])
st.markdown("""<style>.block-container{max-width:1000px;margin:auto;padding-top:2rem;}.btn-kofi{display:inline-block;background-color:#9b59b6;color:white!important;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold;width:100%;text-align:center;animation:p 2s infinite;}@keyframes p{0%{transform:scale(1);}70%{transform:scale(1.02);}100%{transform:scale(1);}}.theory-box{height:30px;width:30px;border-radius:6px;border:1px solid #ccc;margin:0 auto;}</style>""",unsafe_allow_html=True)
with st.sidebar:
 st.header("⚙️ Settings")
 st.number_input("Filament Count",1,10,key="n_f")
 if st.button("♻️ Reset All",use_container_width=True):
  for k in list(st.session_state.keys()):del st.session_state[k]
  st.rerun()
 st.divider()
 st.markdown('<a href="https://ko-fi.com/D1D41Y3WLU" target="_blank" class="btn-kofi">☕ Support Project</a>',unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>🎯 TARGET COLOR</h2>",unsafe_allow_html=True)
_,_cc,_=st.columns([1,1.2,1])
with _cc:
 st.color_picker("C",key="p_tgt",on_change=_sk,args=("tgt",),label_visibility="collapsed")
 st.text_input("H",key="t_tgt",on_change=_st,args=("tgt",),label_visibility="collapsed")
 st.markdown(f"<div style='height:100px;border-radius:15px;border:3px solid white;background:{st.session_state.p_tgt};'></div>",unsafe_allow_html=True)
 _tr=_hr(st.session_state.p_tgt)
st.divider();st.header("1. Your Filaments")
_fc,_vr=[],[]
_tp=sum(st.session_state[f"n_{j}"] for j in range(st.session_state.n_f))
for i in range(st.session_state.n_f):
 if i%2==0:_clm=st.columns(2)
 with _clm[i%2]:
  _c1,_c2=st.columns([1,2.5])
  with _c1:
   st.markdown(f"<div style='height:45px;border-radius:8px;border:1px solid #ddd;background:{st.session_state[f'p_{i}']};'></div>",unsafe_allow_html=True)
   st.color_picker(f"P{i}",key=f"p_{i}",on_change=_sk,args=(i,),label_visibility="collapsed")
  with _c2:
   st.text_input(f"T{i}",key=f"t_{i}",on_change=_st,args=(i,),label_visibility="collapsed")
   _pct=round((st.session_state[f'n_{i}']/_tp*100),1) if _tp>0 else 0
   st.number_input(f"Parts (Share: {_pct}%)",0.0,100.0,key=f"n_{i}",step=1.0)
  _fc.append(_hr(st.session_state[f"p_{i}"]));_vr.append(st.session_state[f"n_{i}"])
st.divider();st.header("✨ Inventory Suggestion")
_sg=_ax(_tr,_fc,st.session_state.n_f);_stt=sum(_sg);_cs=st.columns(st.session_state.n_f if st.session_state.n_f>0 else 1)
for i in range(st.session_state.n_f):
 with _cs[i]:
  st.markdown(f"<div class='theory-box' style='background:{st.session_state[f'p_{i}']};'></div>",unsafe_allow_html=True)
  st.markdown(f"<p style='text-align:center;font-weight:bold;margin-bottom:0;'>{_sg[i]} P ({round((_sg[i]/_stt*100),1) if _stt>0 else 0}%)</p>",unsafe_allow_html=True)
st.divider();st.header("2. Final Comparison")
_stot=sum(_vr);_res=tuple(int(sum(_fc[i][j]*_vr[i] for i in range(len(_fc)))/(_stot if _stot>0 else 1)) for j in range(3));_rhx=_rh(_res)
_ca,_cb=st.columns(2)
_ca.markdown(f"<div style='height:80px;border-radius:10px;background:{st.session_state.p_tgt};text-align:center;padding-top:25px;color:white;font-weight:bold;border:2px solid #ddd;'>Target: {st.session_state.p_tgt}</div>",unsafe_allow_html=True)
_cb.markdown(f"<div style='height:80px;border-radius:10px;background:{_rhx};text-align:center;padding-top:25px;color:white;font-weight:bold;border:2px solid #ddd;'>Mix: {_rhx}</div>",unsafe_allow_html=True)
st.divider();st.header("🏆 The Winner Mix (CMYKW)")
_pv=_tx(_tr);_pt=sum(_pv);_tc=[("#00FFFF","Cyan"),("#FF00FF","Magenta"),("#FFFF00","Yellow"),("#000000","Black"),("#FFFFFF","White")];_tcc=st.columns(5)
for i,(_c,_n) in enumerate(_tc):
 with _tcc[i]:
  st.markdown(f"<div style='height:35px;width:35px;border-radius:8px;background:{_c};margin:0 auto;border:1px solid #ccc;'></div>",unsafe_allow_html=True)
  st.markdown(f"<p style='text-align:center;margin-bottom:0;'><b>{_pv[i]} P ({round((_pv[i]/_pt*100),1) if _pt>0 else 0}%)</b></p>",unsafe_allow_html=True)
  st.caption(f"<p style='text-align:center;'>{_n}<br>{_c}</p>",unsafe_allow_html=True)
