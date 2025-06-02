
import streamlit as st

st.set_page_config(page_title="Laudo USG Tireoide", layout="centered")
st.title("📋 Gerador de Laudo: USG Tireoide com TI-RADS")

st.markdown("Preencha os campos abaixo para gerar um laudo estruturado com base nos seus modelos.")

# --- MEDIDAS DA TIREOIDE ---
st.header("1. Medidas da Tireoide")

# Lobo Direito
st.subheader("Lobo Direito (cm)")
ld_l = st.number_input("LD - Longitudinal", min_value=0.0, step=0.1, format="%.1f")
ld_ap = st.number_input("LD - Ântero-posterior", min_value=0.0, step=0.1, format="%.1f")
ld_t = st.number_input("LD - Transversal", min_value=0.0, step=0.1, format="%.1f")
vol_ld = round((ld_l * ld_ap * ld_t) * 0.52, 2) if all([ld_l, ld_ap, ld_t]) else None

# Lobo Esquerdo
st.subheader("Lobo Esquerdo (cm)")
le_l = st.number_input("LE - Longitudinal", min_value=0.0, step=0.1, format="%.1f")
le_ap = st.number_input("LE - Ântero-posterior", min_value=0.0, step=0.1, format="%.1f")
le_t = st.number_input("LE - Transversal", min_value=0.0, step=0.1, format="%.1f")
vol_le = round((le_l * le_ap * le_t) * 0.52, 2) if all([le_l, le_ap, le_t]) else None

# Istmo
st.subheader("Istmo (opcional)")
istmo = st.number_input("Espessura do Istmo (cm)", min_value=0.0, step=0.1, format="%.1f")
istmo_txt = f"Istmo medindo {istmo:.1f} cm." if istmo else "Istmo é filiforme."

# --- PARENQUIMA ---
st.header("2. Parênquima Tireoidiano")
ecotextura = st.selectbox("Ecotextura", ["Homogênea", "Heterogênea"])
vascularizacao_parenquima = None
com_doppler = st.checkbox("Exame com Doppler?")
if com_doppler:
    vascularizacao_parenquima = st.selectbox("Vascularização do Parênquima", ["Habitual", "Hipervascularização", "Hipovascularização"])

# --- NÓDULOS ---
st.header("3. Nódulos Tireoidianos")

nodulos = []

if "n_nodulos" not in st.session_state:
    st.session_state.n_nodulos = 0

def add_nodulo():
    st.session_state.n_nodulos += 1

st.button("➕ Adicionar Nódulo", on_click=add_nodulo)

for i in range(st.session_state.n_nodulos):
    st.subheader(f"Nódulo {i+1}")
    local = st.text_input(f"Localização do Nódulo {i+1}", key=f"loc{i}")
    comp = st.selectbox(f"Composição", ["Cístico", "Espongiforme", "Misto", "Sólido"], key=f"comp{i}")
    eco = st.selectbox("Ecogenicidade", ["Anecoico", "Isoecogênico", "Hipoecogênico", "Muito hipoecogênico"], key=f"eco{i}")
    forma = st.selectbox("Forma", ["Mais larga que alta", "Mais alta que larga"], key=f"forma{i}")
    margem = st.selectbox("Margens", ["Lisa", "Mal definida", "Lobulada ou irregular", "Com extensão extra-tireoidiana"], key=f"margem{i}")
    focos = st.multiselect("Focos Ecogênicos", ["Nenhum", "Macrocalcificações", "Calcificações periféricas", "Microcalcificações"], key=f"focos{i}")
    medidas = st.text_input("Medidas (cm)", key=f"medidas{i}")
    if com_doppler:
        vascularizacao_nodulo = st.selectbox("Vascularização do Nódulo", ["Ausente", "Predominante periférica", "Predominante central", "Periférica e central"], key=f"vasc{i}")
    else:
        vascularizacao_nodulo = None

    nodulos.append({
        "local": local,
        "comp": comp,
        "eco": eco,
        "forma": forma,
        "margem": margem,
        "focos": focos,
        "medidas": medidas,
        "vascularizacao": vascularizacao_nodulo
    })

# --- CONSTRUÇÃO DO LAUDO ---
if st.button("📝 Gerar Laudo"):
    laudo = "**ULTRASSONOGRAFIA DA TIREOIDE**\n\n"
    laudo += "**Indicação:** Avaliação ultrassonográfica da glândula tireoide.\n\n"

    laudo += "**Análise:**\n"
    laudo += f"Lobo direito mede {ld_l} x {ld_ap} x {ld_t} cm"
    laudo += f", volume estimado de {vol_ld:.2f} cm³.\n" if vol_ld else ".\n"
    laudo += f"Lobo esquerdo mede {le_l} x {le_ap} x {le_t} cm"
    laudo += f", volume estimado de {vol_le:.2f} cm³.\n" if vol_le else ".\n"
    laudo += istmo_txt + "\n"
    laudo += f"Parênquima de ecotextura {ecotextura.lower()}.\n"
    if com_doppler and vascularizacao_parenquima:
        laudo += f"Vascularização do parênquima: {vascularizacao_parenquima.lower()}.\n"

    if nodulos:
        for i, n in enumerate(nodulos):
            laudo += f"Nódulo {i+1}: formação {n['comp'].lower()}, {n['eco'].lower()}, {n['forma'].lower()}, margens {n['margem'].lower()}"
            if n['focos'] and "Nenhum" not in n['focos']:
                laudo += f", com {', '.join([f.lower() for f in n['focos']])}"
            laudo += f", medindo {n['medidas']} cm"
            if com_doppler and n['vascularizacao']:
                laudo += f", com vascularização {n['vascularizacao'].lower()}"
            laudo += f", localizado em {n['local'].lower()}.\n"

    laudo += "\n**Opinião:**\nAchados compatíveis com os descritos. (Adicionar TI-RADS conforme avaliação do nódulo)."

    st.markdown("---")
    st.markdown("### 🖨️ Laudo Gerado")
    st.text_area("Laudo completo", laudo, height=400)
