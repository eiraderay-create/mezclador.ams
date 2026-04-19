import streamlit as st

# --- FUNCIONES DE APOYO ---
def clean_hex(hex_str):
    clean = hex_str.strip().replace(" ", "")
    if not clean.startswith('#'): clean = '#' + clean
    if len(clean) > 7: clean = clean[:7]
    if len(clean) < 7: clean = clean.ljust(7, '0')
    return clean

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    try:
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    except: return (0,0,0)

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# --- TRADUCCIONES ---
texts = {
    "Es": {
        "title": "🎨 Mezclador AMS Pro",
        "pref": "⚙️ Preferencias",
        "lang": "Switch to English (EN)",
        "pastel_q": "¿Tono pastel?",
        "pastel_i": "Intensidad Pastel",
        "support": "Apoya el proyecto",
        "results": "1. Configura tus Filamentos",
        "compare": "2. Comparativa de Mezcla",
        "target_label": "Tu Objetivo",
        "sim_label": "Mezcla Real",
        "target_header": "🎯 COLOR DESEADO",
        "master_mix": "🏆 Combinación teórica perfecta (CMYKW)"
    },
    "En": {
        "title": "🎨 AMS Mixer Pro",
        "pref": "⚙️ Settings",
        "lang": "Cambiar a Español (ES)",
        "pastel_q": "Pastel tone?",
        "pastel_i": "Pastel Intensity",
        "support": "Support the project",
        "results": "1. Configure your Filaments",
        "compare": "2. Mixing Comparison",
        "target_label": "Your Target",
        "sim_label": "Real Mix",
        "target_header": "🎯 TARGET COLOR",
        "master_mix": "🏆 Theoretical perfect mix (CMYKW)"
    }
}

