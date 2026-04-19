import streamlit as st

# --- 🟢 MOTOR DE CÁLCULO  ---
_cl = lambda x: (x.strip().replace(" ", "") if x.strip().replace(" ", "").startswith('#') else '#'+x.strip().replace(" ", ""))[:7].ljust(7,'0')
_hr = lambda x: tuple(int(x.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
_rh = lambda x: '#%02x%02x%02x' % x

def _tx(_t):
    _v = [x/255 for x in _t]; _k = 1 - max(_v); _w = min(_v)
    if _k < 1: 
        _a=(1-_v[0]-_k)/(1-_k); _s=(1-_v[1]-_k)/(1-_k); _d=(1-_v[2]-_k)/(1-_k)
    else: _a=_s=_d=0
    _q = _a+_s+_d+_k+_w
    return [round((x/_q)*4, 1) if _q>0 else 0 for x in [_a,_s,_d,_k,_w]]

def _ax(_tr, _fcs, _nf):
    _v = [0.0] * len(_fcs)
    for _ in range(_nf):
        _bi, _md = 0, 9e9
        for _i in range(len(_fcs)):
            _tv = list(_v); _tv[_i] += 1.0; _sv = sum(_tv)
            _re = tuple(int(sum(_fcs[j][k]*_tv[j] for j in range(len(_fcs)))/_sv) for k in range(3))
            _dist = sum((_tr[k]-_re[k])**2 for k in range(3))
            if _dist < _md: _md, _bi = _dist, _i
        _v[_bi] += 1.0
    return [int(x) for x in _v]

def _sx(_fc, _vr):
    _st = sum(_vr)
    if _st <= 0: return "#000000"
    return _rh(tuple(int(sum(_fc[i][j] * _vr[i] for i in range(len(_fc))) / _st) for j in range(3)))

# --- 🔵 TRADUCCIONES ---
_D = {
    "Es": {
        "t": "🎨 Mezclador AMS Pro", "p": "⚙️ Configuración", "l": "English (EN)",
        "nf": "Nº Filamentos", "s": "Apoya el proyecto", "r": "1. Tus Filamentos", 
        "am": "✨ Sugerencia con tu inventario", "cm": "2. Comparativa Final", 
        "tl": "Objetivo", "sl": "Tu Mezcla", "th": "🎯 COLOR DESEADO", 
        "mm": "🏆 Combinación Teórica (CMYKW)", "rst": "♻️ Resetear Todo"
    },
    "En": {
        "t": "🎨 AMS Mixer Pro", "p": "⚙️ Settings", "l": "Español (ES)",
        "nf": "Filament Count", "s": "Support the project", "r": "1. Your Filaments", 
        "am": "✨ Inventory Suggestion", "cm": "2. Final Comparison", 
        "tl": "Target", "sl": "Your Mix", "th": "🎯 TARGET COLOR", 
        "mm": "🏆 Theoretical Mix (CMYKW)", "rst": "♻️ Reset All"
    }
}

st.set_page_config(page_title="AMS Mixer Pro", layout="wide")

# --- 🟣 CSS ---
st.markdown("""<style>
    [data-testid="stSidebar"][aria-expanded="true"]{min-width: 280px;}
    .big-target-box { height: 160px; border-radius: 20px; border: 4px solid white; box-shadow: 0px 8px 20px rgba(0,0,0,0.2); margin: 10px auto; width: 80%; }
    .slot-preview { height: 60px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 5px; }
    .res-box { height: 100px; border-radius: 15px; border: 2px solid white; box-shadow: 0px 5px 15px rgba(0,0,0,0.15); }
    .theory-box { height: 30px; width: 30px; border-radius: 6px; border: 1px solid #ccc; margin: 0 auto; }
    div[data-testid="stColorPicker"] > label { display: none; }
    input { text-align: center !important; }
    @keyframes pulse-lila {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(155, 89, 182, 0.7); }
        70% { transform: scale(1.03); box-shadow: 0 0 0 10px rgba(155, 89, 182, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(155, 89, 182, 0); }
    }
    .btn-kofi {
        display: inline-block; background-color: #9b59b6; color: white !important; 
        padding: 12px 20px; border-radius: 10px; text-decoration: none; 
        font-weight: bold; width: 100%; text-align: center; 
        animation: pulse-lila 2s infinite;
    }
</style>""", unsafe_allow_html=True)

# --- 🟡 LOGICA DE ESTADO ---
if 'lg' not in st.session_state: st.session_state.lg = "Es"
if 'n_f' not in st.session_state: st.session_state.n_f = 4
_T = _D[st.session_state.lg]
_df = ["#FFFFFF", "#00FFFF", "#000000", "#FFFF00", "#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#808080", "#A52A2A"]

def _sp(i): st.session_state[f"t_{i}"] = st.session_state[f"p_{i}"].upper()
def _st(i): st.session_state[f"p_{i}"] = _cl(st.session_state[f"t_{i}"])

def _dr(idx):
    for i in range(idx, st.session_state.n_f - 1):
        st.session_state[f"p_{i}"] = st.session_state[f"p_{i+1}"]
        st.session_state[f"t_{i}"] = st.session_state[f"t_{i+1}"]
        st.session_state[f"n_{i}"] = st.session_state[f"n_{i+1}"]
    if st.session_state.n_f > 1: st.session_state.n_f -= 1

# --- ⚪ SIDEBAR ---
with st.sidebar:
    if st.button(_T["l"]):
        st.session_state.lg = "En" if st.session_state.lg == "Es" else "Es"
        st.rerun()
    st.header(_T["p"])
    st.session_state.n_f = st.number_input(_T["nf"], 1, 10, st.session_state.n_f)
    if st.button(_T["rst"], use_container_width=True):
        for i in range(10): st.session_state[f"n_{i}"] = 0
        st.rerun()
    st.divider()
    st.markdown(f'<a href="https://ko-fi.com/D1D41Y3WLU" target="_blank" class="btn-kofi">☕ {_T["s"]}</a>', unsafe_allow_html=True)

# --- 🟠 UI PRINCIPAL ---
st.markdown(f"<h2 style='text-align: center;'>{_T['th']}</h2>", unsafe_allow_html=True)
_, _cc, _ = st.columns([1, 1.2, 1])
if "p_tgt" not in st.session_state: st.session_state.p_tgt, st.session_state.t_tgt = "#60A26A", "#60A26A"
with _cc:
    st.text_input("HEX", key="t_tgt", on_change=_st, args=("tgt",))
    st.color_picker("CLR", key="p_tgt", on_change=_sp, args=("tgt",))
    _thx = st.session_state.p_tgt
    st.markdown(f"<div class='big-target-box' style='background:{_thx};'></div>", unsafe_allow_html=True)
    _trg = _hr(_thx)

# --- 🔴 FILAMENTOS ---
st.divider()
st.header(_T["r"])
_fc, _vr = [], []
for i in range(st.session_state.n_f):
    if i % 4 == 0: _cols = st.columns(4)
    if f"p_{i}" not in st.session_state: st.session_state[f"p_{i}"], st.session_state[f"t_{i}"] = _df[i], _df[i]
    if f"n_{i}" not in st.session_state: st.session_state[f"n_{i}"] = 1 if i == 0 else 0
    with _cols[i % 4]:
        st.markdown(f"<div class='slot-preview' style='background:{st.session_state[f'p_{i}']};'></div>", unsafe_allow_html=True)
        st.color_picker(f"P{i}", key=f"p_{i}", on_change=_sp, args=(i,))
        st.text_input(f"HEX {i+1}", key=f"t_{i}", on_change=_st, args=(i,))
        _fc.append(_hr(st.session_state[f"p_{i}"]))
        _vr.append(st.number_input(f"P{i+1}", 0, 20, key=f"n_{i}"))
        st.button("🗑️", key=f"del_{i}", on_click=_dr, args=(i,), use_container_width=True)

# --- ✨ SUGERENCIA ---
st.divider()
st.header(_T["am"])
_sug = _ax(_trg, _fc, st.session_state.n_f)
_scs = st.columns(5)
for i in range(st.session_state.n_f):
    if i % 5 == 0 and i > 0: _scs = st.columns(5)
    with _scs[i % 5]:
        st.markdown(f"<div class='theory-box' style='background:{st.session_state[f'p_{i}']};'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-weight:bold; margin-bottom:0;'>{_sug[i]} P</p>", unsafe_allow_html=True)
        st.caption(f"S{i+1}")

# --- ⚖️ COMPARATIVA ---
_rhx = _sx(_fc, _vr)
st.divider()
st.header(_T["cm"])
_ca, _cb = st.columns(2)
_ca.subheader(_T["tl"]); _ca.markdown(f"<div class='res-box' style='background:{_thx};'></div>", unsafe_allow_html=True); _ca.write(f"HEX: {_thx}")
_cb.subheader(_T["sl"]); _cb.markdown(f"<div class='res-box' style='background:{_rhx};'></div>", unsafe_allow_html=True); _cb.write(f"HEX: {_rhx}")

# --- 🏆 TEORIA ---
st.divider()
st.header(_T["mm"])
_pv = _tx(_trg)
_tc = [("#00FFFF", "Cian"), ("#FF00FF", "Magenta"), ("#FFFF00", "Amarillo"), ("#000000", "Negro"), ("#FFFFFF", "Blanco")]
_tc_cols = st.columns(5)
for i, _tcol in enumerate(_tc_cols):
    with _tcol:
        st.markdown(f"<div class='theory-box' style='background:{_tc[i][0]};'></div>", unsafe_allow_html=True)
        st.write(f"**{_pv[i]} P**")
        st.caption(_tc[i][1])
