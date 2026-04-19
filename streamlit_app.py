import streamlit as st

# --- 🟢 MOTOR DE CÁLCULO ---
_cln = lambda x: (x.strip().replace(" ", "") if x.strip().replace(" ", "").startswith('#') else '#'+x.strip().replace(" ", ""))[:7].ljust(7,'0')
_h2r = lambda x: tuple(int(x.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
_r2h = lambda x: '#%02x%02x%02x' % x

def _kx_(_t_):
    _v_ = [x/255 for x in _t_]; _f_ = 1 - max(_v_); _g_ = min(_v_)
    if _f_ < 1:
        _a_=(1-_v_[0]-_f_)/(1-_f_); _s_=(1-_v_[1]-_f_)/(1-_f_); _d_=(1-_v_[2]-_f_)/(1-_f_)
    else: _a_=_s_=_d_=0
    _q_ = _a_+_s_+_d_+_f_+_g_
    return [round((x/_q_)*4, 1) if _q_>0 else 0 for x in [_a_,_s_,_d_,_f_,_g_]]

def _sx_(_fc_, _vr_):
    _st_ = sum(_vr_)
    if _st_ <= 0: return "#000000"
    return _r2h(tuple(int(sum(_fc_[i][j] * _vr_[i] for i in range(4)) / _st_) for j in range(3)))

# --- 🔵 CONFIGURACIÓN E IDIOMAS ---
texts = {
    "Es": {
        "title": "🎨 Mezclador AMS Pro", "pref": "⚙️ Preferencias", "lang": "Switch to English (EN)",
        "pastel_q": "¿Tono pastel?", "pastel_i": "Intensidad Pastel", "support": "Apoya el proyecto",
        "caption": "¡Gracias por tu apoyo!", "results": "1. Tus Filamentos y Proporciones",
        "compare": "2. Comparativa de Mezcla Real", "target_label": "Tu Objetivo",
        "sim_label": "Mezcla Real", "target_header": "🎯 COLOR DESEADO",
        "master_mix": "🏆 Combinación teórica perfecta (CMYKW)"
    },
    "En": {
        "title": "🎨 AMS Mixer Pro", "pref": "⚙️ Settings", "lang": "Cambiar a Español (ES)",
        "pastel_q": "Pastel tone?", "pastel_i": "Pastel Intensity", "support": "Support the project",
        "caption": "Thanks for your support!", "results": "1. Your Filaments & Proportions",
        "compare": "2. Real Mixing Comparison", "target_label": "Your Target",
        "sim_label": "Real Mix", "target_header": "🎯 TARGET COLOR",
        "master_mix": "🏆 Theoretical perfect mix (CMYKW)"
    }
}

st.set_page_config(page_title="AMS Mixer Pro", layout="wide")

# --- 🟣 ESTILOS CSS (DISEÑO Y ANIMACIÓN) ---
st.markdown(f"""
<style>
    [data-testid="stSidebar"][aria-expanded="true"]{{min-width: 280px; max-width: 280px;}}
    .big-target-box {{ height: 220px; border-radius: 25px; border: 4px solid white; box-shadow: 0px 10px 30px rgba(0,0,0,0.3); margin: 15px auto; width: 85%; transition: 0.5s; }}
    .slot-preview {{ height: 80px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1); }}
    .res-box {{ height: 110px; border-radius: 15px; border: 2px solid white; box-shadow: 0px 5px 15px rgba(0,0,0,0.2); }}
    .theory-box {{ height: 50px; border-radius: 10px; border: 1px solid #ccc; }}
    div[data-testid="stColorPicker"] > label {{ display: none; }}
    
    /* ANIMACIÓN LATIDO LILA */
    @keyframes pulse-lila {{
        0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(155, 89, 182, 0.7); }}
        70% {{ transform: scale(1.03); box-shadow: 0 0 0 12px rgba(155, 89, 182, 0); }}
        100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(155, 89, 182, 0); }}
    }}
    .btn-kofi {{
        display: inline-block; background-color: #9b59b6; color: white !important; 
        padding: 14px 20px; border-radius: 12px; text-decoration: none; 
        font-weight: bold; width: 100%; text-align: center; 
        animation: pulse-lila 2s infinite; border: none; transition: 0.3s;
    }}
    .btn-kofi:hover {{ background-color: #8e44ad; transform: scale(1.05); animation: none; }}
</style>
""", unsafe_allow_html=True)

if 'lang' not in st.session_state: st.session_state.lang = "Es"
t = texts[st.session_state.lang]

# --- 🟡 LÓGICA DE SINCRONIZACIÓN ---
def sync_p(i): st.session_state[f"t_{i}"] = st.session_state[f"p_{i}"].upper()
def sync_t(i): st.session_state[f"p_{i}"] = _cln(st.session_state[f"t_{i}"])

# --- ⚪ BARRA LATERAL ---
with st.sidebar:
    if st.button(t["lang"]):
        st.session_state.lang = "En" if st.session_state.lang == "Es" else "Es"
        st.rerun()
    st.header(t["pref"])
    es_pastel = st.checkbox(t["pastel_q"], value=False)
    f_pastel = st.slider(t["pastel_i"], 1, 10, 5) if es_pastel else 1
    
    st.divider()
    st.subheader(t["support"])
    st.markdown(f"""
        <a href="https://ko-fi.com/D1D41Y3WLU" target="_blank" class="btn-kofi">
            ☕ {t['support']} (Ko-fi)
        </a>
    """, unsafe_allow_html=True)
    st.caption(f"<div style='text-align: center; margin-top: 15px;'>{t['caption']}</div>", unsafe_allow_html=True)

# --- 🟠 INTERFAZ PRINCIPAL ---
st.title(t["title"])
st.markdown(f"<h2 style='text-align: center;'>{t['target_header']}</h2>", unsafe_allow_html=True)
_, col_c, _ = st.columns([1, 1.5, 1])

if "p_tgt" not in st.session_state: st.session_state.p_tgt = "#60A26A"
if "t_tgt" not in st.session_state: st.session_state.t_tgt = "#60A26A"

with col_c:
    st.text_input("HEX", key="t_tgt", on_change=sync_t, args=("tgt",))
    st.color_picker("Color", key="p_tgt", on_change=sync_p, args=("tgt",))
    target_hex = st.session_state.p_tgt
    st.markdown(f"<div class='big-target-box' style='background:{target_hex};'></div>", unsafe_allow_html=True)
    target_rgb = _h2r(target_hex)

# --- 🔴 CONFIGURACIÓN DE FILAMENTOS ---
st.divider()
st.header(t["results"])
cols = st.columns(4)
fil_colors, v_ranuras = [], []
defaults = ["#FFFFFF", "#00FFFF", "#000000", "#FFFF00"]

for i in range(4):
    if f"p_{i}" not in st.session_state: st.session_state[f"p_{i}"] = defaults[i]
    if f"t_{i}" not in st.session_state: st.session_state[f"t_{i}"] = defaults[i]
    with cols[i]:
        st.markdown(f"<div class='slot-preview' style='background:{st.session_state[f'p_{i}']};'></div>", unsafe_allow_html=True)
        st.color_picker(f"P{i}", key=f"p_{i}", on_change=sync_p, args=(i,))
        st.text_input(f"HEX {i+1}", key=f"t_{i}", on_change=sync_t, args=(i,))
        fil_colors.append(_h2r(st.session_state[f"p_{i}"]))
        v_ranuras.append(st.number_input(f"Partes", 0, 20, 1 if i==0 else 0, 1, key=f"n_{i}"))

# --- ⚖️ COMPARATIVA ---
res_hex = _sx_(fil_colors, v_ranuras)
st.divider()
st.header(t["compare"])
ca, cb = st.columns(2)
with ca:
    st.subheader(t["target_label"])
    st.markdown(f"<div class='res-box' style='background:{target_hex};'></div>", unsafe_allow_html=True)
with cb:
    st.subheader(t["sim_label"])
    st.markdown(f"<div class='res-box' style='background:{res_hex};'></div>", unsafe_allow_html=True)

# --- 🏆 COMBINACIÓN PERFECTA CMYKW ---
st.divider()
st.header(t["master_mix"])
p_vals = _kx_(target_rgb)
t_cols = st.columns(5)
t_data = [("#00FFFF", "Cian"), ("#FF00FF", "Magenta"), ("#FFFF00", "Amarillo"), ("#000000", "Negro"), ("#FFFFFF", "Blanco")]

for i, tcol in enumerate(t_cols):
    tcol.markdown(f"<div class='theory-box' style='background:{t_data[i][0]};'></div>", unsafe_allow_html=True)
    tcol.write(f"**{p_vals[i]} P**")
    tcol.caption(t_data[i][1])