st.set_page_config(page_title="AMS Mixer Pro", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
<style>
    [data-testid="stSidebar"][aria-expanded="true"]{min-width: 280px; max-width: 280px;}
    .big-target-box { height: 180px; border-radius: 20px; border: 4px solid white; box-shadow: 0px 10px 25px rgba(0,0,0,0.3); margin: 10px auto; width: 90%; }
    .slot-preview { height: 80px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 10px; }
    .res-box { height: 110px; border-radius: 15px; border: 2px solid white; box-shadow: 0px 5px 15px rgba(0,0,0,0.2); }
    .theory-box { height: 45px; border-radius: 8px; border: 1px solid #ccc; }
    div[data-testid="stColorPicker"] > label { display: none; }
    div[data-testid="stTextInput"] > label { font-size: 0.8rem; color: #666; }
</style>
""", unsafe_allow_html=True)

if 'lang' not in st.session_state: st.session_state.lang = "Es"
t = texts[st.session_state.lang]

# --- LÓGICA DE SINCRONIZACIÓN DE COLORES ---
def on_picker_change(idx):
    # Si cambia el selector circular, actualizamos el texto HEX
    picker_key = f"picker_{idx}"
    text_key = f"text_{idx}"
    st.session_state[text_key] = st.session_state[picker_key].upper()

def on_text_change(idx):
    # Si escribes el HEX y das a Intro, actualizamos el selector circular
    text_key = f"text_{idx}"
    picker_key = f"picker_{idx}"
    st.session_state[picker_key] = clean_hex(st.session_state[text_key])

# --- BARRA LATERAL ---
with st.sidebar:
    if st.button(t["lang"]):
        st.session_state.lang = "En" if st.session_state.lang == "Es" else "Es"
        st.rerun()
    st.header(t["pref"])
    es_pastel = st.checkbox(t["pastel_q"], value=False)
    fuerza_pastel = st.slider(t["pastel_i"], 1, 10, 5) if es_pastel else 1
    st.divider()
    st.markdown(f'<div style="text-align: center;"><a href="https://ko-fi.com/D1D41Y3WLU" target="_blank" style="text-decoration: none;"><div style="background-color: #9b59b6; color: white; padding: 12px; border-radius: 10px; font-weight: bold;">☕ {t["support"]}</div></a></div>', unsafe_allow_html=True)

# --- COLOR OBJETIVO ---
st.markdown(f"<h2 style='text-align: center;'>{t['target_header']}</h2>", unsafe_allow_html=True)
_, col_c, _ = st.columns([1, 1.5, 1])

# Inicializar estado objetivo
if "picker_tgt" not in st.session_state: st.session_state.picker_tgt = "#60A26A"
if "text_tgt" not in st.session_state: st.session_state.text_tgt = "#60A26A"

with col_c:
    st.text_input("HEX", key="text_tgt", on_change=on_text_change, args=("tgt",))
    st.color_picker("Color", key="picker_tgt", on_change=on_picker_change, args=("tgt",))
    target_hex = st.session_state.picker_tgt
    st.markdown(f"<div class='big-target-box' style='background:{target_hex};'></div>", unsafe_allow_html=True)
    target_rgb = hex_to_rgb(target_hex)

# --- 1. CONFIGURACIÓN DE FILAMENTOS ---
st.divider()
st.header(t["results"])
cols = st.columns(4)
fil_colors, v_ranuras = [], []
defaults = ["#FFFFFF", "#00FFFF", "#000000", "#FFFF00"]

for i in range(4):
    # Inicializar estados de los 4 slots si no existen
    if f"picker_{i}" not in st.session_state: st.session_state[f"picker_{i}"] = defaults[i]
    if f"text_{i}" not in st.session_state: st.session_state[f"text_{i}"] = defaults[i]
    
    with cols[i]:
        # Rectángulo de previsualización (SIEMPRE sincronizado con el picker)
        st.markdown(f"<div class='slot-preview' style='background:{st.session_state[f'picker_{i}']};'></div>", unsafe_allow_html=True)
        
        # Selector circular
        st.color_picker(f"P{i}", key=f"picker_{i}", on_change=on_picker_change, args=(i,))
        
        # Input de texto HEX
        st.text_input(f"HEX {i+1}", key=f"text_{i}", on_change=on_text_change, args=(i,))
        
        # Guardamos color para cálculos
        fil_colors.append(hex_to_rgb(st.session_state[f"picker_{i}"]))
        
        # Selector de partes
        v_ranuras.append(st.number_input(f"Partes", 0, 20, 1 if i==0 else 0, 1, key=f"n_{i}"))

# --- COMPARATIVA ---
suma = sum(v_ranuras)
res_hex = rgb_to_hex(tuple(int(sum(fil_colors[idx][j] * v_ranuras[idx] for idx in range(4)) / (suma if suma>0 else 1)) for j in range(3))) if suma>0 else "#000000"

st.divider()
st.header(t["compare"])
ca, cb = st.columns(2)
with ca:
    st.subheader(t["target_label"])
    st.markdown(f"<div class='res-box' style='background:{target_hex};'></div>", unsafe_allow_html=True)
with cb:
    st.subheader(t["sim_label"])
    st.markdown(f"<div class='res-box' style='background:{res_hex};'></div>", unsafe_allow_html=True)

# --- COMBINACIÓN PERFECTA CMYKW ---
st.divider()
st.header(t["master_mix"])
r, g, b = [x/255 for x in target_rgb]
k = 1 - max(r, g, b)
w = min(r, g, b)
if k < 1:
    c = (1-r-k)/(1-k); m = (1-g-k)/(1-k); y = (1-b-k)/(1-k)
else: c=m=y=0

total_raw = c + m + y + k + w
p_vals = [round((x/total_raw)*4, 1) if total_raw > 0 else 0 for x in [c, m, y, k, w]]

t_cols = st.columns(5)
t_data = [("#00FFFF", "Cian"), ("#FF00FF", "Magenta"), ("#FFFF00", "Amarillo"), ("#000000", "Negro"), ("#FFFFFF", "Blanco")]
for i, tcol in enumerate(t_cols):
    tcol.markdown(f"<div class='theory-box' style='background:{t_data[i][0]};'></div>", unsafe_allow_html=True)
    tcol.write(f"**{p_vals[i]} P**")
    tcol.caption(t_data[i][1])

st.info(f"Suma total actual: {suma} partes.")
